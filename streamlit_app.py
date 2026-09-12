import streamlit as st
import json
import os
import google.generativeai as genai

st.set_page_config(page_title="AI Sales Assistant", page_icon="🤖")
st.title("🤖 AI Sales Assistant")

# Secrets سے API Key حاصل کرنا
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API Key نہیں ملی! Streamlit Secrets چیک کریں۔")
    st.stop()

# API Key کنفیگر کرنا
genai.configure(api_key=api_key)

# پروڈکٹس ڈیٹا لوڈ کرنا
def load_products():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "products.json")
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return []

products = load_products()

system_instruction = f"""
You are a helpful multilingual sales assistant for local SMEs. 
You can speak English, Urdu, and Pashto fluently.
Here is our available product inventory: {json.dumps(products, ensure_ascii=False)}
Answer customer queries politely and guide them based on inventory.
"""

model = genai.GenerativeModel(
    model_name="gemini-3.6-flash",
    system_instruction=system_instruction
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Sawal poochein / Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = model.generate_content(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"ایرر: {e}")
