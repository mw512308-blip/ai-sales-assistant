import streamlit as st
import google.generativeai as genai
import json
from gtts import gTTS
import io

# 1. Page Config
st.set_page_config(
    page_title="AI Sales Assistant", 
    page_icon="🛍️", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# 2. Complete CSS Styling (Dark Theme & White Text Fix)
st.markdown("""
    <style>
    /* Full Page Background */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #0f172a !important;
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%) !important;
    }
    
    [data-testid="stHeader"] {display: none;}
    footer {display: none;}

    /* Force Pure White Text Visibility Everywhere */
    p, span, label, div, h1, h2, h3, .stMarkdown, [data-testid="stChatMessage"] {
        color: #ffffff !important;
    }

    /* Text Input Styling */
    input, textarea {
        color: #ffffff !important;
        background-color: #1e293b !important;
    }

    /* Header Styling */
    .header-box {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 16px;
        padding: 18px;
        text-align: center;
        margin-bottom: 20px;
    }

    .app-title {
        font-size: 1.8rem;
        font-weight: 800;
        color: #38bdf8 !important;
        margin-bottom: 4px;
    }

    .status-tag {
        font-size: 0.85rem;
        color: #4ade80 !important;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# Main Header
st.markdown("""
    <div class='header-box'>
        <div class='app-title'>🛍️ AI Sales Assistant</div>
        <div class='status-tag'>🟢 Online | Always Ready</div>
    </div>
""", unsafe_allow_html=True)

# Buttons Section
whatsapp_num = "923183705066"
wa_url = f"https://wa.me/{whatsapp_num}?text=Hello,%20I%20want%20to%20place%20an%20order."
fb_url = "https://facebook.com"

col1, col2 = st.columns(2)
with col1:
    st.link_button("💬 WhatsApp", wa_url, use_container_width=True, type="primary")
with col2:
    st.link_button("🌐 Facebook", fb_url, use_container_width=True, type="secondary")

st.divider()

# Secrets & Gemini Setup
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ API Key Secret میں موجود نہیں ہے۔ Secrets میں GEMINI_API_KEY شامل کریں۔")
    st.stop()

genai.configure(api_key=api_key)

try:
    with open("products.json", "r", encoding="utf-8") as f:
        products = json.load(f)
except Exception:
    products = []

system_prompt = f"You are an expert AI Sales Assistant for a store in Pakistan. Respond politely in Pashto, Roman Urdu, or English. Product inventory: {json.dumps(products)}. Store WhatsApp: 03183705066"

# Dynamic Model Selector (Error 404 Avoidance)
AVAILABLE_MODELS = ["gemini-1.5-flash", "gemini-pro"]

def get_response(user_input):
    for model_name in AVAILABLE_MODELS:
        try:
            model = genai.GenerativeModel(model_name=model_name, system_instruction=system_prompt)
            res = model.generate_content(user_input)
            return res.text
        except Exception:
            continue
    return "معذرت! اس وقت API سے رابطہ نہیں ہو پا رہا۔ براہ کرم کی (Key) اور کنیکشن دوبارہ چیک کریں۔"

def play_audio(text):
    try:
        tts = gTTS(text=text, lang='ur')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')
    except Exception:
        pass

# Chat History Setup
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User Inputs
voice_input = st.audio_input("🎤 Record Voice / آواز سے سوال کریں")
user_text = st.chat_input("Sawal poochein / Ask a question...")

prompt_to_send = user_text if user_text else ("Voice message received." if voice_input else None)

if prompt_to_send:
    st.session_state.messages.append({"role": "user", "content": prompt_to_send})
    with st.chat_message("user"):
        st.write(prompt_to_send)

    with st.chat_message("assistant"):
        bot_reply = get_response(prompt_to_send)
        st.write(bot_reply)
        
        # Display product images if relevant
        for product in products:
            if product.get("name", "").lower() in bot_reply.lower() or product.get("name", "").lower() in prompt_to_send.lower():
                if "image" in product:
                    st.image(product["image"], caption=f"{product['name']} - Rs. {product['price']}", width=250)
        
        play_audio(bot_reply)
        
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
