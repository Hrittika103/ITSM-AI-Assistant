import streamlit as st
import time
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

from ai_engine import ask_ai

# Page title
st.set_page_config(page_title="ITSM AI Assistant")

st.title("💬 ITSM AI Assistant")

# -----------------------------
# DASHBOARD SECTION (Charts)
# -----------------------------

st.subheader("📊 ITSM Dashboard")

conn = sqlite3.connect("tickets.db")

df = pd.read_sql_query("SELECT * FROM tickets", conn)

# Status Chart
st.markdown("### 📂 Ticket Status")

status_counts = df["status"].value_counts()

fig1, ax1 = plt.subplots()
ax1.bar(status_counts.index, status_counts.values)

st.pyplot(fig1)

# Priority Chart
st.markdown("### 🔥 Priority Distribution")

priority_counts = df["priority"].value_counts()

fig2, ax2 = plt.subplots()
ax2.bar(priority_counts.index, priority_counts.values)

st.pyplot(fig2)

# Assignment Group Chart
st.markdown("### 🌐 Assignment Group")

group_counts = df["assignment_group"].value_counts()

fig3, ax3 = plt.subplots()
ax3.bar(group_counts.index, group_counts.values)

st.pyplot(fig3)

conn.close()

st.divider()

# -----------------------------
# CHAT SECTION
# -----------------------------

st.subheader("🤖 Chat Assistant")

# Suggested Questions
col1, col2, col3 = st.columns(3)

suggested_question = None

with col1:
    if st.button("📂 Open Tickets"):
        suggested_question = "How many open tickets?"

with col2:
    if st.button("⏱️ MTTR"):
        suggested_question = "What is MTTR?"

with col3:
    if st.button("⚠️ SLA Misses"):
        suggested_question = "How many SLA misses?"

# Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Ask your ITSM question...")

# Handle button click
if suggested_question:
    user_input = suggested_question

# Process input
if user_input:

    # Show user message (RIGHT SIDE)
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Assistant response (LEFT SIDE)
    with st.chat_message("assistant"):

        with st.spinner("Assistant is thinking..."):
            time.sleep(2)

            response = ask_ai(user_input)

        st.markdown(response)

        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )
