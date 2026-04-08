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
