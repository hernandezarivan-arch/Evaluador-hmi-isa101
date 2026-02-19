import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- SEGURIDAD: LLAVE DESDE SECRETS ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("⚠️ Falta configurar la 'GEMINI_API_KEY' en los Secrets de Streamlit.")

# --- PROMPT MAESTRO (VERSIÓN CIENTÍFICA FORMATIVA) ---
SYSTEM_PROMPT = """
Actúa como un Asesor Virtual experto en diseño de interfaces HMI de Alto Rendimiento (High Performance HMI).
Tu objetivo es proporcionar retroalimentación formativa a estudiantes universitarios de ingeniería para que iteren sus diseños.

REGLAS DE ESTILO E INTERACCIÓN:
1. Tono: Constructivo, académico y motivador. Eres una guía para la mejora, no un juez.
2. Formato: NO generes calificaciones numéricas. Asume buena intención si la imagen es ambigua.
3. Rigor: Basa tu análisis EXCLUSIVAMENTE en la siguiente guía maestra.

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
3. Tabla de Oportunidades de 4 columnas (Obligatorio respetar este formato): 
   | Criterio Evaluado | Observación del Diseño | Sugerencia de Mejora | Referencia Técnica |
   *Nota: En la columna "Referencia Técnica", escribe ÚNICAMENTE la cita exacta en negritas (ej. **ISA-101: 4.2** o **Rockwell: 18-20**).*
4. Conclusión con 3 pasos accionables concretos para la siguiente iteración.
"""

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Asesor Virtual HMI", layout="wide", page_icon="🤖")

# --- ESTILOS VISUALES (CSS) ---
st.markdown("""
    <style>
    /* Estilo para el botón principal */
    .stButton>button {
        background-color: #003366;
        color: white;
        font-size: 18px;
        border-radius: 8px;
        padding: 10px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #004d99;
        border-color: #004d99;
        color: white;
    }
    /* Estilo para títulos */
    .main-title {
        color: #003366;
        font-weight: 800;
        margin-bottom: 0px;
    }
    </style>
""", unsafe_allow_html=True)

# --- ENCABEZADO Y EXPLICACIÓN ---
st.markdown("<h1 class='main-title'>🤖 Asesor Virtual: Interfaces HMI</h1>", unsafe_allow_html=True)
st.markdown("#### Evaluación Formativa para Diseños de Alto Rendimiento (ANSI/ISA-101)")

# Layout en columnas para la cabecera
col_izq, col_der = st.columns([3, 2])

with col_izq:
    st.info("👋 **¡Bienvenido!** Sube una captura de tu interfaz. Este asesor analizará tu diseño gráfico basándose en estándares industriales reales para ayudarte a mejorar antes de tu entrega final.")
    archivo = st.file_uploader("📂 Selecciona o arrastra tu HMI (PNG, JPG)", type=["png", "jpg", "jpeg"])

with col_der:
    with st.expander("📚 Ver los 10 Criterios de Evaluación"):
        st.markdown("""
        **Tu diseño se contrastará contra estas métricas:**
        1. **Filosofía Visual** (Consistencia)
        2. **Jerarquía** (Navegación piramidal)
        3. **Color/Fondo** (Tonos neutros, color = alarmas)
        4. **Alarmas** (Triple codificación)
        5. **Datos** (Contexto y tendencias visuales)
        6. **Claridad Visual** (Diseño 2D, cero 3D)
        7. **Apoyo a Tareas** (Agrupación lógica)
        8. **Proceso** (Flujo coherente de tuberías)
        9. **Iconos** (Simbología geométrica y estándar)
        10. **Navegación** (Acceso rápido, sin laberintos)
        """)

st.divider()

# --- ÁREA DE ANÁLISIS ---
if archivo:
    # Centrar la imagen subida y el botón
    col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
    
    with col_img2:
        img = Image.open(archivo)
        st.image(img, caption="Vista Previa de tu Diseño", use_container_width=True)
        
        analizar = st.button("🚀 Iniciar Auditoría Formativa", use_container_width=True)

    # Procesamiento del reporte
    if analizar:
        st.markdown("<h3 style='text-align: center; color: #003366; margin-top: 20px;'>📋 Reporte de Retroalimentación</h3>", unsafe_allow_html=True)
        
        with st.spinner("Analizando componentes, jerarquías y consultando bibliografía técnica... ⏳"):
            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
                response = model.generate_content([SYSTEM_PROMPT, img])
                
                # Contenedor con borde para que parezca un reporte formal
                with st.container(border=True):
                    st.markdown(response.text)
                
                st.success("✅ Evaluación completada. Aplica estas sugerencias para tu próxima iteración.")
            except Exception as e:
                st.error(f"Nota técnica (Posible saturación de red): {e}")
