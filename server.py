import socket
import threading
import sys
import database
from Faces import encrypt_message, decrypt_message, generate_face, face_to_string

def receive_messages(client_sock, password):
    while True:
        try:
            encrypted_msg = client_sock.recv(1024).decode('utf-8').strip()
            if not encrypted_msg:
                print("\nConnection closed by the client.")
                break

            decrypted_msg = decrypt_message(encrypted_msg, password).strip()
            if decrypted_msg.lower() == "convo-quit":
                print("\nConversation ended by remote.")
                break

            # Save the incoming message
            database.save_to_db(encrypted_msg)

            sys.stdout.write(f"\r\nReceived: {decrypted_msg}\n")
            sys.stdout.write("Message: ")
            sys.stdout.flush()
        except Exception as e:
            print("Error receiving:", e)
            break

def main():
    database.init_db()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen()
    print("Server is listening on port 9999...")

    password = input("Enter encryption password for server session: ")

    client, addr = server.accept()
    print("Connected by", addr)

    threading.Thread(target=receive_messages, args=(client, password), daemon=True).start()

    while True:
        msg = input("Message: ")
        if msg.lower() == "convo-quit":
            cube_face = generate_face()
            cube_face_str = face_to_string(cube_face)
            encrypted_quit = encrypt_message(msg, password, cube_face_str)
            client.send(encrypted_quit.encode('utf-8'))
            print("Conversation ended.")
            break

        cube_face = generate_face()
        cube_face_str = face_to_string(cube_face)
        encrypted = encrypt_message(msg, password, cube_face_str)
        client.send(encrypted.encode('utf-8'))

    client.close()
    server.close()

if __name__ == "__main__":
    main()
