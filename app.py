import streamlit as st
import google.generativeai as genai
import json
from gtts import gTTS
import io

# 1. Page Config
st.set_page_config(page_title="AI Sales Assistant", page_icon="🛍️", layout="centered")

# 2. Custom Modern Styling (Inline & HTML Safe)
st.markdown("""
    <style>
    [data-testid="stHeader"] {display: none;}
    .block-container {padding-top: 1.5rem; padding-bottom: 2rem;}
    footer {display: none;}
    
    .main-card {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        border: 1px solid #334155;
        margin-bottom: 15px;
    }
    .title-text {
        font-size: 26px;
        font-weight: 800;
        color: #38bdf8;
        margin: 0;
    }
    .sub-text {
        font-size: 13px;
        color: #94a3b8;
        margin-top: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.markdown("""
    <div class="main-card">
        <div class="title-text">🛍️ AI Sales Assistant</div>
        <div class="sub-text">🟢 Online | Fast Response</div>
    </div>
""", unsafe_allow_html=True)

# WhatsApp & Facebook Buttons
whatsapp_num = "923183705066"
wa_url = f"https://wa.me/{whatsapp_num}?text=Hello,%20I%20want%20to%20place%20an%20order."
fb_url = "https://facebook.com"

col1, col2 = st.columns(2)
with col1:
    st.link_button("💬 WhatsApp", wa_url, use_container_width=True, type="primary")
with col2:
    st.link_button("🌐 Facebook", fb_url, use_container_width=True, type="secondary")

st.divider()

# Backend Gemini AI Setup
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("API Key missing in Secrets!")
    st.stop()

genai.configure(api_key=api_key)

try:
    with open("products.json", "r", encoding="utf-8") as f:
        products = json.load(f)
except Exception:
    products = []

system_prompt = f"You are a sales assistant. Inventory: {json.dumps(products)}. WhatsApp: 03183705066"
model = genai.GenerativeModel(model_name="gemini-3.6-flash", system_instruction=system_prompt)

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
        except Exception:
            bot_reply = "معذرت! اس وقت سسٹم پر بوجھ زیادہ ہے۔ براہ کرم 1 منٹ بعد دوبارہ کوشش کریں۔"
            
        st.write(bot_reply)
        
        for product in products:
            if product.get("name", "").lower() in bot_reply.lower() or product.get("name", "").lower() in prompt_to_send.lower():
                if "image" in product:
                    st.image(product["image"], caption=f"{product['name']} - Rs. {product['price']}", width=250)
        
        play_audio(bot_reply)
        
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
