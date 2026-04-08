

import os
import sqlite3
import pandas as pd

# Check if DB exists
if not os.path.exists("tickets.db"):
    # Load Excel and create DB dynamically
    df = pd.read_excel("itsm_tickets_dataset_v2_1000_records.xlsx")
    conn = sqlite3.connect("tickets.db")
    df.to_sql("tickets", conn, index=False, if_exists="replace")
    conn.close()
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
    
