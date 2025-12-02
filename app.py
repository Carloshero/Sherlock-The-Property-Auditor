import streamlit as st
import google.generativeai as genai

st.title("👨‍⚕️ Diagnóstico de Conexión")

# 1. Verificar versión de la librería
st.write(f"**Versión de la librería de Google:** `{genai.__version__}`")

# 2. Verificar API Key
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    st.success("✅ API Key encontrada en Secrets.")
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"❌ Error con la API Key: {e}")
    st.stop()

# 3. Listar modelos disponibles
st.write("---")
st.subheader("📋 Modelos disponibles para tu Clave:")
st.write("Consultando a Google... (esto puede tardar unos segundos)")

try:
    modelos = []
    for m in genai.list_models():
        # Filtramos solo los que sirven para generar contenido (chat)
        if 'generateContent' in m.supported_generation_methods:
            modelos.append(m.name)
            st.code(m.name) # Muestra el nombre exacto en pantalla
    
    if not modelos:
        st.error("⚠️ Tu API Key funciona, pero Google dice que NO tienes acceso a ningún modelo. ¿Creaste la clave en AI Studio o en Google Cloud?")
    else:
        st.balloons()
        st.success("¡Conexión exitosa! Copia uno de los nombres de arriba.")

except Exception as e:
    st.error(f"❌ Error fatal al conectar con Google: {e}")
