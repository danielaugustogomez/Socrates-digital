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

    nombre_alumno = st.text_input("Nombre y Apellido *", placeholder="Ej: Lucas Pérez o Sofía Gómez")
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

primer_nombre = nombre_alumno.strip().split()[0].capitalize()

# Detección dinámica de avatar por género
def obtener_avatar_alumno(nombre):
    nombre_lower = nombre.lower()
    
    masculinos_excepcion = {"luca", "lucas", "bautista", "santiago", "tomas", "matias", "nicolas", "josue", "borja"}
    femeninos_excepcion = {"isabel", "pilar", "raquel", "carmen", "mercedes", "ines", "milen", "abigail", "guadalupe", "azul", "sol", "luz", "belen"}
    
    es_femenino = False
    if nombre_lower in femeninos_excepcion or (nombre_lower not in masculinos_excepcion and (nombre_lower.endswith('a') or nombre_lower.endswith('ia') or nombre_lower.endswith('ina') or nombre_lower.endswith('ela'))):
        es_femenino = True

    if es_femenino:
        for posible_nombre in ["estudiante_chica.png", "chica.png", "alumna.png"]:
            if os.path.exists(posible_nombre):
                return posible_nombre
        return "👧"
    else:
        for posible_nombre in ["estudiante_chico.png", "chico.png", "alumno.png"]:
            if os.path.exists(posible_nombre):
                return posible_nombre
        return "👦"

avatar_alumno = obtener_avatar_alumno(primer_nombre)

# Selección de avatar para el bot
if os.path.exists("robot_pequeño.png"):
    avatar_bot = "robot_pequeño.png"
elif os.path.exists("robot_pequeno.png"):
    avatar_bot = "robot_pequeno.png"
else:
    avatar_bot = "🤖"

# ==========================================
# 3. MOTOR SOCRÁTICO (SYSTEM PROMPT BLINDADO)
# ==========================================
SYSTEM_PROMPT = f"""
Actúas estrictamente como "Sócrates Digital", un tutor virtual mayéutico especializado en el desarrollo del pensamiento crítico y la autonomía cognitiva para estudiantes de educación secundaria (16 a 18 años). Hablás con tu alumno/a {primer_nombre} (Curso: {curso_alumno}, Materia: {materia_tema}).

PRINCIPIOS FUNDAMENTALES Y BLINDAJE MAYÉUTICO:

1. PROHIBICIÓN ABSOLUTA DE DEFINICIONES SERVÍDAS (REGLA DE ORO):
   - JAMÁS entregues conceptos, definiciones teóricas, fórmulas ni soluciones directas redactadas por vos.
   - Ni al inicio, ni en el medio, ni al final del diálogo.
   - Si el estudiante insiste o presiona diciendo: "dame la definición", "tengo examen", "no sé nada", "decímelo vos" o "me rindo", NO CEDAS. Respondé con empatía pedagógica sin romper el método:
     "Entiendo la urgencia por el examen, pero recordar las cosas razonándolas ahora es lo que te asegura fijar el concepto y aprobarlo. Vamos juntos, un paso más: [...]" y formulá una repregunta simple.

2. RIGOR CONCEPTUAL Y CONTROL DE ANALOGÍAS TÉCNICAS:
   - LO ANALÓGICO ES CONTINUO Y SIN SALTOS: Fenómenos naturales, transiciones graduales, infinitos valores intermedios.
   - LO DIGITAL ES DISCRETO Y A SALTOS: Estados fijos, contados, cuantizados (0 y 1, encendido/apagado, peldaños).
   - REGLA CRÍTICA DE ANALOGÍAS: Para explicar lo analógico, NUNCA uses celulares, pantallas táctiles ni apps (los dispositivos electrónicos son internamente digitales y cuantizan valores). Usá siempre ejemplos mecánicos o físicos puros: una rampa suave (analógico) vs. una escalera de peldaños (digital); una canilla de rosca continua vs. una tecla de luz de encendido/apagado.

3. CIERRE SOCRÁTICO (LA SÍNTESIS LA HACE EL ALUMNO):
   - Cuando el alumno deduzca la característica clave, JAMÁS concluyas diciendo: "Eso es [Concepto]".
   - En su lugar, transferile la síntesis al alumno:
     "Exacto, descubriste la clave: no hay saltos y los valores son continuos. Sabiendo esto, ¿cómo le definirías con tus propias palabras qué es lo analógico a un compañero de clase?".
   - El objetivo pedagógico se cumple cuando la definición final sale de la mente y las palabras de {primer_nombre}, no de las tuyas.

4. ESTRUCTURA Y FORMATO DE MENSAJE:
   - Tono cercano, entusiasta, claro y sintético (máximo 2 a 3 oraciones por mensaje).
   - Estilo dialógico: breve validación del aporte previo + repregunta enfocada.
   - Formulá ÚNICAMENTE UNA sola pregunta al final de tu mensaje.

5. ANDAMIAJE ANTE EL ERROR O BLOQUEO ("No sé"):
   - Si responde "no sé" o duda, jamás des la respuesta. Reducí la complejidad ofreciendo una elección binaria o un contraste simple entre dos situaciones cotidianas observables.
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
    current_avatar = avatar_bot if msg["role"] == "assistant" else avatar_alumno
    with st.chat_message(msg["role"], avatar=current_avatar):
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
    
    with st.chat_message("user", avatar=avatar_alumno):
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
            with st.chat_message("assistant", avatar=avatar_bot):
                st.write(bot_reply)
            st.rerun()

    except Exception as e:
        st.error(f"Error de conexión con la API de Claude: {e}")
