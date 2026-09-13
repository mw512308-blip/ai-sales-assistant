import streamlit as st
import google.generativeai as genai
import json
from gtts import gTTS
import io

# 1. Page Config
st.set_page_config(page_title="AI Sales Assistant", page_icon="🛍️", layout="centered")

# 2. Advanced Mobile Layout CSS
st.markdown("""
    <style>
    /* Hide top padding & header menu */
    [data-testid="stHeader"] {display: none;}
    .block-container {padding-top: 1rem; padding-bottom: 2rem;}
    footer {display: none;}
    
    /* Clean Compact Title */
    .app-title {
        text-align: center;
        font-size: 1.6rem;
        font-weight: 800;
        color: #FFFFFF;
        margin-bottom: 15px;
    }
    
    /* Custom Responsive Native-looking Buttons */
    .btn-container {
        display: flex;
        gap: 10px;
        margin-bottom: 10px;
    }
    .custom-btn {
        flex: 1;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        font-size: 14px;
        color: white !important;
        text-decoration: none !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    .wa-bg { background-color: #25D366; }
    .fb-bg { background-color: #1877F2; }
    </style>
""", unsafe_allow_html=True)

# Main Header
st.markdown("<div class='app-title'>🛍️ AI Sales Assistant</div>", unsafe_allow_html=True)

# Side-by-Side Action Buttons
whatsapp_num = "923183705066"
wa_url = f"https://wa.me/{whatsapp_num}?text=Hello,%20I%20want%20to%20place%20an%20order."
fb_url = "https://facebook.com"

st.markdown(f"""
    <div class='btn-container'>
        <a href='{wa_url}' target='_blank' class='custom-btn wa-bg'>💬 WhatsApp</a>
        <a href='{fb_url}' target='_blank' class='custom-btn fb-bg'>🌐 Facebook</a>
    </div>
""", unsafe_allow_html=True)

st.divider()

# Setup Gemini API & Logic
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

voice_input = st.audio_input("🎤 Voice Question / بول کر سوال پوچھیں")
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
