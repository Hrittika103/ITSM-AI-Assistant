
import pandas as pd
import sqlite3

# Load Excel dataset
file_name = "itsm_tickets_dataset_v2_1000_records.xlsx"

df = pd.read_excel(file_name)

# Connect SQLite database
conn = sqlite3.connect("tickets.db")

# Store table into database
df.to_sql(
    "tickets",
    conn,
    if_exists="replace",
    index=False
)

print("Database created successfully!")

# Check total records
cursor = conn.cursor()

cursor.execute(
    "SELECT COUNT(*) FROM tickets"
)

count = cursor.fetchone()[0]

print("Total Records:", count)

conn.close()

On Wed, Apr 8, 2026, 15:27 HRITTIKA PAUL <hrittika.paul.uemk.cse2016@gmail.com> wrote:
import pandas as pd
import sqlite3

# Load Excel dataset
file_name = "itsm_tickets_dataset_v2_1000_records.xlsx"

print("Loading Excel file...")

df = pd.read_excel(file_name)

print("Excel loaded successfully!")

# Connect SQLite database
conn = sqlite3.connect("tickets.db")

df.to_sql(
    "tickets",
    conn,
    if_exists="replace",
    index=False
)

print("Database created successfully!")

cursor = conn.cursor()

cursor.execute(
    "SELECT COUNT(*) FROM tickets"
)

count = cursor.fetchone()[0]

print("Total Records:", count)

conn.close()
Show quoted text
import sqlite3

print("Connecting to database...")

conn = sqlite3.connect("tickets.db")

cursor = conn.cursor()

# Closed Tickets
cursor.execute("""
SELECT COUNT(*)
FROM tickets
WHERE status='Closed'
""")

closed = cursor.fetchone()[0]

print("Closed Tickets:", closed)

# SLA Miss Count
cursor.execute("""
SELECT COUNT(*)
FROM tickets
WHERE sla_miss=1
""")

sla_miss = cursor.fetchone()[0]

print("SLA Miss Count:", sla_miss)

# MTTR Calculation
cursor.execute("""
SELECT 
AVG(
JULIANDAY(resolved_at) -
JULIANDAY(created_at)
)*24
FROM tickets
WHERE status='Closed'
""")

mttr = cursor.fetchone()[0]

print("MTTR (hours):", mttr)

conn.close()

print("Metrics test completed.")
Show quoted text
from langchain.utilities import SQLDatabase
from langchain.llms import OpenAI
from langchain.chains import SQLDatabaseChain

print("Loading database...")

# Connect to database
db = SQLDatabase.from_uri(
    "sqlite:///tickets.db"
)

print("Database connected.")

# Load OpenAI model
llm = OpenAI(
    temperature=0
)

# Create SQL AI chain
db_chain = SQLDatabaseChain.from_llm(
    llm,
    db,
    verbose=True
)

print("AI Engine Ready!")

# Function to ask AI
def ask_ai(question):

    result = db_chain.run(question)

    return result

On Wed, Apr 8, 2026, 16:16 HRITTIKA PAUL <hrittika.paul.uemk.cse2016@gmail.com> wrote:
Show quoted text
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
Show quoted text
import sqlite3
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

def ask_ai(question):

    # Connect database
    conn = sqlite3.connect("tickets.db")
    cursor = conn.cursor()

    # Define known questions → SQL mapping
    if "closed" in question.lower():

        cursor.execute("""
        SELECT COUNT(*)
        FROM tickets
        WHERE status='Closed'
        """)

        result = cursor.fetchone()[0]

        return f"Closed Tickets: {result}"

    elif "sla" in question.lower():

        cursor.execute("""
        SELECT COUNT(*)
        FROM tickets
        WHERE sla_miss=1
        """)

        result = cursor.fetchone()[0]

        return f"SLA Miss Count: {result}"

    elif "mttr" in question.lower():

        cursor.execute("""
        SELECT 
        AVG(
        JULIANDAY(resolved_at) -
        JULIANDAY(created_at)
        )*24
        FROM tickets
        WHERE status='Closed'
        """)

        result = cursor.fetchone()[0]

        return f"MTTR (hours): {round(result,2)}"

    else:

        return "Try asking: Closed tickets, SLA misses, or MTTR"

    conn.close()
Show quoted text
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
Show quoted text
import sqlite3

def ask_ai(question):

    # Connect to database
    conn = sqlite3.connect("tickets.db")
    cursor = conn.cursor()

    question = question.lower()

    # Closed tickets
    if "closed" in question:

        cursor.execute("""
        SELECT COUNT(*)
        FROM tickets
        WHERE status='Closed'
        """)

        result = cursor.fetchone()[0]

        conn.close()

        return f"Closed Tickets: {result}"

    # Open tickets  ✅ NEW
    elif "open" in question:

        cursor.execute("""
        SELECT COUNT(*)
        FROM tickets
        WHERE status='Open'
        """)

        result = cursor.fetchone()[0]

        conn.close()

        return f"Open Tickets: {result}"

    # SLA misses
    elif "sla" in question:

        cursor.execute("""
        SELECT COUNT(*)
        FROM tickets
        WHERE sla_miss=1
        """)

        result = cursor.fetchone()[0]

        conn.close()

        return f"SLA Miss Count: {result}"

    # MTTR
    elif "mttr" in question:

        cursor.execute("""
        SELECT 
        AVG(
        JULIANDAY(resolved_at) -
        JULIANDAY(created_at)
        )*24
        FROM tickets
        WHERE status='Closed'
        """)

        result = cursor.fetchone()[0]

        conn.close()

        return f"MTTR (hours): {round(result,2)}"

    else:

        conn.close()

        return "Try asking about Closed tickets, Open tickets, SLA misses, or MTTR."
Show quoted text
# High priority tickets
    elif "high" in question:

        cursor.execute("""
        SELECT COUNT(*)
        FROM tickets
        WHERE priority='High'
        """)

        result = cursor.fetchone()[0]

        conn.close()

        return f"High Priority Tickets: {result}"
Show quoted text
# Medium priority tickets
    elif "medium" in question:

        cursor.execute("""
        SELECT COUNT(*)
        FROM tickets
        WHERE priority='Medium'
        """)

        result = cursor.fetchone()[0]

        conn.close()

        return f"Medium Priority Tickets: {result}"

    # Low priority tickets
    elif "low" in question:

        cursor.execute("""
        SELECT COUNT(*)
        FROM tickets
        WHERE priority='Low'
        """)

        result = cursor.fetchone()[0]

        conn.close()

        return f"Low Priority Tickets: {result}"

    # Critical priority tickets
    elif "critical" in question:

        cursor.execute("""
        SELECT COUNT(*)
        FROM tickets
        WHERE priority='Critical'
        """)

        result = cursor.fetchone()[0]

        conn.close()

        return f"Critical Priority Tickets: {result}"
Show quoted text
# ITSM AI Assistant (Local Demo Project)

## Overview

This project demonstrates a local ITSM assistant 
that retrieves ticket metrics using natural language queries.

The assistant connects to a SQLite database created 
from an Excel-based ITSM dataset.

## Features

- Open Ticket Count
- Closed Ticket Count
- SLA Miss Count
- MTTR Calculation
- Priority-based Ticket Counts
  - High
  - Medium
  - Low
  - Critical

## Technologies Used

- Python
- SQLite
- Streamlit
- Pandas

## Example Questions

How many open tickets?

How many closed tickets?

How many SLA misses?

What is MTTR?

How many high priority tickets?

How many critical priority tickets?

## Future Enhancements

- ServiceNow Integration
- Real-time dashboards
- Predictive SLA analytics
Show quoted text
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
Show quoted text
import streamlit as st
import time
from ai_engine import ask_ai

# Page title
st.title("💬 ITSM AI Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input box
user_input = st.chat_input("Ask your ITSM question...")

if user_input:

    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.write(user_input)

    # Assistant response
    with st.chat_message("assistant"):

        # Show typing effect
        with st.spinner("Assistant is thinking..."):
            time.sleep(2)  # Delay for realism

            response = ask_ai(user_input)

        st.write(response)

        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )
Show quoted text
Got it — you want the messages to appear side-by-side like real chat bubbles, not stacked awkwardly one after another.
That's exactly how modern Streamlit chat apps should behave — and we can fix this cleanly.
Right now the issue is likely because:
Charts are loading above chat
Messages are not grouped properly
Chat container isn't structured correctly
We'll fix it so it looks like:
👤 User (right side)
🤖 Assistant (left side)
With smooth typing delay.
What We'll Fix
We'll:
✅ Keep charts at top
✅ Show chat below
✅ Show proper side-by-side bubbles
✅ Keep typing delay
✅ Keep suggested buttons
Replace Your app.py With This Clean Chat Layout
Open:
Plain text
app.py
Replace everything with this improved version:
Python
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
Save:
Plain text
Ctrl + S
Now Restart Streamlit
In terminal:
Bash
Ctrl + C
streamlit run app.py
What You Should Now See
Correct behavior:
✔ User message → Right side
✔ Assistant message → Left side
✔ Messages grouped
✔ Looks like real chat
✔ Spinner delay
✔ Charts still visible
Just like professional chat apps.
Optional — Make It Look Even Better
Next upgrades I strongly recommend:
1️⃣ Add Clear Chat button
2️⃣ Add timestamps
3️⃣ Add message avatars
4️⃣ Add colored chat bubbles
These make it look product-grade.
Tell Me What You See Now
After running:
Do messages now appear:
1️⃣ User on right, assistant on left?
OR
2️⃣ Still stacked incorrectly?
If still not perfect, send screenshot — I'll fix layout precisely.
Show quoted text
import streamlit as st
import time
from ai_engine import ask_ai

# Page config
st.set_page_config(page_title="ITSM AI Assistant")

# Title
st.title("💬 ITSM AI Assistant")

# Welcome message
st.markdown(
"""
👋 **Hello! I'm your ITSM Assistant**

Ask me things like:

• How many open tickets?  
• What is MTTR?  
• How many SLA misses?  
• How many high priority tickets?  
"""
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Ask your ITSM question...")

# Process user input
if user_input:

    # Show user message (RIGHT SIDE)
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Assistant response (LEFT SIDE)
    with st.chat_message("assistant"):

        # Typing delay
        with st.spinner("Assistant is thinking..."):
            time.sleep(2.5)  # delay for realism

            response = ask_ai(user_input)

        st.markdown(response)

        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )
Show quoted text


On Tue, Apr 14, 2026, 17:42 HRITTIKA PAUL <hrittika.paul.uemk.cse2016@gmail.com> wrote:
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
