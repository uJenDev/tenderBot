import socket
import time

HOST = "127.0.0.1"
PORT = 2222

time_to_serve = 2

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        try:
            print(f"Connected by {addr}")
            while True:
                x = conn.recv(1024).decode()
                conn.sendall(f"Received: {x}".encode())
                y = conn.recv(1024).decode()
                conn.sendall(f"Received: {y}".encode())
                drinkNum = conn.recv(1024).decode()
                conn.sendall(f"Received: {drinkNum}".encode())

                print(f'Received x: {x}, y: {y}, drinkNum: {drinkNum}')

                time.sleep(time_to_serve)
                conn.sendall(b"COMPLETE")
        except Exception as e:
            print(e)
            conn.close()
            s.close()
    if conn:
        conn.close()
    if s:
        s.close()