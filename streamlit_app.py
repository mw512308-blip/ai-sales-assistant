import streamlit as st
from google import genai
from gtts import gTTS
import io

# Page Config (Centered view for mobile card look)
st.set_page_config(page_title="AI Sales Assistant", page_icon="🤖", layout="centered")

# Gemini API Initialization
GEMINI_API_KEY = "AQ.Ab8RN6K9JidgLgRtBansOlTim0qbCUN9bu_rC5E1r4dkRiz7iQ"
client = genai.Client(api_key=GEMINI_API_KEY)

# Custom High-End Mobile Glassmorphism CSS
st.markdown("""
<style>
    /* Dark Aesthetic Background */
    .stApp {
        background: linear-gradient(135deg, #0b0f19 0%, #111827 50%, #080b11 100%);
        color: #ffffff;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* Hide Default Headers */
    header, footer {visibility: hidden;}
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 480px !important;
    }

    /* Main Title */
    .app-title {
        font-size: 28px;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.5px;
        margin-bottom: 2px;
    }
    .status-badge {
        color: #22c55e;
        font-size: 14px;
        font-weight: 500;
        margin-bottom: 20px;
    }

    /* Badges Layout */
    .badge-grid {
        display: flex;
        gap: 8px;
        margin-bottom: 25px;
    }
    .badge-item {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 8px 12px;
        font-size: 12px;
        color: #9ca3af;
        backdrop-filter: blur(12px);
        display: flex;
        align-items: center;
        gap: 5px;
    }

    /* Custom Social Buttons */
    .btn-container {
        display: flex;
        gap: 12px;
        margin-bottom: 25px;
    }
    .social-btn {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        padding: 12px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.12);
        background: rgba(255, 255, 255, 0.06);
        color: white;
        text-decoration: none;
        font-weight: 500;
        font-size: 14px;
        backdrop-filter: blur(16px);
        transition: all 0.2s ease;
    }
    .social-btn:hover {
        background: rgba(255, 255, 255, 0.12);
        border-color: rgba(255, 255, 255, 0.25);
    }

    /* Voice Recording Glass Box */
    .voice-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 24px;
        padding: 16px 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 20px;
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    .mic-icon-circle {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: rgba(212, 175, 55, 0.15);
        border: 1px solid rgba(212, 175, 55, 0.4);
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* Custom Input Box Styling */
    .stChatInput > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 30px !important;
        backdrop-filter: blur(20px) !important;
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

# Voice Recording UI Box
st.markdown("""
<div class="voice-card">
    <div style="display: flex; align-items: center; gap: 14px;">
        <div class="mic-icon-circle">🎙️</div>
        <div>
            <div style="font-weight: 600; font-size: 14px; color: #fff;">آواز سے سوال کریں / Record Voice</div>
            <div style="font-size: 12px; color: #9ca3af;">Tap to start speaking</div>
        </div>
    </div>
    <div style="font-size: 13px; color: #9ca3af; font-family: monospace;">00:00</div>
</div>
""", unsafe_allow_html=True)

# Chat Messages Display
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat Input & Logic
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
