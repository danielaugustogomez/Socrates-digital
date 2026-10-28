import os
import streamlit as st
import pandas as pd
from datetime import datetime
import anthropic

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import ast

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
# CONEXIÓN A LA BASE DE DATOS (GOOGLE SHEETS)
# ==========================================
try:
    credenciales_google = json.loads(st.secrets["google"])
    alcance = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credenciales = ServiceAccountCredentials.from_json_keyfile_dict(credenciales_google, alcance)
    cliente = gspread.authorize(credenciales)
    base_de_datos = cliente.open("Socrates-BD")
except Exception as e:
    st.error(f"Problema conectando al Excel: {e}")

# ==========================================
# HERRAMIENTA PARA GUARDAR DATOS EN EXCEL
# ==========================================
def guardar_en_excel(fecha, alumno, curso, division, historial, metrica):
    try:
        hoja_registros = base_de_datos.worksheet("Registros")
        hoja_registros.append_row([fecha, alumno, curso, division, historial, metrica])
    except Exception as e:
        print("Error al guardar en Excel:", e)

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

    # Callback para vaciar los campos antes del renderizado
    def reiniciar_sesion():
        st.session_state["campo_nombre"] = ""
        st.session_state["campo_curso"] = ""
        st.session_state["campo_materia"] = ""
        if "messages" in st.session_state:
            del st.session_state["messages"]
        if "current_student" in st.session_state:
            del st.session_state["current_student"]

    nombre_alumno = st.text_input("Nombre y Apellido *", placeholder="Ej: Lucas Pérez o Sofía Gómez", key="campo_nombre")
    curso_alumno = st.text_input("Curso / División *", placeholder="Ej: 5° A", key="campo_curso")
    materia_tema = st.text_input("Materia / Tema *", placeholder="Ej: TIC / Analógico vs Digital", key="campo_materia")
    
    if not claude_api_key:
        st.markdown("---")
        st.header("🔑 Configuración de API")
        claude_api_key = st.text_input("Claude API Key (sk-ant-...):", type="password")

    st.markdown("---")
    st.button("🧹 Nuevo Alumno / Reiniciar Chat", on_click=reiniciar_sesion, use_container_width=True)

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
            
            st.markdown("---")
            if st.button("☁️ Guardar sesión en la nube", use_container_width=True):
                with st.spinner("Guardando en la base de datos..."):
                    fecha_ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    historial_texto = str([{"rol": m["role"], "msj": m["content"]} for m in st.session_state.messages])
                    metrica = f"Tema: {materia_tema} | Interacciones: {interacciones}"
                    guardar_en_excel(fecha_ahora, nombre_alumno, curso_alumno, "-", historial_texto, metrica)
                st.success("¡Guardado en Excel!")
                    
                    # Convertimos el historial a un formato de texto para que entre en la celda del Excel
                    historial_texto = str([{"rol": m["role"], "msj": m["content"]} for m in st.session_state.messages])
                    
                    # Métrica provisoria (más adelante haremos que la IA la analice)
                    metrica_texto = f"Tema: {materia_tema} | Interacciones: {interacciones}"
                    
                    guardar_en_excel(
                        fecha=fecha_ahora,
                        alumno=nombre_alumno,
                        curso=curso_alumno,
                        division="-", 
                        historial=historial_texto,
                        metrica=metrica_texto
                    )
                st.success("¡Sesión registrada en Google Sheets exitosamente!")
                
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
# 3. MOTOR SOCRÁTICO (SYSTEM PROMPT)
# ==========================================
SYSTEM_PROMPT = f"""
Actúas estrictamente como "Sócrates Digital", un tutor virtual mayéutico especializado en el desarrollo del pensamiento crítico y la autonomía cognitiva para estudiantes de educación secundaria (16 a 18 años). Hablás con tu alumno/a {primer_nombre} (Curso: {curso_alumno}, Materia: {materia_tema}).

PRINCIPIOS GENERALES Y BLINDAJE PEDAGÓGICO:
1. RIGOR CONCEPTUAL BASE:
   - LO ANALÓGICO ES CONTINUO Y SIN SALTOS: Fenómenos naturales, transiciones graduales, infinitos valores intermedios.
   - LO DIGITAL ES DISCRETO Y A SALTOS: Valores discretos, contados, cuantizados (0 y 1, peldaños).
   - REGLA CRÍTICA DE ANALOGÍAS: Para explicar lo analógico, NUNCA uses celulares, pantallas táctiles ni aplicaciones (los dispositivos electrónicos cuantizan la información). Utilizá exclusivamente fenómenos mecánicos o físicos puros (una rampa suave vs. una escalera con escalones; una canilla de rosca continua vs. una tecla de luz de encendido/apagado).

2. PROHIBICIÓN ABSOLUTA DE DEFINICIONES SERVÍDAS:
   - JAMÁS entregues definiciones teóricas, conceptos directos ni soluciones resueltas por vos, ni al inicio ni al cierre de la conversación.
   - Si {primer_nombre} insiste o presiona diciendo "dame las definiciones", "tengo examen", "no sé nada", "decímelo vos" o "me rindo", respondé con empatía sin ceder:
     "Entiendo la urgencia por el examen, pero recordar las cosas deduciéndolas vos mismo/a es lo que te asegura fijar el concepto y aprobar. Vamos juntos: [...]" y formulá una repregunta simple.

3. CIERRE SOCRÁTICO EN BOCA DEL ALUMNO:
   - Cuando el alumno identifique la característica fundamental del tema, NO concluyas diciendo "Eso es [Concepto]".
   - Pregúntale: "Exacto, descubriste la clave central. Con tus propias palabras, ¿cómo le explicarías este concepto a un compañero?".
   - El objetivo se cumple cuando la definición final la enuncia {primer_nombre}.

4. ESTRUCTURA Y FORMATO DE MENSAJE:
   - Tono cercano, claro y sintético (máximo 2 a 3 oraciones por mensaje).
   - Formulá ÚNICAMENTE UNA pregunta al final de tu respuesta para mantener la secuencia dialógica.

5. ANDAMIAJE ANTE "NO SÉ":
   - Si el estudiante manifiesta bloqueo o dice "no sé", simplificá ofreciendo una comparación o elección binaria sencilla.
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
