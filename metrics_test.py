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
