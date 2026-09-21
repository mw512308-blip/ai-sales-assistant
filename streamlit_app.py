import streamlit as st
from google import genai
from gtts import gTTS
import io

# Page Config
st.set_page_config(page_title="AI Sales Assistant", page_icon="🤖", layout="centered")

# Gemini API Initialization
GEMINI_API_KEY = "AQ.Ab8RN6K9JidgLgRtBansOlTim0qbCUN9bu_rC5E1r4dkRiz7iQ"
client = genai.Client(api_key=GEMINI_API_KEY)

# Pure Dark Glassmorphism CSS (Mobile Optimized)
st.markdown("""
<style>
    /* Force Pure Dark Background for Entire App */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #0b0f17 !important;
        background: linear-gradient(180deg, #0b0f17 0%, #05070a 100%) !important;
        color: #ffffff !important;
    }

    /* Hide Top Header & Streamlit Elements */
    header, footer, #MainMenu {visibility: hidden !important;}
    
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 5rem !important;
        max-width: 450px !important;
    }

    /* Header Text */
    .app-title {
        font-size: 26px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 4px;
    }
    .status-badge {
        color: #22c55e;
        font-size: 13px;
        font-weight: 500;
        margin-bottom: 18px;
    }

    /* Badges Layout */
    .badge-grid {
        display: flex;
        gap: 6px;
        margin-bottom: 20px;
    }
    .badge-item {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 6px 10px;
        font-size: 11px;
        color: #9ca3af;
        backdrop-filter: blur(10px);
    }

    /* Social Buttons */
    .btn-container {
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
    }
    .social-btn {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        padding: 10px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.12);
        background: rgba(255, 255, 255, 0.05);
        color: white !important;
        text-decoration: none;
        font-size: 13px;
        backdrop-filter: blur(10px);
    }

    /* Voice Card */
    .voice-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(212, 175, 55, 0.35);
        border-radius: 20px;
        padding: 14px 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 15px;
    }

    /* FIX STREAMLIT BOTTOM CHAT INPUT (Dark Glass Theme) */
    [data-testid="stBottom"], [data-testid="stChatInput"] {
        background-color: transparent !important;
        background: transparent !important;
    }
    
    [data-testid="stChatInput"] > div {
        background: rgba(255, 255, 255, 0.06) !important;
        border: 1px solid rgba(212, 175, 55, 0.4) !important;
        border-radius: 25px !important;
        backdrop-filter: blur(15px) !important;
        color: white !important;
    }
    
    [data-testid="stChatInput"] textarea {
        color: white !important;
    }
    
    /* Hide manage app button space */
    .viewerBadge_container__1S12D {display: none !important;}
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
        <div style="width: 36px; height: 36px; border-radius: 50%; background: rgba(212,175,55,0.15); border: 1px solid rgba(212,175,55,0.4); display: flex; align-items: center; justify-content: center;">🎙️</div>
        <div>
            <div style="font-weight: 600; font-size: 13px; color: #fff;">آواز سے سوال کریں / Record Voice</div>
            <div style="font-size: 11px; color: #9ca3af;">Tap to start speaking</div>
        </div>
    </div>
    <div style="font-size: 12px; color: #9ca3af; font-family: monospace;">00:00</div>
</div>
""", unsafe_allow_html=True)

# Chat Messages History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat Input & Gemini Logic
if prompt := st.chat_input("Sawal poochein / Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            reply = response.text
            st.write(reply)

            # Audio output
            tts = gTTS(text=reply, lang='ur')
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            st.audio(fp, format='audio/mp3')

            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"Error: {e}")
