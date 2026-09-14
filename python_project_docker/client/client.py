import socket
import time

HOST = "python_server"
PORT = 9999

time.sleep(1)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"Hello from client")
    data = s.recv(1024)
    print("Received:", data.decode())
