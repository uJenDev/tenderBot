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
                data = conn.recv(1024).decode()
                if not data or data == b"done":
                    break
                x, y = data[:4], data[4:]
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