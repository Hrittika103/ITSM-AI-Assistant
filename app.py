import streamlit as st
from ai_engine import ask_ai

st.title("ITSM AI Assistant")

st.write("""
Ask questions like:

• How many tickets are closed?
• How many SLA misses?
• What is MTTR?
""")

question = st.text_input(
"Ask your question:"
)

if question:

    result = ask_ai(question)

    st.write(result)
    