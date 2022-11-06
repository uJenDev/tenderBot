
import socket

is_local = True

HOST = "127.0.0.1" if is_local else '192.168.1.2'  # The server's hostname or IP address
PORT = 2222  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    connectionResponse = s.recv(1024).decode()
    print(f"{connectionResponse}")
    msg = ''
    while msg != 'exit':
        msg = input('Enter command: ')
        s.sendall(msg.encode())
        data = s.recv(1024).decode()
        print(f"{data}")
    s.close()