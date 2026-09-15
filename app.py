import streamlit as st
import google.generativeai as genai
import json

# Page Config
st.set_page_config(
    page_title="AI Sales Assistant", 
    page_icon="🛍️", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# Light Mode Styling
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

# WhatsApp Button
whatsapp_num = "923183705066"
wa_url = f"https://wa.me/{whatsapp_num}?text=Hello,%20I%20want%20to%20place%20an%20order."
st.link_button("💬 Chat on WhatsApp", wa_url, use_container_width=True, type="primary")

st.divider()

# Secrets & API Setup
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ Secrets میں GEMINI_API_KEY موجود نہیں ہے۔")
    st.stop()

api_key = str(api_key).strip().replace('"', '').replace("'", "")
genai.configure(api_key=api_key)

try:
    with open("products.json", "r", encoding="utf-8") as f:
        products = json.load(f)
except Exception:
    products = []

system_prompt = f"You are an expert AI Sales Assistant for a store in Pakistan. Respond politely in Pashto, Roman Urdu, or English. Product inventory: {json.dumps(products)}. Store WhatsApp: 03183705066"

def get_response(user_input):
    models_to_try = ["models/gemini-1.5-flash", "models/gemini-1.5-pro", "gemini-1.5-flash", "gemini-pro"]
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name=model_name)
            full_prompt = f"{system_prompt}\n\nUser Question: {user_input}"
            res = model.generate_content(full_prompt)
            if res.text:
                return res.text
        except Exception:
            continue
    return "معذرت! اس وقت رابطہ قائم نہیں ہو پا رہا۔ براہ کرم تھوڑی دیر بعد کوشش کریں۔"

# Chat History Setup
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User Input
user_text = st.chat_input("Sawal poochein / Ask a question...")

if user_text:
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.write(user_text)

    with st.chat_message("assistant"):
        bot_reply = get_response(user_text)
        st.write(bot_reply)
        
        for product in products:
            if product.get("name", "").lower() in bot_reply.lower() or product.get("name", "").lower() in user_text.lower():
                if "image" in product:
                    st.image(product["image"], caption=f"{product['name']} - Rs. {product['price']}", width=250)
        
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
