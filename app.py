import streamlit as st
import google.generativeai as genai
import json
from gtts import gTTS
import io

# 1. Page Config
st.set_page_config(page_title="AI Sales Assistant", page_icon="🛍️", layout="centered")

# 2. Premium Dark Gradient UI & Custom Styling
st.markdown("""
    <style>
    [data-testid="stHeader"] {display: none;}
    .block-container {padding-top: 1.5rem; padding-bottom: 2rem;}
    footer {display: none;}
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
        color: #f8fafc;
    }

    .header-box {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }

    .app-title {
        font-size: 1.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
    }

    .status-tag {
        font-size: 0.85rem;
        color: #4ade80;
        font-weight: 600;
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

# WhatsApp & Facebook Side-by-Side Action Buttons
whatsapp_num = "923183705066"
wa_url = f"https://wa.me/{whatsapp_num}?text=Hello,%20I%20want%20to%20place%20an%20order."
fb_url = "https://facebook.com"

col1, col2 = st.columns(2)
with col1:
    st.link_button("💬 WhatsApp", wa_url, use_container_width=True, type="primary")
with col2:
    st.link_button("🌐 Facebook", fb_url, use_container_width=True, type="secondary")

st.divider()

# Backend AI Logic & Secrets Integration
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

system_prompt = f"You are an expert sales assistant. Inventory: {json.dumps(products)}. WhatsApp: 03183705066"
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
