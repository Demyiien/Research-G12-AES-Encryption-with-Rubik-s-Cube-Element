import sqlite3
import os
from datetime import datetime

# Store the database in a fixed location (Documents folder)
DATABASE_NAME = r"C:\Users\acer\Documents\CCNSHS\PracRes\Research Change\encrypted_data.db"

def init_db():
    """Initialize the SQLite database and create the table if it doesn't exist."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS encrypted_messages
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      encrypted_text TEXT,
                      timestamp DATETIME,
                      sender TEXT)''')  # Add sender column
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()


def save_to_db(encrypted_text, sender):
    """Save the encrypted text, timestamp, and sender to the database."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute('''INSERT INTO encrypted_messages 
                     (encrypted_text, timestamp, sender)
                     VALUES (?, ?, ?)''',
                  (encrypted_text, datetime.now(), sender))  # Save sender
        conn.commit()
        print("Data saved to database successfully!")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()


def view_database():
    """View all records in the database (one-time display)."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute("SELECT id, encrypted_text, timestamp FROM encrypted_messages")
        rows = c.fetchall()
        
        print("\nDatabase Contents:")
        print("ID | Encrypted Text | Timestamp")
        print("--------------------------------")
        for row in rows:
            print(f"{row[0]} | {row[1]} | {row[2]}")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

def clear_database():
    """Delete all records from the database."""
    conn = None
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

def get_records():
    """Return all records from the database as a list of tuples."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute("SELECT id, encrypted_text, timestamp, sender FROM encrypted_messages")
        rows = c.fetchall()
        return rows
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        if conn:
            conn.close()

