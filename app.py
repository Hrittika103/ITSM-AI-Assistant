import os
import sqlite3
import pandas as pd
import streamlit as st
from ai_engine import ask_ai

# Initialize DB only if it doesn't exist to save resources
DB_NAME = 'tickets.db'
EXCEL_FILE = 'itsm_tickets_dataset_v2_1000_records.xlsx'

if not os.path.exists(DB_NAME):
    # Using openpyxl as recommended by pandas documentation
    df = pd.read_excel(EXCEL_FILE, engine='openpyxl') 
    conn = sqlite3.connect(DB_NAME)
    # Convert dataframe to SQL table
    df.to_sql('tickets', conn, index=False, if_exists='replace')
    conn.close()

st.title("ITSM AI Assistant")
st.write("Ask questions like:")
st.markdown("""
* How many tickets are closed?
* How many SLA misses?
* What is MTTR?
""")

question = st.text_input("Ask your question:")

if question:
    # Processing the AI engine response
    result = ask_ai(question)
    st.write(result)
