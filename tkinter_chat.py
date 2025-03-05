import customtkinter as ctk
import socket
import threading
import database
from encryption import encrypt_message, decrypt_message, generate_face, face_to_string

class ChatClient(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Secure Chat")
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

        # Setup Client
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('127.0.0.1', 9999))
        self.password = ctk.CTkInputDialog(text="Enter encryption password:", title="Password").get_input()

        threading.Thread(target=self.receive_messages, daemon=True).start()
    
    def send_message(self, event=None):
        msg = self.msg_entry.get().strip()
        if msg:
            cube_face = generate_face()
            cube_face_str = face_to_string(cube_face)
            encrypted_msg = encrypt_message(msg, self.password, cube_face_str)
            self.client.send(encrypted_msg.encode('utf-8'))
            self.display_message(f"You: {msg}")
            self.msg_entry.delete(0, "end")
            if msg.lower() == "convo-quit":
                self.client.close()
                self.quit()
    
    def receive_messages(self):
        while True:
            try:
                encrypted_msg = self.client.recv(1024).decode('utf-8').strip()
                if not encrypted_msg:
                    break
                decrypted_msg = decrypt_message(encrypted_msg, self.password).strip()
                database.save_to_db(encrypted_msg, "Client")
                self.display_message(f"Received: {decrypted_msg}")
            except Exception as e:
                self.display_message(f"Error: {e}")
                break
    
    def display_message(self, message):
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", message + "\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")

if __name__ == "__main__":
    database.init_db()
    app = ChatClient()
    app.mainloop()
