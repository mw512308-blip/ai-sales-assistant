import streamlit as st
import google.generativeai as genai
import json
from gtts import gTTS
import io

# 1. Page Configuration
st.set_page_config(page_title="AI Sales Assistant", page_icon="🛍️")
st.title("🛍️ AI Sales Assistant")

# 2. Setup Gemini API
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("API Key missing in Secrets!")
    st.stop()

genai.configure(api_key=api_key)

# 3. Load Products Data
try:
    with open("products.json", "r", encoding="utf-8") as f:
        products = json.load(f)
except Exception as e:
    products = []

# System Prompt
system_prompt = f"""
You are a helpful sales assistant.
Available products inventory: {json.dumps(products)}
Respond in English, Urdu, or Pashto based on customer input.
"""

model = genai.GenerativeModel(
    model_name="gemini-3.6-flash",
    system_instruction=system_prompt
)

# 4. Text-to-Speech Helper Function
def play_audio(text):
    try:
        tts = gTTS(text=text, lang='ur')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')
    except Exception:
        pass

# 5. Chat Memory Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Past Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 6. Inputs (Text & Voice)
user_text = st.chat_input("Sawal poochein / Ask a question...")
voice_input = st.audio_input("🎤 Record your voice / بول کر سوال پوچھیں")

prompt_to_send = None

if user_text:
    prompt_to_send = user_text
elif voice_input:
    prompt_to_send = "Voice message received."

# 7. Process Input with Error Handling
if prompt_to_send:
    st.session_state.messages.append({"role": "user", "content": prompt_to_send})
    with st.chat_message("user"):
        st.write(prompt_to_send)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt_to_send)
            bot_reply = response.text
        except Exception as e:
            bot_reply = "معذرت! اس وقت سسٹم پر بوجھ زیادہ ہے۔ براہ کرم 1 منٹ بعد دوبارہ کوشش کریں۔"
            
        st.write(bot_reply)
        
        # Play AI response as audio
        play_audio(bot_reply)
        
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
