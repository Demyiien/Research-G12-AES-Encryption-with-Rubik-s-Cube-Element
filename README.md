# Research
Riemann Group 4 Research Project

Research Paper Link: https://docs.google.com/document/d/1O0sF0lla_NVeagtewmOVEpWJMTy-6t7o/edit?fbclid=IwZXh0bgNhZW0CMTEAAR07ZA-NS9-_yJlcosEyzj_RmvU1kginn7MkyvvfZDXkDPXZoDxS_vbbE_g_aem_ZnbAsAsL_Lzwo-C2Pgv9vg

**Rubik's Cube Encryption Chat System**
This project is a simple encrypted messaging system that uses a dynamic substitution cipher inspired by a Rubik’s Cube. It features a graphical display (via Pygame) of an animated Rubik’s Cube, real-time encrypted chat between a client and server, and logs all encrypted messages in a local SQLite database.

**Features**
Dynamic Encryption:
Uses a dynamic substitution cipher where each character is independently scrambled based on a random nonce and a pre‑agreed passphrase. Even identical messages result in different ciphertexts.

Real-Time Messaging:
The client and server can send messages concurrently without waiting for one another.

Database Logging:
All encrypted messages are stored in a SQLite database (encrypted_data.db) along with a timestamp.

Visual Rubik's Cube Display:
An animated Rubik’s Cube is displayed using Pygame to symbolize the encryption process.

**Control Commands:**

convo-quit: Ends the conversation.
database-view: Launches an animated view of the encrypted messages stored in the database.
database-clear: Clears the database.
decrypt-manual-on / decrypt-manual-off: Toggles automatic decryption in the visual interface.

**Requirements**
Python 3.10 or later
Pygame (pip install pygame)
Cryptography (pip install cryptography)
SQLite (included with Python's standard library)

**Project Files**
client.py – Runs the client-side chat program.
server.py – Runs the server-side chat program.
database.py – Contains functions to initialize and interact with the SQLite database.
Faces.py – Contains encryption/decryption functions and the Rubik’s Cube visualization code.

**Setup and Installation**

1. Clone or Download the Repository:
bash:
git clone https://github.com/yourusername/your-repository.git
cd your-repository

2. Install Dependencies:
bash:
pip install pygame cryptography

3. Ensure the Files Are Present:
Verify that client.py, server.py, database.py, and Faces.py are in the project folder.

**How to Run**

**Server**
1. On the machine that will act as the server, open a terminal and run:
bash:
python server.py
2. The server will bind to 0.0.0.0 on port 9999 (adjust in the code if needed) and wait for a client connection.

**Client**
1. On the machine that will act as the client, open a terminal and run:
bash
python client.py
2. In client.py, update the IP address (in client.connect(...)) to match the server’s IP if necessary.

**Faces (Visualization)**
To run the visual Rubik’s Cube and input interface (which supports control commands), execute:
bash
python Faces.py
This window shows an animated Rubik’s Cube and lets you enter commands (such as database-view to see animated database entries, or convo-quit to exit).

**Using the Chat System**

Sending Messages:
Type your message at the Message: prompt and press Enter. Your message is encrypted using a random, dynamic substitution cipher, then sent and stored in the database.

Receiving Messages:
Incoming messages are automatically decrypted and displayed. The system uses threads so you can type messages at any time.

**Control Commands:**

Type convo-quit to terminate the conversation.
Type database-view to launch an animated view of the encrypted messages stored in the database.
Type database-clear to clear the database.
Use decrypt-manual-on or decrypt-manual-off to toggle automatic decryption in the visualization.

**Notes**
One-to-One Chat:
The current implementation supports one client and one server (one-to-one messaging). To support group chats, the server must be modified to handle multiple client connections and broadcast messages.

Encryption Security:
While the dynamic substitution cipher provides obfuscation and ensures that identical plaintexts result in different ciphertexts, it is intended primarily for educational and demonstrative purposes. For production-grade security, consider using established cryptographic protocols.

Troubleshooting:

If the client cannot connect to the server, ensure that both devices are on the same network or configure your firewall accordingly.
Verify that your Python interpreter is correctly set up and that all dependencies are installed.
Check that you’re using the correct IP address in client.py.
