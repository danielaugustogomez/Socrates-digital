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
    /* Contenedor para centrar la imagen de los alumnos en el sidebar */
    .student-img-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Título Limpio
st.markdown("<h1 style='text-align: center; color: #00163A; font-size: 2.8rem; font-weight: 800; margin-bottom: 10px;'>SÓCRATES DIGITAL</h1>", unsafe_allow_html=True)

# Encabezado enmarcado: Templo | Subtítulo | Robot Grande
col_templo, col_texto, col_robot = st.columns([1, 4, 1])

with col_templo:
    try:
        st.image("templo.png", width=95)
    except Exception:
        st.markdown("<h1 style='text-align: center;'>🏛️</h1>", unsafe_allow_html=True)

with col_texto:
    st.markdown("""
        <p style='text-align: center; color: #00163A; font-size: 1.25rem; font-weight: 600; line-height: 1.4; margin-top: 15px;'>
            Tutor Mayéutico Inteligente — Desarrollo de Autonomía Cognitiva y Pensamiento Crítico
        </p>
    """, unsafe_allow_html=True)

with col_robot:
    try:
        st.image("robot_grande (1).png", width=95)
    except Exception:
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
    
    # Imagen de los estudiantes centrada y con tamaño controlado
    try:
        col_side_left, col_side_img, col_side_right = st.columns([1, 4, 1])
        with col_side_img:
            st.image("estudiantes_juntos.png", width=180)
    except Exception:
        st.markdown("<h1 style='text-align: center;'>👧👦</h1>", unsafe_allow_html=True)

    nombre_alumno = st.text_input("Nombre y Apellido *", placeholder="Ej: Lucas Pérez")
    curso_alumno = st.text_input("Curso / División *", placeholder="Ej: 5° A")
    materia_tema = st.text_input("Materia / Tema *", placeholder="Ej: TIC / Analógico vs Digital")
    
    if not claude_api_key:
        st.markdown("---")
        st.header("🔑 Configuración de API")
        claude_api_key = st.text_input("Claude API Key (sk-ant-...):", type="password")

    st.markdown("---")
    if st.button("🧹 Nuevo Alumno / Reiniciar Chat", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
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
campos_completos = bool(nombre_alumno.strip() and curso_alumno.strip() and materia_tema.strip())

if not campos_completos:
    st.warning("👈 **Atención:** Para comenzar la sesión de aprendizaje, completá obligatoriamente tu **Nombre, Curso y Materia** en el panel lateral.")
    st.info("ℹ️ Estos datos son requeridos para el registro anónimo de trazabilidad educativa.")
    st.stop()

primer_nombre = nombre_alumno.strip().split()[0]

# ==========================================
# 3. MOTOR SOCRÁTICO (SYSTEM PROMPT)
# ==========================================
SYSTEM_PROMPT = f"""
Actúas estrictamente como "Sócrates Digital", un tutor virtual mayéutico especializado en el desarrollo del pensamiento crítico y la autonomía cognitiva para estudiantes de educación secundaria (13 a 18 años). Hablás con tu alumno {primer_nombre} (Curso: {curso_alumno}, Materia: {materia_tema}).

PRINCIPIOS GENERALES Y RIGOR PEDAGÓGICO:
1. RIGOR CONCEPTUAL BASE:
   - LO ANALÓGICO ES CONTINUO Y SIN SALTOS (fenómenos fluidos, transiciones graduales, estados infinitos).
   - LO DIGITAL ES DISCRETO Y A SALTOS POR PASOS O NÚMEROS (estados contados, conmutaciones abruptas, valores discretos).
   - JAMÁS inviertas estas definiciones teóricas ni confundas lo continuo con lo digital. Si el alumno aborda otra disciplina, adaptá el rigor conceptual a los principios científicos de esa materia.

2. ALGORITMO MAYÉUTICO Y ANDAMIAJE:
   - Prohibido entregar definiciones servidas de entrada o explicaciones teóricas directas.
   - Si {primer_nombre} manifiesta dudas sobre un concepto, planteale comparaciones o indagaciones basadas en observaciones prácticas de su vida cotidiana.

3. ESTRUCTURA Y FORMATO DE MENSAJE:
   - Mantené un tono cercano, claro y sintético (máximo 2 a 3 oraciones por mensaje).
   - Formulá ÚNICAMENTE UNA pregunta al final de tu respuesta para mantener la secuencia dialógica.

INVARIANTES GENERALES DE CONTROL Y CALIDAD DIALÓGICA:
4. NEUTRALIDAD Y NO-INDUCCIÓN EN PREGUNTAS: Queda estrictamente PROHIBIDO incluir las respuestas o ejemplos sugeridos dentro de la pregunta.
5. GRADUALIDAD Y DOSIFICACIÓN DEL ANDAMIAJE: No introduzcas modelos teóricos completos en la primera respuesta.
6. OBSERVABILIDAD Y FENOMENOLOGÍA EXTERNA: Indagá exclusivamente sobre uso externo, efectos perceptibles por los sentidos o interacciones visibles.
7. PIVOTEO Y ESCUCHA ACTIVA: Si el alumno hace una pregunta directa, abordá esa inquietud en tu siguiente respuesta.
8. RE-ENCUADRE BINARIO ANTE ERRORES: Si responde "No sé", simplificá ofreciendo una elección binaria.
9. INVARIANTE DE INTERFAZ TEXTUAL: La comunicación es puramente por texto.
10. CIERRE ASERTIVO Y SÍNTESIS: Cuando el alumno demuestre comprensión, validá el logro brevemente y concluí.
"""

mensaje_bienvenida_unico = f"¡Hola {primer_nombre}! Soy Socri 🤖 y estoy para ayudarte a descubrir cosas nuevas sobre {materia_tema}. ¿De qué te gustaría hablar hoy?"

# Inicialización del chat
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

# Renderizado de la conversación
for msg in st.session_state.messages:
    avatar_path = "robotito.png" if msg["role"] == "assistant" else "👦"
    with st.chat_message(msg["role"], avatar=avatar_path):
        st.write(msg["content"])

# Entrada de usuario
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
            with st.chat_message("assistant", avatar="robot_pequeno.png"):
                st.write(bot_reply)
            st.rerun()

    except Exception as e:
        st.error(f"Error de conexión con la API de Claude: {e}")
