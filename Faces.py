import pygame
import random
import threading
import database
from database import clear_database, view_database
import os
import base64
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Pre-agreed passphrase and key derivation for AES-GCM
PRE_AGREED_PASSPHRASE = "my_secure_passphrase"

def get_key():
    return hashlib.sha256(PRE_AGREED_PASSPHRASE.encode('utf-8')).digest()

def encrypt_message(plaintext):
    key = get_key()
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)  # 12 bytes nonce for AES-GCM
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode('utf-8'), None)
    # Store nonce and ciphertext together (base64-encoded)
    return base64.b64encode(nonce + ciphertext).decode('utf-8')

def decrypt_message(encrypted_text):
    key = get_key()
    aesgcm = AESGCM(key)
    data = base64.b64decode(encrypted_text)
    nonce = data[:12]
    ciphertext = data[12:]
    plaintext = aesgcm.decrypt(nonce, ciphertext, None).decode('utf-8')
    return plaintext

# The following Rubik's Cube constants and functions are retained for the visual display.
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
            view_database()
            continue
        elif input_text.lower() == "database-clear":
            clear_database()
            print("Database cleared.")
            continue
        else:
            # Encrypt the message
            encrypted = encrypt_message(input_text)
            database.save_to_db(encrypted)
            print("Encrypted text:", encrypted)
            # If automatic decryption is active, immediately decrypt and show the original text
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

    # Start the input thread (for entering messages and commands)
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
