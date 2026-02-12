import streamlit as st
from groq import Groq
from PyPDF2 import PdfReader

# Tu clave de Groq ya configurada
API_KEY = "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" 
client = Groq(api_key=API_KEY)

st.set_page_config(page_title="Chat con PDF (Groq)", page_icon="⚡")
st.title("⚡ Asistente rápido con Groq y PDF")

pdf_file = st.file_uploader("Sube un PDF", type=["pdf"])
pdf_text = ""

if pdf_file is not None:
    reader = PdfReader(pdf_file)
    text_parts = [page.extract_text() for page in reader.pages if page.extract_text()]
    pdf_text = "\n".join(text_parts)
    st.success(f"PDF cargado ✅")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for m in st.session_state["messages"]:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Pregunta lo que quieras..."):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    contexto = f"Documento: {pdf_text}\n\nPregunta: {prompt}"
    
    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": contexto}],
        )
        answer = resp.choices[0].message.content
    except Exception as e:
        answer = f"⚠️ Error: {e}"

    st.session_state["messages"].append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)