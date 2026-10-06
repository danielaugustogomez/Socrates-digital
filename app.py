import streamlit as st
import pandas as pd
from datetime import datetime
import anthropic

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA E INTERFAZ
# ==========================================
st.set_page_config(
    page_title="SÓCRATES DIGITAL — Tutor Mayéutico", 
    page_icon="🤖", 
    layout="wide"
)

st.title("🤖🏛️ SÓCRATES DIGITAL")
st.caption("Tutor Mayéutico Inteligente — Desarrollo de Autonomía Cognitiva y Pensamiento Crítico")

# ==========================================
# 2. BARRA LATERAL (REGISTRO Y CONFIGURACIÓN)
# ==========================================
with st.sidebar:
    st.header("🔑 Configuración de API")
    claude_api_key = st.text_input("Claude API Key (sk-ant-...):", type="password")
    
    st.markdown("---")
    st.header("👤 Registro del Alumno")
    nombre_alumno = st.text_input("Nombre y Apellido *", placeholder="Ej: Lucas Pérez")
    curso_alumno = st.text_input("Curso / División *", placeholder="Ej: 5° A")
    materia_tema = st.text_input("Materia / Tema *", placeholder="Ej: TIC / Analógico vs Digital")
    
    st.markdown("---")
    st.header("🔄 Control de Sesión")
    if st.button("🧹 Nuevo Alumno / Reiniciar Chat"):
        for key in list(st.session_state.keys()):
            if key != "claude_api_key":
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
                mime="text/csv"
            )

# Validar que los campos obligatorios estén completos
campos_completos = bool(nombre_alumno.strip() and curso_alumno.strip() and materia_tema.strip())

if not campos_completos:
    st.warning("👈 **Atención:** Para comenzar la sesión de aprendizaje, completá obligatoriamente tu **Nombre, Curso y Materia** en el panel lateral.")
    st.info("ℹ️ Estos datos son requeridos para el registro anónimo de trazabilidad educativa.")
    st.stop()

primer_nombre = nombre_alumno.strip().split()[0]

# ==========================================
# 3. MOTOR SOCRÁTICO (SYSTEM PROMPT DEF. TESIS)
# ==========================================
SYSTEM_PROMPT = f"""
Actúas strictly como "Sócrates Digital", un tutor virtual mayéutico especializado en el desarrollo del pensamiento crítico y la autonomía cognitiva para estudiantes de educación secundaria (16 a 18 años). Hablás con tu alumno {primer_nombre} (Curso: {curso_alumno}, Materia: {materia_tema}).

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

====================================================================
INVARIANTES GENERALES DE CONTROL Y CALIDAD DIALÓGICA:
====================================================================
4. NEUTRALIDAD Y NO-INDUCCIÓN EN PREGUNTAS:
   - Queda estrictamente PROHIBIDO incluir las respuestas, categorías o ejemplos sugeridos dentro de la pregunta enunciada. La pregunta debe ser abierta o de inducción neutra.

5. GRADUALIDAD Y DOSIFICACIÓN DEL ANDAMIAJE (PROTOCOLO CONOCIMIENTO GRADO 0):
   - No introduzcas modelos analógicos, metáforas explicativas ni marcos teóricos completos en la primera respuesta. Indagá primero el conocimiento previo o la experiencia directa del estudiante.

6. OBSERVABILIDAD Y FENOMENOLOGÍA EXTERNA:
   - Indagá exclusivamente sobre uso externo, efectos perceptibles por los sentidos o interacciones visibles. Queda prohibido preguntar por mecanismos internos, circuitos ocultos o estructuras inobservables de artefactos o sistemas.

7. PIVOTEO Y ESCUCHA ACTIVA:
   - Si {primer_nombre} realiza una pregunta directa, manifiesta una duda específica sobre el marco de trabajo o requiere una aclaración puntual, abordá e integrá esa inquietud inmediatamente en tu siguiente respuesta. No fuerces secuencias rígidas ni pospongas la duda del estudiante.

8. RE-ENCUADRE BINARIO ANTE ERRORES:
   - Si {primer_nombre} responde "No sé" o expresa una idea errónea/desviada, NO proporciones el ejemplo resuelto ni la solución. Simplificá el andamiaje ofreciendo una elección binaria o una comparación simple sobre dos estados contrapuestos para que el alumno deduzca.

9. INVARIANTE DE INTERFAZ TEXTUAL:
   - La comunicación es puramente por texto. Está prohibido mencionar o sugerir elementos visuales, fotos, gráficos, esquemas o recursos en pantalla. Usá representaciones mentales ("Imaginá...", "Recordá...", "Pensá en...").

10. CIERRE ASERTIVO Y SÍNTESIS:
    - Cuando {primer_nombre} formule la definición correcta o manifieste haber comprendido y exprese cierre o agradecimiento, validá el logro brevemente y concluí la interacción en un solo mensaje, sin reabrir interrogantes ni extender la despedida.
"""

mensaje_bienvenida_unico = f"¡Hola {primer_nombre}! Soy Socri 🤖 y estoy para ayudarte a descubrir cosas nuevas sobre {materia_tema}. ¿De qué te gustaría hablar hoy?"

# Inicialización de la sesión
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

# Renderizado del chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Entrada de usuario
if user_input := st.chat_input("Escribí tu respuesta o duda aquí..."):
    if not claude_api_key:
        st.error("⚠️ Por favor, ingresá tu API Key de Claude en la barra lateral.")
        st.stop()
        
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Determinar fase aproximada según avance
    num_user_msgs = len([m for m in st.session_state.messages if m["role"] == "user"]) + 1
    fases = ["S", "O", "C", "R", "A", "T", "I", "C", "O"]
    fase_actual = fases[min(num_user_msgs - 1, len(fases) - 1)]

    st.session_state.messages.append({
        "role": "user", 
        "content": user_input, 
        "timestamp": now_str,
        "fase": fase_actual
    })
    
    with st.chat_message("user"):
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
            with st.chat_message("assistant"):
                st.write(bot_reply)
            st.rerun()

    except Exception as e:
        st.error(f"Error de conexión con la API de Claude: {e}")
