import pygame
import random
import threading
import database
from database import clear_database, view_database
import os
import base64
import hashlib
import string
import time

# Pre‐agreed passphrase for the dynamic substitution cipher
PRE_AGREED_PASSPHRASE = "my_secure_passphrase"
# Define an alphabet that includes letters, digits, punctuation, and space.
ALPHABET = string.ascii_letters + string.digits + string.punctuation + " "

def encrypt_message(plaintext: str) -> str:
    """
    Encrypts the plaintext by generating an independent random permutation for each character.
    For every character (if it is in ALPHABET), a permutation is generated using a seed derived
    from the pre‐agreed passphrase, a random nonce, and the character's index. The encrypted
    character is the character in the permutation at the same index as in ALPHABET.
    
    The nonce (base64‑encoded) is prepended (with a colon separator) to the ciphertext.
    """
    nonce = os.urandom(8)  # Generate an 8-byte nonce
    nonce_b64 = base64.b64encode(nonce).decode('utf-8')
    ciphertext_chars = []
    for i, ch in enumerate(plaintext):
        if ch in ALPHABET:
            # For each character, generate a permutation specific to its index.
            seed = int.from_bytes(
                hashlib.sha256(PRE_AGREED_PASSPHRASE.encode('utf-8') + nonce + str(i).encode('utf-8')).digest(), 
                'big'
            )
            rng = random.Random(seed)
            permuted = list(ALPHABET)
            rng.shuffle(permuted)
            # Instead of a cyclic shift, use the permutation mapping:
            idx = ALPHABET.index(ch)
            ciphertext_chars.append(permuted[idx])
        else:
            ciphertext_chars.append(ch)
    ciphertext = ''.join(ciphertext_chars)
    return nonce_b64 + ":" + ciphertext

def decrypt_message(encrypted_text: str) -> str:
    """
    Decrypts the text produced by encrypt_message.
    The nonce is extracted and for each character (if in ALPHABET), the same permutation is regenerated
    (using the pre‐agreed passphrase, nonce, and character's index) and the original character is recovered
    by finding the index of the encrypted character in that permutation.
    """
    try:
        nonce_b64, ciphertext = encrypted_text.split(":", 1)
    except ValueError:
        raise ValueError("Invalid encrypted text format; missing nonce separator.")
    nonce = base64.b64decode(nonce_b64)
    plaintext_chars = []
    for i, ch in enumerate(ciphertext):
        if ch in ALPHABET:
            seed = int.from_bytes(
                hashlib.sha256(PRE_AGREED_PASSPHRASE.encode('utf-8') + nonce + str(i).encode('utf-8')).digest(), 
                'big'
            )
            rng = random.Random(seed)
            permuted = list(ALPHABET)
            rng.shuffle(permuted)
            # Find the index of the encrypted character in the permutation; that's the original index in ALPHABET.
            idx = permuted.index(ch)
            plaintext_chars.append(ALPHABET[idx])
        else:
            plaintext_chars.append(ch)
    return ''.join(plaintext_chars)


# Animation functions for database view

def animate_text(text: str) -> str:
    """
    Returns an animated version of the text by cyclically shifting it.
    The shift amount is based on the current time, so the output changes every second.
    """
    if not text:
        return text
    shift = int(time.time()) % len(text)
    return text[shift:] + text[:shift]

def animate_database_view():
    """
    Continuously displays the database records, animating the encrypted text.
    The stored ciphertext remains unchanged; only the display output is animated.
    Press Ctrl+C to exit the animated view.
    """
    try:
        while True:
            records = database.get_records()
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Database Contents:")
            print("ID | Encrypted Text | Timestamp")
            print("-------------------------------------------------")
            for record in records:
                rec_id, encrypted_text, timestamp = record
                animated_text = animate_text(encrypted_text)
                print(f"{rec_id} | {animated_text} | {timestamp}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting animated database view.")

# The following constants and functions provide a Rubik's Cube visual display,
# maintaining the thematic element of an ever-changing, scrambled face.
WIDTH, HEIGHT = 400, 400
ROWS, COLS = 3, 3
SQUARE_SIZE = WIDTH // COLS
COLORS = {
    'R': (255, 0, 0),
    'G': (0, 255, 0),
    'B': (0, 0, 255),
    'Y': (255, 255, 0),
    'O': (255, 165, 0),
    'W': (255, 255, 255)
}

def generate_face():
    return [[random.choice(list(COLORS.keys())) for _ in range(COLS)] for _ in range(ROWS)]

def draw_face(face):
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(
                screen,
                COLORS[face[row][col]],
                (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            )
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                1
            )

# Global flag for decryption mode (automatic by default)
manual_decryption = False

def handle_input():
    database.init_db()  # Initialize database
    global manual_decryption
    while True:
        input_text = input("Enter text: ")
        # Process control commands that bypass encryption/decryption
        if input_text.lower() == "decrypt-manual-on":
            manual_decryption = True
            print("Manual decryption mode activated.")
            continue
        elif input_text.lower() == "decrypt-manual-off":
            manual_decryption = False
            print("Automatic decryption mode activated.")
            continue
        elif input_text.lower() == "convo-quit":
            print("Conversation quit command received. Exiting.")
            break
        elif input_text.lower() == "database-view":
            # Launch the animated database view (press Ctrl+C to exit)
            animate_database_view()
            continue
        elif input_text.lower() == "database-clear":
            clear_database()
            print("Database cleared.")
            continue
        else:
            # Encrypt the message with our new dynamic substitution cipher
            encrypted = encrypt_message(input_text)
            database.save_to_db(encrypted)
            print("Encrypted text:", encrypted)
            # If automatic decryption is active, immediately decrypt and display the original text
            if not manual_decryption:
                try:
                    decrypted = decrypt_message(encrypted)
                    print("Decrypted text:", decrypted)
                except Exception as e:
                    print("Error during decryption:", e)

def main():
    clock = pygame.time.Clock()
    running = True

    face = generate_face()

    # Start the input thread for entering messages and commands
    input_thread = threading.Thread(target=handle_input, daemon=True)
    input_thread.start()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        face = generate_face()

        screen.fill((0, 0, 0))
        draw_face(face)

        pygame.display.flip()
        clock.tick(1)
    pygame.quit()

if __name__ == "__main__":
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Rubik's Cube Encryption")
    main()
