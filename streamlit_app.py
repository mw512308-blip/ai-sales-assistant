import streamlit as st
import google.generativeai as genai
import json
from gtts import gTTS
import io

# 1. Page Config & Force Dark Theme
st.set_page_config(page_title="AI Sales Assistant", page_icon="🛍️", layout="centered", initial_sidebar_state="collapsed")

# 2. Strict CSS Injection for Dark Mode & Styling
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #0f172a !important;
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%) !important;
        color: #ffffff !important;
    }
    
    [data-testid="stHeader"] {display: none;}
    footer {display: none;}

    .header-box {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 16px;
        padding: 18px;
        text-align: center;
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
    }

    .app-title {
        font-size: 1.8rem;
        font-weight: 800;
        color: #38bdf8;
        margin-bottom: 4px;
    }

    .status-tag {
        font-size: 0.85rem;
        color: #4ade80;
        font-weight: 600;
    }

    p, span, label, div {
        color: #f1f5f9 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Main Header Card
st.markdown("""
    <div class='header-box'>
        <div class='app-title'>🛍️ AI Sales Assistant</div>
        <div class='status-tag'>🟢 Online | Always Ready</div>
    </div>
""", unsafe_allow_html=True)

# WhatsApp & Facebook Action Buttons
whatsapp_num = "923183705066"
wa_url = f"https://wa.me/{whatsapp_num}?text=Hello,%20I%20want%20to%20place%20an%20order."
fb_url = "https://facebook.com"

col1, col2 = st.columns(2)
with col1:
    st.link_button("💬 WhatsApp", wa_url, use_container_width=True, type="primary")
with col2:
    st.link_button("🌐 Facebook", fb_url, use_container_width=True, type="secondary")

st.divider()

# Robust Gemini AI Initialization
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ API Key Secret میں موجود نہیں ہے۔")
    st.stop()

genai.configure(api_key=api_key)

try:
    with open("products.json", "r", encoding="utf-8") as f:
        products = json.load(f)
except Exception:
    products = []

system_prompt = f"You are an expert AI Sales Assistant for a store in Pakistan. Respond politely in Pashto, Roman Urdu, or English. Product inventory: {json.dumps(products)}. Store WhatsApp: 03183705066"

# Model selection using correct standard models
try:
    model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=system_prompt)
except Exception:
    model = genai.GenerativeModel(model_name="gemini-pro", system_instruction=system_prompt)

def play_audio(text):
    try:
        tts = gTTS(text=text, lang='ur')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')
    except Exception:
        pass

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

voice_input = st.audio_input("🎤 Record Voice / آواز سے سوال کریں")
user_text = st.chat_input("Sawal poochein / Ask a question...")

prompt_to_send = user_text if user_text else ("Voice message received." if voice_input else None)

if prompt_to_send:
    st.session_state.messages.append({"role": "user", "content": prompt_to_send})
    with st.chat_message("user"):
        st.write(prompt_to_send)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt_to_send)
            bot_reply = response.text
        except Exception as e:
            bot_reply = f"معذرت! API سے رابطہ میں مسئلہ آ رہا ہے: {str(e)}"
            
        st.write(bot_reply)
        
        for product in products:
            if product.get("name", "").lower() in bot_reply.lower() or product.get("name", "").lower() in prompt_to_send.lower():
                if "image" in product:
                    st.image(product["image"], caption=f"{product['name']} - Rs. {product['price']}", width=250)
        
        play_audio(bot_reply)
        
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
