import sqlite3
from datetime import datetime

DATABASE_NAME = 'encrypted_data.db'

def init_db():
    """Initialize the SQLite database and create the table if it doesn't exist."""
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS encrypted_messages
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      original_text TEXT,
                      encrypted_text TEXT,
                      timestamp DATETIME)''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

def save_to_db(original_text, encrypted_text):
    """Save the original and encrypted text to the database."""
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute('''INSERT INTO encrypted_messages 
                     (original_text, encrypted_text, timestamp)
                     VALUES (?, ?, ?)''',
                  (original_text, encrypted_text, datetime.now()))
        conn.commit()
        print("Data saved to database successfully!")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

def view_database():
    """View all records in the database."""
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM encrypted_messages")
        rows = c.fetchall()
        
        print("\nDatabase Contents:")
        print("ID | Original Text | Encrypted Text | Timestamp")
        print("------------------------------------------------")
        for row in rows:
            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

def clear_database():
    """Delete all records from the database."""
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute("DELETE FROM encrypted_messages")
        c.execute("DELETE FROM sqlite_sequence WHERE name='encrypted_messages'")
        conn.commit()
        print("All records deleted successfully.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()