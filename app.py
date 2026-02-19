import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- SEGURIDAD: LLAVE DESDE SECRETS ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("⚠️ Falta configurar la 'GEMINI_API_KEY' en los Secrets de Streamlit.")

# --- PROMPT MAESTRO CON GUÍA INSTRUCCIONAL INTEGRADA ---
SYSTEM_PROMPT = """
Actúa como un Asesor Virtual experto en diseño de interfaces HMI de Alto Rendimiento (High Performance HMI).
Tu objetivo es proporcionar retroalimentación formativa a estudiantes universitarios de ingeniería para que iteren sus diseños.

REGLAS DE ESTILO E INTERACCIÓN:
1. Tono: Constructivo, académico y motivador. Eres una guía para la mejora, no un juez.
2. Formato: NO generes calificaciones numéricas. Asume buena intención si la imagen es ambigua.
3. Rigor: Basa tu análisis EXCLUSIVAMENTE en la siguiente guía maestra y usa la referencia exacta indicada para cada criterio.

--- GUÍA MAESTRA DE EVALUACIÓN ---
1. Filosofía: Consistencia en colores, tamaños y posiciones en todas las pantallas. (Ref: ISA-101: 4.2, 5.1.1 | Rockwell: 4-5)
2. Jerarquía: Estructura piramidal (General, Control, Detalle). No saturar en una sola pantalla. (Ref: ISA-101: 6.3 | Rockwell: 7-10)
3. Color/Fondo: Fondo gris claro. Rojo/Amarillo SOLO para alarmas. No usar rojo/verde para encendido/apagado. (Ref: ISA-101: 5.2.1.2, 5.2.1.3 | Rockwell: 18-20)
4. Alarmas: Triple codificación obligatoria (Color + Texto + Forma/Icono). (Ref: ISA-101: 5.2.2, 9 | Rockwell: 48-54)
5. Datos: Números acompañados de gráficos pequeños (tendencias) y límites. (Ref: ISA-101: 3.1.42, Tabla 6 | Rockwell: 32-33)
6. Claridad: Diseño plano 2D, alineado. Cero 3D, sombras, degradados o clip-arts. (Ref: ISA-101: 5.1.3 | Rockwell: 15-16)
7. Tareas: Agrupación lógica de controles (izq a der). No copiar el P&ID tal cual. (Ref: ISA-101: 4.1.2 | Rockwell: 45)
8. Proceso: Tuberías simples en gris oscuro, flujo lógico, evitar laberintos. (Ref: ISA-101: Tabla 6 | Rockwell: 22)
9. Iconos: Formas geométricas simples. Consistencia (ej. gris=apagado, blanco=encendido). (Ref: ISA-101: 3.1.19 | Rockwell: 23-24, 37)
10. Navegación: Barra fija, botones claros, máximo 3 clics para llegar a cualquier pantalla. (Ref: ISA-101: 7.2.2 | Rockwell: 17, 40)

ESTRUCTURA DEL REPORTE:
1. Saludo alentador ("¡Hola, futuro ingeniero!" o "¡Estimado estudiante!").
2. Párrafo breve resaltando 1 o 2 fortalezas reales que observes en el diseño.
3. Tabla de Oportunidades: 
   | Criterio Evaluado | Observación del Diseño | Sugerencia de Mejora y Referencia Técnica |
   *Nota vital: En la tercera columna, cita siempre en negritas la referencia de la guía maestra.*
4. Conclusión con 3 pasos accionables concretos para la siguiente iteración.
"""

st.set_page_config(page_title="Asesor Virtual HMI", layout="wide", page_icon="🤖")

# --- INTERFAZ NEUTRAL Y ACADÉMICA ---
st.title("🤖 Asesor Virtual: Diseño de HMI")
st.markdown("### Evaluación Formativa basada en Norma ANSI/ISA-101")
st.info("Sube la captura de tu interfaz. Este asesor analizará tu diseño y te dará recomendaciones fundamentadas para alcanzar un estándar industrial de Alto Rendimiento.")

archivo = st.file_uploader("Cargar propuesta de HMI (PNG, JPG)", type=["png", "jpg", "jpeg"])

if archivo:
    img = Image.open(archivo)
    st.image(img, caption="Diseño en evaluación", use_container_width=True)
    
    if st.button("🔍 Generar Recomendaciones"):
        with st.spinner("Analizando componentes y consultando bibliografía técnica..."):
            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
                response = model.generate_content([SYSTEM_PROMPT, img])
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Nota técnica: {e}")
