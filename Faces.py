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

def get_permutation(nonce: bytes):
    """
    Generates a permutation of ALPHABET based on a nonce and the pre‐agreed key.
    The nonce is combined with the key and hashed to produce a seed, which then
    is used to shuffle the alphabet deterministically.
    """
    seed = int.from_bytes(
        hashlib.sha256(PRE_AGREED_PASSPHRASE.encode('utf-8') + nonce).digest(), 
        'big'
    )
    rng = random.Random(seed)
    permuted = list(ALPHABET)
    rng.shuffle(permuted)
    return permuted

def encrypt_message(plaintext: str) -> str:
    """
    Encrypts the plaintext by generating a dynamic substitution mapping.
    A random nonce is generated and used (with the pre‐agreed key) to shuffle the
    alphabet. Each character is substituted based on the mapping.
    The nonce (base64-encoded) is prepended to the ciphertext separated by a colon.
    """
    nonce = os.urandom(8)  # Generate an 8-byte nonce
    permuted = get_permutation(nonce)
    mapping = {a: b for a, b in zip(ALPHABET, permuted)}
    # Encrypt: substitute each character using the mapping
    ciphertext = ''.join(mapping.get(ch, ch) for ch in plaintext)
    # Prepend the nonce (encoded in base64) for later decryption
    nonce_b64 = base64.b64encode(nonce).decode('utf-8')
    return nonce_b64 + ":" + ciphertext

def decrypt_message(encrypted_text: str) -> str:
    """
    Decrypts the encrypted text by extracting the nonce and regenerating the
    substitution mapping. The mapping is then inverted to recover the original text.
    """
    try:
        nonce_b64, ciphertext = encrypted_text.split(":", 1)
    except ValueError:
        raise ValueError("Invalid encrypted text format; missing nonce separator.")
    nonce = base64.b64decode(nonce_b64)
    permuted = get_permutation(nonce)
    reverse_mapping = {b: a for a, b in zip(ALPHABET, permuted)}
    plaintext = ''.join(reverse_mapping.get(ch, ch) for ch in ciphertext)
    return plaintext

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
            # Encrypt the message with our dynamic substitution cipher
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
