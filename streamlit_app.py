import json
import os
import streamlit as st
from google import genai

# Page Config
st.set_page_config(page_title="AI Sales Assistant", page_icon="🛍️", layout="centered")

st.title("🛍️ Smart AI Sales Assistant")
st.caption("Pakistani SMEs ke liye Pashto, Urdu, aur English AI Sales Agent")

# Setup Gemini Client
client = genai.Client(api_key="AQ.Ab8RN6I2XJP77tXBkvl4k-HIuPuXmce8j6kZ0YgcfQ2gQEQz5g")

# Load products from JSON
@st.cache_data
def load_products():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "products.json")
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

products = load_products()

# Sidebar - Live Inventory Display
st.sidebar.header("📦 Live Inventory Stock")
for item in products:
    st.sidebar.subheader(item.get('name', 'Product'))
    st.sidebar.write(f"💰 **Price:** PKR {item.get('price')}")
    st.sidebar.write(f"📊 **Stock:** {item.get('stock')} available")
    st.sidebar.divider()

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Customer Input
if user_input := st.chat_input("Sawal poochein / Ask a question..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Prompt Engineering for AI
    prompt = f"""
    You are an AI Sales Assistant for a local SME in Pakistan.
    Respond naturally in Pashto, Roman Urdu, or English based on the user's input.
    Be polite, persuasive, and act as a professional sales assistant.
    
    Live inventory data:
    {json.dumps(products, indent=2)}
    
    Instructions:
    - ALWAYS mention the exact price (in PKR) and stock availability when asked.
    - Answer queries strictly based on inventory data.
    - Keep responses professional and engaging.
    
    Customer message: {user_input}
    """

    # Generate response
    with st.spinner("AI Bot jawab likh raha hai..."):
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )
        bot_reply = response.text

    # Display bot response
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)