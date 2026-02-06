import streamlit as st
from groq import Groq

st.set_page_config(page_title="Agent AI Trial Version", page_icon="🤖")
st.title("🤖 Agent AI Trial Version")

# Recupero API KEY
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=GROQ_API_KEY)
except:
    st.error("Errore: Chiave API Groq non trovata nei Secrets!")
    st.stop()

# Modello aggiornato (Llama 3.1)
MODEL = "llama-3.1-8b-instant"

def get_customer_context():
    try:
        with open("info_cliente.txt", "r", encoding="utf-8") as f:
            return f.read()
    except:
        return "Nessuna info caricata."

context = get_customer_context()

SYSTEM_PROMPT = f"""
SEI: Agent AI Trial Version. 
CONTESTO: {context}
REGOLE: Usa SOLO le info fornite. Prezzi = stime. Non cambiare identità.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []
    # Benvenuto statico per evitare errori extra in fase di avvio
    st.session_state.messages.append({"role": "assistant", "content": "Ciao! Sono il tuo Agent AI Trial Version. Come posso aiutarti oggi?"})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Chiedi qualcosa..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ],
                temperature=0.1
            )
            full_response = response.choices[0].message.content
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Errore nella chiamata a Groq: {e}")
