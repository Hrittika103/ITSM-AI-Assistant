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