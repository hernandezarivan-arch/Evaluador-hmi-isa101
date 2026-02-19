import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuración de seguridad (se configura después en Streamlit Cloud)
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("⚠️ Falta configurar la 'GEMINI_API_KEY' en los Secrets de Streamlit.")

# --- TU RÚBRICA Y GUÍA OFICIAL INTEGRADA ---
SYSTEM_PROMPT = """
Actúa como el Profesor Iván Hernández, mentor de Mecatrónica en el Tec de Monterrey. 
Tu misión es evaluar HMI basándote en la "Guía de Diseño y Evaluación de Interfaces HMI (Nivel Inicial)".

PERSONALIDAD:
- Empático: Valida el esfuerzo del alumno antes de corregir.
- Mentor Directo: Explica el "porqué" técnico basado en ISA-101 y Guía Rockwell.
- Riguroso: Usa los niveles Destacado, Básico e Incipiente.

TABLA DE EVALUACIÓN (PESOS):
1. Filosofía (5%) | 2. Jerarquía (15%) | 3. Color/Fondo (15%) | 4. Alarmas (15%) | 5. Datos (10%) 
6. Claridad (10%) | 7. Tareas (10%) | 8. Proceso (5%) | 9. Iconos (5%) | 10. Navegación (10%)

REFERENCIAS A CITAR: ISA-101, Guía Rockwell y Presentación ISA.
"""

st.set_page_config(page_title="Evaluador HMI ISA-101", layout="wide", page_icon="🛡️")
st.title("🛡️ Evaluador HMI - Prof. Iván Hernández")
st.markdown("### Validación Técnica bajo Norma ANSI/ISA-101")

archivo = st.file_uploader("Sube la captura de tu HMI", type=["png", "jpg", "jpeg"])

if archivo:
    img = Image.open(archivo)
    st.image(img, caption="Diseño del Alumno", use_container_width=True)
    
    if st.button("🚀 Iniciar Evaluación Profesional"):
        with st.spinner("El Profe está analizando tu diseño..."):
            try:
                # Usamos el modelo Pro para máxima calidad de análisis visual
                model = genai.GenerativeModel('gemini-2.5-pro')
                response = model.generate_content([SYSTEM_PROMPT, img])
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Nota técnica: {e}")
