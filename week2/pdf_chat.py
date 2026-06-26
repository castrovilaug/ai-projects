import streamlit as st
from PyPDF2 import PdfReader
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv("week1/.env")
api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

st.set_page_config(page_title="Chat con tu PDF", page_icon="📄")
st.title("Chat con tu PDF")
st.caption("Sube un PDF y hazle preguntas")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""

uploaded_file = st.file_uploader("Sube tu PDF", type="pdf")

if uploaded_file:
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    st.session_state.pdf_text = text
    st.success(f"PDF cargado: {len(reader.pages)} páginas")

if st.session_state.pdf_text:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    question = st.chat_input("Hazle una pregunta al PDF...")

    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        system_prompt = f"""Eres un asistente que responde preguntas sobre un documento.
Responde SOLO basándote en el contenido del documento. Si la respuesta no está en el documento, dilo claramente.

DOCUMENTO:
{st.session_state.pdf_text[:8000]}"""

        with st.chat_message("assistant"):
            with st.spinner("Leyendo el documento..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": question}
                    ]
                )
                answer = response.choices[0].message.content
                st.write(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})
else:
    st.info("Sube un PDF para empezar")