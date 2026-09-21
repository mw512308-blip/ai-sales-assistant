import streamlit as st
import os

# Page Config
st.set_page_config(page_title="AI Sales Assistant", page_icon="🤖", layout="centered")

# Custom UI Design CSS (Dark Glassmorphism UI)
st.markdown("""
<style>
    /* Dark Theme Background */
    .stApp {
        background-color: #0d1117;
        color: #ffffff;
    }
    
    /* Title & Status Styling */
    .title-text {
        font-size: 32px;
        font-weight: bold;
        color: #ffffff;
        margin-bottom: 2px;
    }
    .status-badge {
        color: #3fb950;
        font-size: 15px;
        font-weight: 500;
        margin-bottom: 20px;
    }
    
    /* Badges Styling */
    .badge-container {
        display: flex;
        gap: 10px;
        margin-bottom: 25px;
    }
    .badge {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 8px 14px;
        font-size: 13px;
        color: #c9d1d9;
        backdrop-filter: blur(10px);
    }

    /* Buttons Styling */
    .stButton > button {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 16px !important;
        color: white !important;
        font-weight: 500 !important;
        padding: 12px 20px !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        background: rgba(255, 255, 255, 0.18) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
    }

    /* Input & Voice Boxes */
    .glass-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 20px;
        padding: 16px;
        margin-top: 15px;
        backdrop-filter: blur(12px);
    }
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown('<div class="title-text">AI Sales Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="status-badge">🟢 Online • Always Ready</div>', unsafe_allow_html=True)

# Badges Section
st.markdown("""
<div class="badge-container">
    <div class="badge">🛡️ 24/7 AI Support</div>
    <div class="badge">🔒 SSL Secure</div>
    <div class="badge">📄 SOC 2</div>
</div>
""", unsafe_allow_html=True)

st.divider()

# Social Links
col1, col2 = st.columns(2)
with col1:
    st.link_button("💬 WhatsApp", "https://wa.me/", use_container_width=True)
with col2:
    st.link_button("📘 Facebook", "https://facebook.com", use_container_width=True)

# Voice Input Box Simulation
st.markdown("""
<div class="glass-card">
    <div style="display: flex; align-items: center; justify-content: space-between;">
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 20px;">🎙️</span>
            <div>
                <strong style="color: #fff;">آواز سے سوال کریں / Record Voice</strong><br>
                <small style="color: #8b949e;">Tap to start speaking</small>
            </div>
        </div>
        <span style="color: #8b949e;">00:00</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Chat Input Box
if prompt := st.chat_input("Sawal poochein / Ask a question..."):
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        st.write("آپ کا پیغام موصول ہو گیا ہے!")
