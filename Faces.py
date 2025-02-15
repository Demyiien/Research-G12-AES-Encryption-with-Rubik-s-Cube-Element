import random
import base64
import hashlib
import hmac
import os
import string
from hashlib import pbkdf2_hmac
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Define an alphabet (for reference; you can adjust as needed)
ALPHABET = string.ascii_letters + string.digits + string.punctuation + " "

# --- NEW: Encryption Functions with Hidden Cube Face ---

def derive_key_face(password: str, salt: bytes) -> bytes:
    """
    Derive a key for encrypting the cube face using only the user-entered password.
    """
    return pbkdf2_hmac('sha256', password.encode(), salt, 100000, dklen=32)

def derive_key_message(password: str, cube_face: str, salt: bytes) -> bytes:
    """
    Derive a key for encrypting the message using the combination of the password and the (plaintext) cube face.
    """
    key_material = password + cube_face
    return pbkdf2_hmac('sha256', key_material.encode(), salt, 100000, dklen=32)

def encrypt_message(plaintext: str, password: str, cube_face: str) -> str:
    """
    Encrypts the plaintext using AES-GCM. The process is twofold:
    
    1. Encrypt the Rubik's Cube face:
       - Generate a random salt for the face.
       - Derive a key (key_face) solely from the password.
       - Encrypt the cube face string (cube_face) using AES-GCM.
       - Build the 'cube face part' as: salt_face || nonce_face || tag_face || ciphertext_face,
         then Base64‑encode it.
    
    2. Encrypt the main message:
       - Generate a random salt for the message.
       - Derive a key (key_message) from the password concatenated with the cube face (plaintext).
       - Encrypt the plaintext with AES-GCM.
       - Compute an HMAC over the ciphertext.
       - Build the 'message part' as: salt_message || nonce_message || tag_message || hmac || ciphertext_message,
         then Base64‑encode it.
    
    Finally, combine the two parts with a "::" separator.
    """
    # --- Encrypt the Cube Face (to hide it) ---
    salt_face = os.urandom(16)
    key_face = derive_key_face(password, salt_face)
    cipher_face = AES.new(key_face, AES.MODE_GCM)
    cube_face_bytes = cube_face.encode()  # Convert cube face string to bytes
    ciphertext_face, tag_face = cipher_face.encrypt_and_digest(cube_face_bytes)
    encrypted_cube_face_part = salt_face + cipher_face.nonce + tag_face + ciphertext_face
    encrypted_cube_face_b64 = base64.b64encode(encrypted_cube_face_part).decode()
    
    # --- Encrypt the Main Message ---
    salt_message = os.urandom(16)
    key_message = derive_key_message(password, cube_face, salt_message)
    cipher_message = AES.new(key_message, AES.MODE_GCM)
    ciphertext_message, tag_message = cipher_message.encrypt_and_digest(plaintext.encode())
    hmac_value = hmac.new(key_message, ciphertext_message, hashlib.sha256).digest()
    encrypted_message_part = salt_message + cipher_message.nonce + tag_message + hmac_value + ciphertext_message
    encrypted_message_b64 = base64.b64encode(encrypted_message_part).decode()
    
    # Combine the two parts using a double-colon separator
    final = encrypted_cube_face_b64 + "::" + encrypted_message_b64
    return final

def decrypt_message(encrypted_text: str, password: str) -> str:
    """
    Decrypts the ciphertext by reversing the encryption steps:
    
    1. Split the input on "::" to extract the encrypted cube face and the main encrypted message.
    2. Decrypt the cube face part:
       - Base64‑decode, extract salt, nonce, tag, and ciphertext.
       - Derive key_face from the password and salt.
       - Decrypt to recover the original cube face string.
    3. Using the recovered cube face, decrypt the main message:
       - Base64‑decode and extract salt, nonce, tag, HMAC, and ciphertext.
       - Derive key_message using password and the recovered cube face.
       - Verify the HMAC.
       - Decrypt and verify the ciphertext to recover the plaintext.
    """
    try:
        encrypted_cube_face_b64, encrypted_message_b64 = encrypted_text.split("::", 1)
        
        # --- Decrypt the Cube Face ---
        encrypted_cube_face_part = base64.b64decode(encrypted_cube_face_b64)
        salt_face = encrypted_cube_face_part[:16]
        nonce_face = encrypted_cube_face_part[16:32]
        tag_face = encrypted_cube_face_part[32:48]
        ciphertext_face = encrypted_cube_face_part[48:]
        key_face = derive_key_face(password, salt_face)
        cipher_face = AES.new(key_face, AES.MODE_GCM, nonce=nonce_face)
        cube_face = cipher_face.decrypt_and_verify(ciphertext_face, tag_face).decode()
        
        # --- Decrypt the Main Message ---
        encrypted_message_part = base64.b64decode(encrypted_message_b64)
        salt_message = encrypted_message_part[:16]
        nonce_message = encrypted_message_part[16:32]
        tag_message = encrypted_message_part[32:48]
        hmac_value = encrypted_message_part[48:80]  # 32 bytes for HMAC-SHA256
        ciphertext_message = encrypted_message_part[80:]
        key_message = derive_key_message(password, cube_face, salt_message)
        expected_hmac = hmac.new(key_message, ciphertext_message, hashlib.sha256).digest()
        if not hmac.compare_digest(expected_hmac, hmac_value):
            raise ValueError("HMAC authentication failed! Possible tampering detected.")
        cipher_message = AES.new(key_message, AES.MODE_GCM, nonce=nonce_message)
        plaintext = cipher_message.decrypt_and_verify(ciphertext_message, tag_message).decode()
        return plaintext
    except Exception as e:
        return f"Decryption error: {e}"

# --- Helper Functions for Rubik's Cube Theme ---

def generate_face():
    """
    Generates a random 3x3 Rubik's Cube face using colors:
    'R' (red), 'G' (green), 'B' (blue), 'Y' (yellow), 'O' (orange), 'W' (white).
    """
    COLORS = ['R', 'G', 'B', 'Y', 'O', 'W']
    ROWS, COLS = 3, 3
    return [[random.choice(COLORS) for _ in range(COLS)] for _ in range(ROWS)]

def face_to_string(face):
    """
    Converts the 2D Rubik's Cube face (list of lists) into a single string.
    For example, a 3x3 face [['R','G','B'],['Y','O','W'],['R','G','B']]
    becomes "RGBYOWRGB".
    """
    return ''.join(''.join(row) for row in face)
