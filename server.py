import socket
from Faces import encrypt_message, decrypt_message
import database

manual_decryption = False  # default is automatic decryption

def main():
    global manual_decryption
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 9999))
    server.listen()
    
    client, addr = server.accept()
    print("Connected by", addr)
    
    database.init_db()
    
    done = False
    while not done:
        msg = client.recv(4096).decode('utf-8')
        if msg.lower() == "convo-quit":
            print("Conversation quit command received from client.")
            done = True
            client.send("convo-quit".encode('utf-8'))
            continue
        
        # Decrypt the incoming message if in automatic mode
        try:
            if not manual_decryption:
                decrypted = decrypt_message(msg)
                print("Decrypted message from client:", decrypted)
            else:
                print("Encrypted message from client:", msg)
        except Exception as e:
            print("Error during decryption:", e)
        
        response = input("Message: ")
        
        # Process control commands locally
        if response.lower() == "decrypt-manual-on":
            manual_decryption = True
            print("Manual decryption mode activated.")
            continue
        elif response.lower() == "decrypt-manual-off":
            manual_decryption = False
            print("Automatic decryption mode activated.")
            continue
        elif response.lower() == "convo-quit":
            client.send("convo-quit".encode('utf-8'))
            done = True
            continue
        
        encrypted_response = encrypt_message(response)
        database.save_to_db(encrypted_response)
        client.send(encrypted_response.encode('utf-8'))
    
    client.close()
    server.close()

if __name__ == "__main__":
    main()
