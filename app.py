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

# Estilos CSS para replicar la estética exacta
st.markdown("""
    <style>
    .stApp {
        background-color: #E6E3FE;
    }
    .stButton>button {
        background-color: #D5DBCA !important;
        color: #00163A !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 8px 16px !important;
        transition: all 0.2s ease !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1) !important;
    }
    div[data-testid="stSidebar"] {
        background-color: #FFD8D1 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Título Limpio (sin íconos pegados antes del texto)
st.markdown("<h1 style='text-align: center; color: #00163A; font-size: 3rem; font-weight: 800; margin-bottom: 20px;'>SÓCRATES DIGITAL</h1>", unsafe_allow_html=True)

# Encabezado enmarcado: Templo a la izquierda | Subtítulo | Robot a la derecha
col_templo, col_texto, col_robot = st.columns([1.5, 5, 1.5])

with col_templo:
    # Ilustración Templo Clásico
    st.markdown("""
        <div style="text-align: center;">
            <svg width="110" height="90" viewBox="0 0 120 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M60 10 L10 35 L110 35 Z" fill="#E2D4C9" stroke="#333" stroke-width="3"/>
                <rect x="15" y="35" width="90" height="10" fill="#C5B4A5" stroke="#333" stroke-width="3"/>
                <rect x="22" y="45" width="10" height="40" fill="#FFF" stroke="#333" stroke-width="2.5"/>
                <rect x="42" y="45" width="10" height="40" fill="#FFF" stroke="#333" stroke-width="2.5"/>
                <rect x="68" y="45" width="10" height="40" fill="#FFF" stroke="#333" stroke-width="2.5"/>
                <rect x="88" y="45" width="10" height="40" fill="#FFF" stroke="#333" stroke-width="2.5"/>
                <rect x="10" y="85" width="100" height="10" fill="#C5B4A5" stroke="#333" stroke-width="3"/>
            </svg>
        </div>
    """, unsafe_allow_html=True)

with col_texto:
    st.markdown("""
        <div style="display: flex; align-items: center; justify-content: center; height: 100%;">
            <p style='text-align: center; color: #00163A; font-size: 1.35rem; font-weight: 600; line-height: 1.3; margin: 0;'>
                Tutor Mayéutico Inteligente — Desarrollo de Autonomía Cognitiva y Pensamiento Crítico
            </p>
        </div>
    """, unsafe_allow_html=True)

with col_robot:
    # Ilustración Cabeza de Robot
    st.markdown("""
        <div style="text-align: center;">
            <svg width="100" height="90" viewBox="0 0 120 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="25" y="25" width="70" height="55" rx="18" fill="#D2EBF7" stroke="#1A2B4C" stroke-width="3.5"/>
                <rect x="33" y="33" width="54" height="38" rx="12" fill="#1B3B5A" stroke="#1A2B4C" stroke-width="2"/>
                <circle cx="48" cy="52" r="8" fill="#42C3D8" stroke="#FFF" stroke-width="2"/>
                <circle cx="72" cy="52" r="8" fill="#42C3D8" stroke="#FFF" stroke-width="2"/>
                <circle cx="49" cy="50" r="3" fill="#FFF"/>
                <circle cx="73" cy="50" r="3" fill="#FFF"/>
                <path d="M12 45 L25 45 M95 45 L108 45" stroke="#1A2B4C" stroke-width="4" stroke-linecap="round"/>
                <circle cx="10" cy="45" r="4" fill="#FF9EAA"/>
                <circle cx="110" cy="45" r="4" fill="#FF9EAA"/>
                <line x1="60" y1="25" x2="60" y2="12" stroke="#1A2B4C" stroke-width="3"/>
                <circle cx="60" cy="9" r="5" fill="#FF9EAA" stroke="#1A2B4C" stroke-width="2"/>
            </svg>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='margin-top: 15px; margin-bottom: 25px; border-color: #C0B2EC;'>", unsafe_allow_html=True)

# ==========================================
# GESTIÓN DE API KEY (SECRETS O MANUAL)
# ==========================================
claude_api_key = st.secrets.get("ANTHROPIC_API_KEY", None)

# ==========================================
# 2. BARRA LATERAL (REGISTRO Y CONFIGURACIÓN)
# ==========================================
with st.sidebar:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 15px;">
            <span style="font-size: 1.2rem;">👤</span>
            <h3 style="color: #00163A; font-size: 1.1rem; font-weight: 700; margin: 0;">REGISTRO DEL ALUMNO</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Ilustración Niña y Niño Estudiantes
    st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <svg width="190" height="110" viewBox="0 0 200 120" fill="none" xmlns="http://www.w3.org/2000/svg">
                <!-- Niña -->
                <path d="M25 42 C 20 20, 65 20, 60 42 C 60 70, 25 70, 25 42" fill="#5C2719"/>
                <circle cx="42" cy="45" r="16" fill="#FCE0D8"/>
                <path d="M28 40 Q 42 48 56 40 Q 42 32 28 40" fill="#5C2719"/>
                <circle cx="37" cy="45" r="2" fill="#333"/>
                <circle cx="47" cy="45" r="2" fill="#333"/>
                <path d="M40 52 Q 42 55 44 52" stroke="#333" stroke-width="1.5"/>
                <path d="M25 65 L60 65 L65 110 L20 110 Z" fill="#E86A75"/>
                <rect x="18" y="72" width="10" height="28" rx="4" fill="#D94B58"/>
                <!-- Niño -->
                <path d="M132 28 C 130 18, 170 18, 168 28" stroke="#3D2314" stroke-width="12" stroke-linecap="round"/>
                <circle cx="150" cy="45" r="16" fill="#FCE0D8"/>
                <circle cx="145" cy="45" r="2" fill="#333"/>
                <circle cx="155" cy="45" r="2" fill="#333"/>
                <path d="M148 52 Q 150 55 152 52" stroke="#333" stroke-width="1.5"/>
                <path d="M130 65 L170 65 L175 110 L125 110 Z" fill="#4DAA98"/>
                <rect x="142" y="70" width="18" height="24" rx="2" fill="#E86A75" stroke="#333" stroke-width="1.5"/>
            </svg>
        </div>
    """, unsafe_allow_html=True)

    nombre_alumno = st.text_input("Nombre y Apellido *", placeholder="")
    curso_alumno = st.text_input("Curso / División *", placeholder="")
    materia_tema = st.text_input("Materia / Tema *", placeholder="")
    
    if not claude_api_key:
        st.markdown("---")
        st.header("🔑 Configuración de API")
        claude_api_key = st.text_input("Claude API Key (sk-ant-...):", type="password")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Nuevo Alumno / Reiniciar Chat", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Enviar", use_container_width=True):
        pass

    st.markdown("<br>", unsafe_allow_html=True)
    if "messages" in st.session_state:
        interacciones = len([m for m in st.session_state.messages if m["role"] == "user"])
        
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
campos_completos = bool(nombre_alumno.strip() and curso_alumno.strip() and materia_tema.strip())

if not campos_completos:
    st.warning("👈 **Atención:** Para comenzar la sesión de aprendizaje, completá obligatoriamente tu **Nombre, Curso y Materia** en el panel lateral.")
    st.stop()

primer_nombre = nombre_alumno.strip().split()[0]

# ==========================================
# 3. MOTOR SOCRÁTICO (SYSTEM PROMPT)
# ==========================================
SYSTEM_PROMPT = f"""
Actúas estrictamente como "Sócrates Digital", un tutor virtual mayéutico especializado en el desarrollo del pensamiento crítico y la autonomía cognitiva para estudiantes de educación secundaria (16 a 18 años). Hablás con tu alumno {primer_nombre} (Curso: {curso_alumno}, Materia: {materia_tema}).

PRINCIPIOS GENERALES Y RIGOR PEDAGÓGICO:
1. RIGOR CONCEPTUAL BASE:
   - LO ANALÓGICO ES CONTINUO Y SIN SALTOS.
   - LO DIGITAL ES DISCRETO Y A SALTOS POR PASOS O NÚMEROS.
2. ALGORITMO MAYÉUTICO Y ANDAMIAJE:
   - Prohibido entregar definiciones servidas de entrada.
3. ESTRUCTURA Y FORMATO DE MENSAJE:
   - Mantené un tono cercano y sintético (máximo 2 a 3 oraciones).
   - Formulá ÚNICAMENTE UNA pregunta al final.
"""

mensaje_bienvenida_unico = f"¡Hey, {primer_nombre}! Soy Sócrates Digital... ¡porque tu tutor Mayéutico está presente! 🤔"

if "messages" not in st.session_state or st.session_state.get("current_student") != primer_nombre:
    st.session_state.current_student = primer_nombre
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": mensaje_bienvenida_unico,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "fase": "S"
        }
    ]

# Avatar del Robot para el chat
avatar_robot_svg = """data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="45" fill="%23D2EBF7" stroke="%231A2B4C" stroke-width="4"/><rect x="25" y="30" width="50" height="40" rx="8" fill="%231B3B5A"/><circle cx="40" cy="48" r="6" fill="%2342C3D8"/><circle cx="60" cy="48" r="6" fill="%2342C3D8"/></svg>"""

for msg in st.session_state.messages:
    avatar_choice = avatar_robot_svg if msg["role"] == "assistant" else "👦"
    with st.chat_message(msg["role"], avatar=avatar_choice):
        st.write(msg["content"])

if user_input := st.chat_input("Escribí tu respuesta o duda aquí..."):
    if not claude_api_key:
        st.error("⚠️ Falta configurar la API Key de Claude.")
        st.stop()
        
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    num_user_msgs = len([m for m in st.session_state.messages if m["role"] == "user"]) + 1
    fases = ["S", "O", "C", "R", "A", "T", "I", "C", "O"]
    fase_actual = fases[min(num_user_msgs - 1, len(fases) - 1)]

    st.session_state.messages.append({
        "role": "user", 
        "content": user_input, 
        "timestamp": now_str,
        "fase": fase_actual
    })
    
    with st.chat_message("user", avatar="👦"):
        st.write(user_input)

    try:
        client = anthropic.Anthropic(api_key=claude_api_key)

        history_claude = []
        for m in st.session_state.messages:
            role_claude = "assistant" if m["role"] == "assistant" else "user"
            history_claude.append({"role": role_claude, "content": m["content"]})

        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=350,
            system=SYSTEM_PROMPT,
            messages=history_claude
        )

        bot_reply = response.content[0].text

        if bot_reply:
            reply_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.messages.append({
                "role": "assistant", 
                "content": bot_reply, 
                "timestamp": reply_time,
                "fase": fase_actual
            })
            with st.chat_message("assistant", avatar=avatar_robot_svg):
                st.write(bot_reply)
            st.rerun()

    except Exception as e:
        st.error(f"Error de conexión con la API de Claude: {e}")
