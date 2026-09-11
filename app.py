import json
import os
from google import genai

# Setup Gemini Client
client = genai.Client(api_key="AQ.Ab8RN6I2XJP77tXBkvl4k-HIuPuXmce8j6kZ0YgcfQ2gQEQz5g")

# Load products from JSON
def load_products():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "products.json")
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# AI Sales Assistant Function
def ai_sales_assistant(user_message):
    products = load_products()
    
    prompt = f"""
    You are an AI Sales Assistant for a local SME in Pakistan.
    Respond naturally in Pashto, Roman Urdu, or English based on the user's input.
    Be polite, persuasive, and act as a professional sales assistant.
    
    Live inventory data:
    {json.dumps(products, indent=2)}
    
    Instructions:
    - ALWAYS mention the exact price (in PKR) and stock availability when asked.
    - Answer queries strictly based on inventory data.
    - Keep responses concise for WhatsApp.
    
    Customer message: {user_message}
    """

    # Model name updated exactly to gemini-3.6-flash
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )
    
    return response.text

# Main Loop
if __name__ == "__main__":
    print("==========================================")
    print(" Smart AI Sales Assistant Started! ")
    print(" (Type 'exit' to quit) ")
    print("==========================================")
    
    while True:
        user_input = input("\nCustomer: ")
        if user_input.lower() == "exit":
            break
        
        reply = ai_sales_assistant(user_input)
        print(f"\nAI Bot: {reply}")