import streamlit as st
from google import genai
import json
import streamlit.components.v1 as components

# Configurazione pagina HUD
st.set_page_config(
    page_title="O.R.I.O.N. // Cloud Core",
    page_icon="🌌",
    layout="centered"
)

# Stile CSS Cyberpunk / Olografico
st.markdown("""
    <style>
    .stApp {
        background-color: #030712;
        background-image: radial-gradient(circle at 50% 50%, rgba(0, 240, 255, 0.05) 0%, transparent 80%);
        color: #00f0ff;
    }
    h1 {
        text-align: center;
        font-family: 'Courier New', monospace;
        letter-spacing: 3px;
        color: #00f0ff;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
    }
    .stChatMessage {
        background-color: rgba(17, 24, 39, 0.8);
        border: 1px solid rgba(0, 240, 255, 0.2);
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>O.R.I.O.N. // SYSTEM ONLINE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ca3af;'>Neural Core Cloud powered by Google Gemini</p>", unsafe_allow_html=True)

# Connessione API Gemini tramite i Secrets di Streamlit
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    client = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostra storico chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

system_instruction = (
    "Sei Orion, un'intelligenza artificiale avanzata, sarcastica, "
    "estremamente efficiente e fedele al tuo creatore. Rispondi in italiano "
    "in modo conciso, diretto e con un tono da maggiordomo cibernetico di altissimo livello."
)

prompt = st.chat_input("Invia un comando a Orion...")
uploaded_file = st.sidebar.file_uploader("Carica immagine o documento", type=["png", "jpg", "jpeg", "pdf", "txt"])

if prompt or uploaded_file:
    user_content = prompt if prompt else "Analizza questo file, signore."
    st.session_state.messages.append({"role": "user", "content": user_content})

    with st.chat_message("user"):
        st.markdown(user_content)
        if uploaded_file:
            st.image(uploaded_file, width=250)

    with st.chat_message("assistant"):
        with st.spinner("Elaborazione dati..."):
            if not client:
                risposta = "Errore: Chiave API di Gemini non configurata nei segreti di Streamlit Cloud."
            else:
                try:
                    contenuti = [user_content]
                    file_temp = None
                    if uploaded_file:
                        file_temp = f"temp_{uploaded_file.name}"
                        with open(file_temp, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        uploaded_g = client.files.upload(file=file_temp)
                        contenuti.append(uploaded_g)

                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=contenuti,
                        config={
                            'system_instruction': system_instruction,
                            'temperature': 0.7,
                        }
                    )
                    risposta = response.text
                except Exception as e:
                    risposta = f"Anomalia nei sistemi: {e}"

            st.markdown(risposta)
            st.session_state.messages.append({"role": "assistant", "content": risposta})
