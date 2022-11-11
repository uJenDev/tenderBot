
import socket
import os

def clear():
    os.system('clear')

is_local = False

HOST = "127.0.0.1" if is_local else '192.168.12.52'  # The server's hostname or IP address
PORT = 14000  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    connectionResponse = s.recv(1024).decode()
    clear()
    print(f"{connectionResponse}")
    msg = ''
    while True:
        msg = input('Enter command: ')
        if msg == '':
            msg = ' '
        s.sendall(msg.encode())
        if msg == '8':
            print('Exiting')
            break
        data = s.recv(1024).decode()
        clear()
        print(data)
    s.close()