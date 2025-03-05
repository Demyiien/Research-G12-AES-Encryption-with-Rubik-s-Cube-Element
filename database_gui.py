import customtkinter as ctk
import database

class DatabaseGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Database Manager")
        self.geometry("500x500")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Centered Frame
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(expand=True)

        # Title Label
        self.label = ctk.CTkLabel(self.frame, text="Database Records", font=("Arial", 18))
        self.label.pack(pady=10)

        # Scrollable Textbox for Records
        self.textbox = ctk.CTkTextbox(self.frame, width=450, height=300, wrap="word")
        self.textbox.pack(pady=10)
        self.textbox.configure(state="disabled")

        # Buttons
        self.update_button = ctk.CTkButton(self.frame, text="Update Records", command=self.view_records)
        self.update_button.pack(pady=5)

        self.clear_button = ctk.CTkButton(self.frame, text="Clear Database", command=self.clear_database)
        self.clear_button.pack(pady=5)

        self.exit_button = ctk.CTkButton(self.frame, text="Exit", command=self.quit)
        self.exit_button.pack(pady=5)

        # Auto-load records on startup
        self.view_records()
    
    def view_records(self):
        records = database.get_records()
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        if records:
            for index, record in enumerate(records, start=1):
                timestamp = record[1]  # Assuming timestamp is stored as the second field
                message = record[2]  # Assuming message is stored as the third field
                sender = "Server" if record[3] == "Client" else "Client"  # Correct sender swapping
                
                # Apply color formatting
                self.textbox.insert("end", f"[{index}] ", ("message_number",))
                self.textbox.insert("end", f"[{timestamp}] ", ("timestamp",))
                self.textbox.insert("end", f"[{sender}] ", ("client" if sender == "Client" else "server",))
                self.textbox.insert("end", f"{message}\n\n")
                
            # Define tag styles
            self.textbox.tag_config("message_number", foreground="green")
            self.textbox.tag_config("timestamp", foreground="orange")
            self.textbox.tag_config("server", foreground="yellow")
            self.textbox.tag_config("client", foreground="#89CFF0")  # Lighter blue for client
        else:
            self.textbox.insert("end", "No records found.\n")
        self.textbox.configure(state="disabled")
    
    def clear_database(self):
        database.clear_database()
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        self.textbox.insert("end", "All records have been deleted.\n")
        self.textbox.configure(state="disabled")
    
if __name__ == "__main__":
    database.init_db()
    app = DatabaseGUI()
    app.mainloop()
