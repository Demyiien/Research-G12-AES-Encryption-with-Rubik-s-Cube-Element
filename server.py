import socket
import database

print("Creating server socket...")
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Binding to port 9999...")
try:
    server.bind(('0.0.0.0', 9999))
    print("✅ Server successfully bound to port 9999.")
except OSError as e:
    print(f"❌ Error binding socket: {e}")
    exit(1)

print("Server is now listening...")
server.listen()
print("✅ Server is actively listening on port 9999...")

while True:  # Keeps server alive
    client, addr = server.accept()
    print(f"Connected by {addr}")
