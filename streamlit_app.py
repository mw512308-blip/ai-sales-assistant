import streamlit as st
from google import genai
from gtts import gTTS
import io

# Page Config
st.set_page_config(page_title="AI Sales Assistant", page_icon="🤖", layout="centered")

# Gemini API Initialization
GEMINI_API_KEY = "AQ.Ab8RN6K9JidgLgRtBansOlTim0qbCUN9bu_rC5E1r4dkRiz7iQ"
client = genai.Client(api_key=GEMINI_API_KEY)

# Exact Mobile Glassmorphism Theme CSS
st.markdown("""
<style>
    /* Dark Aesthetic Background */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #0b0f17 !important;
        background: linear-gradient(180deg, #0f141c 0%, #080a0f 100%) !important;
        color: #ffffff !important;
    }

    /* Hide Top Header & Streamlit Padding */
    header, footer, #MainMenu {visibility: hidden !important;}
    
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 420px !important;
    }

    /* Header Text */
    .app-title {
        font-size: 28px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 2px;
    }
    .status-badge {
        color: #22c55e;
        font-size: 13px;
        font-weight: 500;
        margin-bottom: 22px;
    }

    /* Badges Layout */
    .badge-grid {
        display: flex;
        gap: 8px;
        margin-bottom: 22px;
    }
    .badge-item {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 8px 12px;
        font-size: 12px;
        color: #9ca3af;
        backdrop-filter: blur(10px);
    }

    /* Social Buttons */
    .btn-container {
        display: flex;
        gap: 12px;
        margin-bottom: 22px;
    }
    .social-btn {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        padding: 12px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        background: rgba(255, 255, 255, 0.05);
        color: white !important;
        text-decoration: none;
        font-size: 14px;
        font-weight: 500;
        backdrop-filter: blur(10px);
    }

    /* Voice Recording Box */
    .voice-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(212, 175, 55, 0.4);
        border-radius: 24px;
        padding: 14px 18px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 25px;
    }

    /* Streamlit Input Fixes */
    .stTextInput > div > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(212, 175, 55, 0.4) !important;
        border-radius: 25px !important;
        color: white !important;
    }
    
    .stTextInput input {
        color: white !important;
    }
    
    .stButton button {
        background: rgba(212, 175, 55, 0.2) !important;
        border: 1px solid rgba(212, 175, 55, 0.5) !important;
        color: white !important;
        border-radius: 50% !important;
        height: 42px !important;
        width: 42px !important;
    }
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown('<div class="app-title">AI Sales Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="status-badge">🟢 Online • Always Ready</div>', unsafe_allow_html=True)

# Trust Badges
st.markdown("""
<div class="badge-grid">
    <div class="badge-item">🛡️ 24/7 AI Support</div>
    <div class="badge-item">🔒 SSL Secure</div>
    <div class="badge-item">📄 SOC 2</div>
</div>
""", unsafe_allow_html=True)

# Social Links
st.markdown("""
<div class="btn-container">
    <a href="https://wa.me/" target="_blank" class="social-btn">
        <span style="color: #25D366;">💬</span> WhatsApp
    </a>
    <a href="https://facebook.com" target="_blank" class="social-btn">
        <span style="color: #1877F2;">📘</span> Facebook
    </a>
</div>
""", unsafe_allow_html=True)

# Voice Recording Box
st.markdown("""
<div class="voice-card">
    <div style="display: flex; align-items: center; gap: 12px;">
        <div style="width: 38px; height: 38px; border-radius: 50%; background: rgba(212,175,55,0.15); border: 1px solid rgba(212,175,55,0.4); display: flex; align-items: center; justify-content: center;">🎙️</div>
        <div>
            <div style="font-weight: 600; font-size: 13px; color: #fff;">آواز سے سوال کریں / Record Voice</div>
            <div style="font-size: 11px; color: #9ca3af;">Tap to start speaking</div>
        </div>
    </div>
    <div style="font-size: 12px; color: #9ca3af; font-family: monospace;">00:00</div>
</div>
""", unsafe_allow_html=True)

# Chat Form (Inside Dark Container)
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input("", placeholder="Sawal poochein / Ask a question...", label_visibility="collapsed")
    with col2:
        submit = st.form_submit_button("➔")

if submit and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_input,
        )
        reply = response.text
        st.session_state.messages.append({"role": "assistant", "content": reply})

        # Voice Audio Generation
        tts = gTTS(text=reply, lang='ur')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')

        st.rerun()
    except Exception as e:
        st.error(f"Error: {e}")
