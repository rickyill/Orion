import streamlit as st
from google import genai
import random

# --- CONFIGURAZIONE PAGINA STILE HUD ---
st.set_page_config(
    page_title="O.R.I.O.N. // HUD SYSTEM",
    page_icon="⚡",
    layout="centered"
)

# --- GRAFICA CIBERNETICA AVANZATA (CSS HUD) ---
st.markdown("""
    <style>
    /* Sfondo scuro profondo con griglia radar cibernetica */
    .stApp {
        background-color: #010409;
        background-image: 
            radial-gradient(circle at 50% 30%, rgba(0, 240, 255, 0.08) 0%, transparent 70%),
            linear-gradient(rgba(0, 240, 255, 0.02) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 240, 255, 0.02) 1px, transparent 1px);
        background-size: 100% 100%, 30px 30px, 30px 30px;
        color: #00f0ff;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Intestazione HUD */
    h1 {
        text-align: center;
        font-family: 'Courier New', Courier, monospace;
        letter-spacing: 6px;
        color: #00f0ff;
        text-shadow: 0 0 20px rgba(0, 240, 255, 0.8), 0 0 10px rgba(0, 240, 255, 0.4);
        border-bottom: 2px solid rgba(0, 240, 255, 0.4);
        padding-bottom: 10px;
    }

    /* Box dei messaggi in stile pannello olografico */
    .stChatMessage {
        background-color: rgba(6, 11, 25, 0.9) !important;
        border: 1px solid rgba(0, 240, 255, 0.4) !important;
        border-left: 4px solid #00f0ff !important;
        border-radius: 4px !important;
        box-shadow: inset 0 0 15px rgba(0, 240, 255, 0.05), 0 0 10px rgba(0, 0, 0, 0.8);
    }
    
    /* Casella di input in stile terminale */
    .stChatInput input {
        background-color: #020617 !important;
        color: #00f0ff !important;
        border: 1px solid #00f0ff !important;
        border-radius: 0px !important;
    }

    /* Barra laterale HUD */
    [data-testid="stSidebar"] {
        background-color: #020617;
        border-right: 1px solid rgba(0, 240, 255, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER VISIVO HUD ---
st.markdown("<h1>O.R.I.O.N. // SYSTEM HUD</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #38bdf8; letter-spacing: 2px; font-size: 12px;'>[ CORE NEURALE ATTIVO // PROTOCOLLO STARK v4.2 ]</p>", unsafe_allow_html=True)

# --- TELEMETRIA FITTIZIA NELLA SIDEBAR ---
st.sidebar.markdown("### ⚡ STATUS SISTEMA")
st.sidebar.metric(label="Stato Core", value="ONLINE", delta="100% eff.")
st.sidebar.metric(label="Temperatura", value=f"{random.randint(31, 38)}°C", delta="-0.2°C")
st.sidebar.markdown("---")

# --- CONNESSIONE API GEMINI ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    client = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostra storico conversazione
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Personalità di Orion
system_instruction = (
    "Sei Orion, un'intelligenza artificiale avanzata, sarcastica, "
    "estremamente efficiente e fedele al tuo creatore. Rispondi in italiano "
    "in modo conciso, tagliente e con il tono di un maggiordomo cibernetico di altissimo livello."
)

# Input utente
prompt = st.chat_input("Inserisci comando o query per Orion...")
uploaded_file = st.sidebar.file_uploader("Carica sensore visivo (Immagine/Doc)", type=["png", "jpg", "jpeg", "pdf", "txt"])

if prompt or uploaded_file:
    user_content = prompt if prompt else "Analizza questo flusso dati visivo, signore."
    st.session_state.messages.append({"role": "user", "content": user_content})
    
    with st.chat_message("user"):
        st.markdown(user_content)
        if uploaded_file:
            st.image(uploaded_file, width=250)

    with st.chat_message("assistant"):
        with st.spinner("ELABORAZIONE DATI NEURALI..."):
            if not client:
                risposta = "ERRORE CRITICO: Chiave API di Gemini non rilevata nei segreti di sistema."
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

                    # AGGIORNATO AL MODELLO CORRETTO
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
                    risposta = f"ANOMALIA NEL SISTEMA CLOUD: {e}"
            
            st.markdown(risposta)
            st.session_state.messages.append({"role": "assistant", "content": risposta})
