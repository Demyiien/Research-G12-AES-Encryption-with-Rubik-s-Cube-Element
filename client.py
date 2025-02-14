import socket
import threading
import sys
import database
from Faces import encrypt_message, decrypt_message

def receive_messages(sock):
    while True:
        try:
            encrypted_msg = sock.recv(1024).decode('utf-8').strip()
            if not encrypted_msg:
                print("\nConnection closed by the server.")
                break

            # Decrypt the incoming message and strip extra whitespace
            decrypted_msg = decrypt_message(encrypted_msg).strip()
            if decrypted_msg.lower() == "convo-quit":
                print("\nConversation ended by remote.")
                break

            # Save the received message (this includes echoes from your own messages)
            database.save_to_db(encrypted_msg)

            sys.stdout.write(f"\r\nReceived: {decrypted_msg}\n")
            sys.stdout.write("Message: ")
            sys.stdout.flush()
        except Exception as e:
            print("Error receiving:", e)
            break

def main():
    database.init_db()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('192.168.254.101', 9999))  # adjust IP as needed
    print("Connected to server!")

    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

    while True:
        msg = input("Message: ")
        if msg.lower() == "convo-quit":
            encrypted_quit = encrypt_message(msg)
            client.send(encrypted_quit.encode('utf-8'))
            # Optionally, you may also save the quit message here if desired
            print("Conversation ended.")
            break

        encrypted = encrypt_message(msg)
        # Do not call database.save_to_db here—let the receiving thread store the echo.
        client.send(encrypted.encode('utf-8'))

    client.close()

if __name__ == "__main__":
    main()
