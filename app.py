import streamlit as st
from google import genai
import json

# Safely handle gTTS
try:
    from gTTS import gTTS
    import io
    gtts_available = True
except Exception:
    gtts_available = False

# 1. Page Config
st.set_page_config(
    page_title="AI Sales Assistant", 
    page_icon="🛍️", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# 2. Strict Light Mode Styling
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    :root { color-scheme: light !important; }
    [data-testid="stHeader"], footer {display: none;}
    p, span, label, div, h1, h2, h3, .stMarkdown, [data-testid="stChatMessage"] {
        color: #000000 !important;
    }
    input, textarea {
        color: #000000 !important;
        background-color: #f8fafc !important;
        border: 1px solid #cbd5e1 !important;
    }
    .header-box {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        margin-bottom: 15px;
    }
    .app-title {
        font-size: 1.8rem;
        font-weight: 800;
        color: #0284c7 !important;
    }
    .status-tag {
        font-size: 0.85rem;
        color: #16a34a !important;
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

# WhatsApp Integration Button
whatsapp_num = "923183705066"
wa_url = f"https://wa.me/{whatsapp_num}?text=Hello,%20I%20want%20to%20place%20an%20order."
st.link_button("💬 Chat on WhatsApp", wa_url, use_container_width=True, type="primary")

st.divider()

# Get Key & Setup Client
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ Secrets میں GEMINI_API_KEY موجود نہیں ہے۔")
    st.stop()

api_key = str(api_key).strip().replace('"', '').replace("'", "")

try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"API Client Setup Error: {e}")

try:
    with open("products.json", "r", encoding="utf-8") as f:
        products = json.load(f)
except Exception:
    products = []

system_prompt = f"You are an expert AI Sales Assistant for a store in Pakistan. Respond politely in Pashto, Roman Urdu, or English. Product inventory: {json.dumps(products)}. Store WhatsApp: 03183705066"

# New Google GenAI SDK Method
def get_response(user_input):
    models_to_try = ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-2.0-flash"]
    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=f"{system_prompt}\n\nUser Question: {user_input}"
            )
            if response.text:
                return response.text
        except Exception:
            continue
    return "معذرت! اس وقت رابطہ قائم نہیں ہو پا رہا۔ براہ کرم تھوڑی دیر بعد کوشش کریں۔"

def play_audio(text):
    if gtts_available:
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

# Voice & Text Inputs
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
        
        # Display product image if found
        for product in products:
            if product.get("name", "").lower() in bot_reply.lower() or product.get("name", "").lower() in prompt_to_send.lower():
                if "image" in product:
                    st.image(product["image"], caption=f"{product['name']} - Rs. {product['price']}", width=250)
        
        play_audio(bot_reply)
        
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
