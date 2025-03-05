import time
import os
import database
from encryption import encrypt_message, decrypt_message, generate_face, face_to_string

def animate_text(text: str) -> str:
    """
    Returns an animated version of the text by cyclically shifting it based on the current time.
    """
    if not text:
        return text
    shift = int(time.time()) % len(text)
    return text[shift:] + text[:shift]

def animate_database_view():
    """
    Continuously displays the database records with the encrypted text animated.
    Press Ctrl+C to exit the animation.
    """
    try:
        while True:
            records = database.get_records()
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Database Contents:")
            print("ID | Encrypted Text | Timestamp")
            print("-------------------------------------------")
            for record in records:
                rec_id, encrypted_text, timestamp = record
                animated_text = animate_text(encrypted_text)
                print(f"{rec_id} | {animated_text} | {timestamp}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting animated database view.")

# Initialize the database
database.init_db()

# Prompt for the encryption password for this CLI session.
PASSWORD = input("Enter encryption password for CLI session: ")

def handle_input():
    """
    Reads user input and processes commands.
    Commands:
      - "database-view": Show animated view of database records.
      - "database-clear": Clear all database records.
      - "convo-quit": Quit the session.
      - Any other input is encrypted and stored.
    """
    while True:
        input_text = input("Enter text: ")
        if input_text.lower() == "convo-quit":
            print("Conversation quit command received. Exiting.")
            break
        elif input_text.lower() == "database-view":
            print("Launching animated database view (press Ctrl+C to exit)...")
            animate_database_view()
            continue
        elif input_text.lower() == "database-clear":
            database.clear_database()
            print("Database cleared.")
            continue
        else:
            # For each message, generate a new Rubik's Cube face.
            cube_face = generate_face()
            cube_face_str = face_to_string(cube_face)
            encrypted = encrypt_message(input_text, PASSWORD, cube_face_str)
            database.save_to_db(encrypted)
            print("Encrypted text:", encrypted)
            try:
                decrypted = decrypt_message(encrypted, PASSWORD)
                print("Decrypted text:", decrypted)
            except Exception as e:
                print("Error during decryption:", e)

def main():
    handle_input()

if __name__ == "__main__":
    main()
