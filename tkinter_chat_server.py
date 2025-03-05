import customtkinter as ctk
import socket
import threading
import database
from encryption import encrypt_message, decrypt_message, generate_face, face_to_string

class ChatServer(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Secure Chat Server")
        self.geometry("500x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Chat Display
        self.chat_display = ctk.CTkTextbox(self, width=480, height=400, wrap="word")
        self.chat_display.pack(padx=10, pady=10)
        self.chat_display.configure(state="disabled")

        # Message Entry
        self.msg_entry = ctk.CTkEntry(self, width=400, placeholder_text="Type your message...")
        self.msg_entry.pack(padx=10, pady=5)
        self.msg_entry.bind("<Return>", self.send_message)

        # Send Button
        self.send_button = ctk.CTkButton(self, text="Send", command=self.send_message)
        self.send_button.pack(pady=10)

        # Ask for password
        self.password = ctk.CTkInputDialog(text="Enter encryption password:", title="Password").get_input()

        # Start the server in a separate thread
        self.server_thread = threading.Thread(target=self.start_server, daemon=True)
        self.server_thread.start()

    def start_server(self):
        """Handles server setup and waits for a client connection."""
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('0.0.0.0', 9999))  # Use server's IP if needed
        self.server.listen()

        self.display_message("Server is listening on port 9999...")
        
        self.client, self.addr = self.server.accept()
        self.display_message(f"Connected by {self.addr}")

        # Start receiving messages in a separate thread
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_message(self, event=None):
        msg = self.msg_entry.get().strip()
        if msg:
            cube_face = generate_face()
            cube_face_str = face_to_string(cube_face)
            encrypted_msg = encrypt_message(msg, self.password, cube_face_str)
            self.client.send(encrypted_msg.encode('utf-8'))
            self.display_message(f"Server: {msg}")
            self.msg_entry.delete(0, "end")
            if msg.lower() == "convo-quit":
                self.client.close()
                self.server.close()
                self.quit()

    def receive_messages(self):
        while True:
            try:
                encrypted_msg = self.client.recv(1024).decode('utf-8').strip()
                if not encrypted_msg:
                    break
                decrypted_msg = decrypt_message(encrypted_msg, self.password).strip()
                database.save_to_db(encrypted_msg, "Server")
                self.display_message(f"Client: {decrypted_msg}")
            except Exception as e:
                self.display_message(f"Error: {e}")
                break

    def display_message(self, message):
        """Safely update the GUI from a different thread."""
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", message + "\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")

if __name__ == "__main__":
    database.init_db()
    app = ChatServer()
    app.mainloop()