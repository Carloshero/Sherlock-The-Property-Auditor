import streamlit as st
import google.generativeai as genai
from PIL import Image

# Page Configuration
st.set_page_config(page_title="Sherlock – Property Auditor", layout="wide")
st.title("🕵️‍♂️ Sherlock – The Property Auditor")

# 1. Secure API Key Configuration
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("⚠️ Error: API Key not found in Streamlit secrets.")
    st.stop()

# 2. System Instructions (Sherlock Persona)
system_instruction = """
You are an expert property auditor named Sherlock. 
Your task is to analyze property images to identify construction details, condition status, materials, and potential maintenance issues.
Always respond in English. Be professional, concise, and direct.
"""

# 3. Model Configuration (UPDATED to Gemini 2.5)
# ¡AQUÍ ESTABA EL ERROR! Ahora usamos el nombre exacto de tu lista:
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash", 
    system_instruction=system_instruction
)

# 4. Sidebar for Image Upload
with st.sidebar:
    st.header("📸 Upload Evidence")
    uploaded_file = st.file_uploader("Upload a property photo:", type=["jpg", "jpeg", "png"])
    
    image = None
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)
            st.success("Image ready for analysis.")
        except Exception as e:
            st.error("Error loading image. Please try another file.")

# 5. Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Chat Logic
if prompt := st.chat_input("Type your message here..."):
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate response
    try:
        # Prepare history
        history_history = [
            {"role": m["role"], "parts": [m["content"]]} 
            for m in st.session_state.messages[:-1]
        ]
        
        chat = model.start_chat(history=history_history)
        
        # Send message (with or without image)
        if image:
            response = chat.send_message([prompt, image])
        else:
            response = chat.send_message(prompt)
            
        text_response = response.text
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(text_response)
        st.session_state.messages.append({"role": "model", "content": text_response})
        
    except Exception as e:
        st.error(f"An error occurred: {e}")
