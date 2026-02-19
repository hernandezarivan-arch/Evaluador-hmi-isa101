import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- SEGURIDAD: LLAVE DESDE SECRETS ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("⚠️ Falta configurar la 'GEMINI_API_KEY' en los Secrets de Streamlit.")

# --- PROMPT REFINADO (ESTILO IVÁN HERNÁNDEZ) ---
SYSTEM_PROMPT = """
Actúa como el Profesor Iván Hernández, mentor de Mecatrónica en el Tec de Monterrey. 
Tu misión es realizar una auditoría técnica de interfaces HMI bajo la norma ANSI/ISA-101.

REGLAS DE ESTILO:
1. Ve directo al análisis técnico, pero mantén la calidez de un profesor.
2. Usa exclusivamente el término "HMI de Alto Rendimiento" (High Performance HMI).
3. Sé riguroso pero actúa como mentor: explica siempre el porqué técnico de cada fallo.

ESTRUCTURA DEL REPORTE:
1. Saludo amable y motivador (ej. "¡Estimado estudiante!" o "¡Hola, futuro ingeniero!"), validando su esfuerzo y resaltando un acierto técnico real del diseño.
2. Tabla de Evaluación: | Criterio (Peso) | Nivel | Observación y Referencia Técnica |.
   Niveles a usar: Destacado (100%), Básico (70%), Incipiente (50%).
3. CALIFICACIÓN FINAL: Suma ponderada exacta de los 10 criterios, mostrada sobre 100 puntos.
4. 3 Pasos prioritarios, claros y directos para el rediseño.

BIBLIOGRAFÍA PARA REFERENCIAS: 
- Norma ISA-101.01-2015.
- Guía de Diseño HMI de Rockwell Automation.
- Presentación ISA sobre HMI de Alto Rendimiento.

CRITERIOS Y PESOS: 
1. Filosofía (5%) | 2. Jerarquía (15%) | 3. Color y Fondo (15%) | 4. Alarmas (15%) | 5. Datos y Gráficos (10%) | 6. Claridad Visual (10%) | 7. Apoyo a Tareas (10%) | 8. Representación del Proceso (5%) | 9. Iconos y Objetos (5%) | 10. Navegación (10%).
"""

st.set_page_config(page_title="Evaluador HMI ISA-101", layout="wide", page_icon="🛡️")
st.title("🛡️ Evaluador HMI - Prof. Iván Hernández")
st.markdown("### Auditoría Técnica Profesional (ANSI/ISA-101)")

archivo = st.file_uploader("Sube la captura de tu HMI", type=["png", "jpg", "jpeg"])

if archivo:
    img = Image.open(archivo)
    st.image(img, caption="Diseño del Alumno", use_container_width=True)
    
    if st.button("🚀 Iniciar Auditoría"):
        with st.spinner("Analizando bajo estándares industriales..."):
            try:
                # Motor Flash para máxima velocidad y evitar cuotas excedidas en clase
                model = genai.GenerativeModel('gemini-2.5-flash')
                response = model.generate_content([SYSTEM_PROMPT, img])
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Nota técnica: {e}")
