import os
import streamlit as st
import pandas as pd
from datetime import datetime
import anthropic

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA E INTERFAZ
# ==========================================
st.set_page_config(
    page_title="SÓCRATES DIGITAL — Tutor Mayéutico", 
    page_icon="🏛️", 
    layout="wide"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .stApp {
        background-color: #E6E3FE;
    }
    .stButton>button {
        background-color: #D5DBCA !important;
        color: #00163A !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease-in-out !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.15) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Título Limpio
st.markdown("<h1 style='text-align: center; color: #00163A; font-size: 2.8rem; font-weight: 800; margin-bottom: 10px;'>SÓCRATES DIGITAL</h1>", unsafe_allow_html=True)

# Encabezado enmarcado: Templo | Subtítulo | Robot Grande
col_templo, col_texto, col_robot = st.columns([1, 4, 1])

with col_templo:
    if os.path.exists("templo.png"):
        st.image("templo.png", width=95)
    else:
        st.markdown("<h1 style='text-align: center;'>🏛</h1>", unsafe_allow_html=True)

with col_texto:
    st.markdown("""
        <p style='text-align: center; color: #00163A; font-size: 1.25rem; font-weight: 600; line-height: 1.4; margin-top: 15px;'>
            Tutor Mayéutico Inteligente — Desarrollo de Autonomía Cognitiva y Pensamiento Crítico
        </p>
    """, unsafe_allow_html=True)

with col_robot:
    if os.path.exists("robot_grande (1).png"):
        st.image("robot_grande (1).png", width=95)
    elif os.path.exists("robot_grande.png"):
        st.image("robot_grande.png", width=95)
    else:
        st.markdown("<h1 style='text-align: center;'>🤖</h1>", unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# GESTIÓN DE API KEY
# ==========================================
claude_api_key = st.secrets.get("ANTHROPIC_API_KEY", None)

# ==========================================
# 2. BARRA LATERAL (REGISTRO Y CONFIGURACIÓN)
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='color: #00163A; font-size: 1.3rem; font-weight: 700;'>👤 REGISTRO DEL ALUMNO</h2>", unsafe_allow_html=True)
    
    # Imagen de los estudiantes
    if os.path.exists("estudiantes_juntos.png"):
        col_side_left, col_side_img, col_side_right = st.columns([1, 4, 1])
        with col_side_img:
            st.image("estudiantes_juntos.png", width=180)
    else:
        st.markdown("<h1 style='text-align: center;'>👧👦</h1>", unsafe_allow_html=True)

    # Control de reseteo para limpiar inputs
    if "reset_count" not in st.session_state:
        st.session_state.reset_count = 0

    reset_id = st.session_state.reset_count

    nombre_alumno = st.text_input(
        "Nombre y Apellido *", 
        placeholder="Ej: Lucas Pérez o Sofía Gómez",
        key=f"input_nombre_{reset_id}"
    )
    curso_alumno = st.text_input(
        "Curso / División *", 
        placeholder="Ej: 5° A",
        key=f"input_curso_{reset_id}"
    )
    materia_tema = st.text_input(
        "Materia / Tema *", 
        placeholder="Ej: TIC / Analógico vs Digital",
        key=f"input_materia_{reset_id}"
    )
    
    if not claude_api_key:
        st.markdown("---")
        st.header("🔑 Configuración de API")
        claude_api_key = st.text_input("Claude API Key (sk-ant-...):", type="password")

    st.markdown("---")
    if st.button("🧹 Nuevo Alumno / Reiniciar Chat", use_container_width=True):
        st.session_state.clear()
        st.session_state.reset_count = reset_id + 1
        st.rerun()

    st.markdown("---")
    st.header("📊 Analítica y Trazabilidad")
    if "messages" in st.session_state:
        interacciones = len([m for m in st.session_state.messages if m["role"] == "user"])
        st.metric("Interacciones del Alumno", interacciones)
        
        if interacciones > 0:
            datos_chat = []
            for msg in st.session_state.messages:
                datos_chat.append({
                    "Fecha_Hora": msg.get("timestamp", ""),
                    "Alumno": nombre_alumno.strip(),
                    "Curso": curso_alumno.strip(),
                    "Materia": materia_tema.strip(),
                    "Rol": msg["role"],
                    "Fase_SOCRATICO": msg.get("fase", "S"),
                    "Mensaje": msg["content"]
                })
            
            df = pd.DataFrame(datos_chat)
            csv_data = df.to_csv(index=False).encode('utf-8')
            
            nombre_archivo = f"chat_{nombre_alumno.replace(' ', '_')}_{curso_alumno.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
            
            st.download_button(
                label="📥 Descargar Trazabilidad (CSV)",
                data=csv_data,
                file_name=nombre_archivo,
                mime="text/csv",
                use_container_width=True
            )

# Validar datos del alumno
campos_completos = bool(nombre_alumno.strip() and curso_
