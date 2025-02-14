import socket
from Faces import encrypt_message, decrypt_message
import database

manual_decryption = False  # automatic decryption is on by default

def main():
    global manual_decryption
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 9999))
    
    # Initialize the database
    database.init_db()
    
    done = False
    while not done:
        message = input("Message: ")
        
        # Process control commands locally
        if message.lower() == "decrypt-manual-on":
            manual_decryption = True
            print("Manual decryption mode activated.")
            continue
        elif message.lower() == "decrypt-manual-off":
            manual_decryption = False
            print("Automatic decryption mode activated.")
            continue
        elif message.lower() == "convo-quit":
            client.send("convo-quit".encode('utf-8'))
            done = True
            continue
        
        # Encrypt the outgoing message
        encrypted_message = encrypt_message(message)
        # Store the encrypted message in the database
        database.save_to_db(encrypted_message)
        client.send(encrypted_message.encode('utf-8'))
        
        # Wait for the response
        resp = client.recv(4096).decode('utf-8')
        if resp.lower() == "convo-quit":
            print("Conversation terminated by the other party.")
            done = True
        else:
            # If automatic decryption is enabled, try to decrypt before displaying
            try:
                if not manual_decryption:
                    decrypted = decrypt_message(resp)
                    print("Decrypted message:", decrypted)
                else:
                    print("Encrypted message:", resp)
            except Exception as e:
                print("Error during decryption:", e)
    
    client.close()

if __name__ == "__main__":
    main()
