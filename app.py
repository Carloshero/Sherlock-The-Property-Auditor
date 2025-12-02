import streamlit as st
import google.generativeai as genai

# Configuración de la página (Título y diseño)
st.set_page_config(page_title="Sherlock — The Property Auditor By AgentCoachAi", layout="wide")

# Título visible en la pantalla
st.title("Sherlock — The Property Auditor By AgentCoachAi")

# 1. Configuración de la API Key (La tomamos de los secretos de Streamlit para seguridad)
# Si estás probando en tu PC local, asegúrate de tener tu API Key a mano.
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    # Esto es solo para que no de error si no has configurado la clave aún
    st.error("⚠️ Falta la API Key. Configúrala en los secretos de Streamlit.")
    st.stop()

genai.configure(api_key=api_key)

# 2. Inicializar el modelo
# PEGA AQUÍ LAS INSTRUCCIONES DE TU GEM ENTRE LAS COMILLAS TRIPLES
instrucciones_del_sistema = """
Analyzes property photos to estimate repair costs, spot red flags, and calculate ROI.
"""


model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=instrucciones_del_sistema
)

# 3. Guardar el historial del chat (para que recuerde lo que hablan)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Mostrar mensajes anteriores en la pantalla
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Caja de entrada de texto (El chat)
if prompt := st.chat_input("To get started, upload any room or area, to get cost estimates to share with the homeowner."):
    # Mostrar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(prompt)
    # Guardar en historial
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generar respuesta de Gemini
    try:
        # Preparamos el historial para enviarlo a Gemini
        chat = model.start_chat(history=[
            {"role": m["role"], "parts": [m["content"]]} 
            for m in st.session_state.messages[:-1] # Excluir el último para no duplicar
        ])
        
        response = chat.send_message(prompt)
        text_response = response.text
        
        # Mostrar respuesta del asistente
        with st.chat_message("assistant"):
            st.markdown(text_response)
        
        # Guardar respuesta en historial
        st.session_state.messages.append({"role": "model", "content": text_response})
        
    except Exception as e:

        st.error(f"Ocurrió un error: {e}")




