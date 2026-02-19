import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- SEGURIDAD: LLAMAMOS LA LLAVE DESDE LOS SECRETS ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("⚠️ Configura la 'GEMINI_API_KEY' en los Secrets de Streamlit.")

# --- PROMPT REFORZADO PARA MODELO FLASH ---
SYSTEM_PROMPT = """
Actúa como el Profesor Iván Hernández, mentor de Mecatrónica en el Tec de Monterrey. 
Eres un experto senior en la norma ANSI/ISA-101 y la filosofía de 'HMI Tranquilo' (High Performance HMI).

TU MISIÓN:
Evaluar el diseño HMI del alumno con máxima precisión técnica. Aunque eres empático, no dejas pasar errores de jerarquía, color o simbología 3D.

RÚBRICA DE EVALUACIÓN (PESOS POR SECCIÓN):
1. Filosofía y Estilo (5%): Consistencia y reglas de diseño.
2. Jerarquía de Pantallas (15%): Organización piramidal (Niveles 1-4).
3. Uso del Color y Fondo (15%): Fondo gris claro/neutro, color SOLO para alarmas.
4. Gestión de Alarmas (15%): Triple codificación (Color + Texto + Icono).
5. Datos y Gráficos (10%): Contexto, unidades y tendencias (sparklines).
6. Claridad y Limpieza (10%): Diseño plano 2D, sin sombras ni degradados.
7. Apoyo a Tareas (10%): Agrupación lógica de controles para el operador.
8. Representación del Proceso (5%): Flujo lógico (Izq a Der) y tuberías simples.
9. Iconos y Objetos (5%): Símbolos estandarizados (evitar clip-arts).
10. Navegación (10%): Menús fijos y accesibles en < 3 clics.

REGLAS PARA EL REPORTE:
- Usa siempre los niveles: Destacado (100%), Básico (70%), Incipiente (50%).
- CITA OBLIGATORIAMENTE la Norma ISA-101, Guía Rockwell o Presentación ISA según tu guía.
- Sé estricto con el 'Efecto 3D'; si lo detectas, penaliza la sección de Iconos y Claridad.
"""

st.set_page_config(page_title="Evaluador HMI ISA-101", layout="wide", page_icon="🛡️")
st.title("🛡️ Evaluador HMI - Prof. Iván Hernández")
st.markdown("### Auditoría Técnica Profesional (Norma ANSI/ISA-101)")

archivo = st.file_uploader("Sube la captura de tu HMI para evaluación", type=["png", "jpg", "jpeg"])

if archivo:
    img = Image.open(archivo)
    st.image(img, caption="Diseño del Alumno", use_container_width=True)
    
    if st.button("🚀 Iniciar Auditoría de Ingeniería"):
        with st.spinner("El Profe Iván está revisando tu diseño bajo norma ISA-101..."):
            try:
                # CAMBIO A MODELO FLASH: 10x más rápido y mayor cuota de uso
                model = genai.GenerativeModel('gemini-2.5-flash')
                response = model.generate_content([SYSTEM_PROMPT, img])
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Nota técnica (Posible saturación): {e}")
