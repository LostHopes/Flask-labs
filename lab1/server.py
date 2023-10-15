import socket
import time
import os
import threading

def handle_client(conn, addr, users):
    connection_time = time.strftime("%D - %H:%M:%S", time.localtime())
    users.append(conn)
    print(f'User {os.getlogin()} with ip {addr} connected to the server in [{connection_time}]\
        \nUsers online: {len(users)}')
    while True:
        data = conn.recv(1024)
        if not data:
            users.remove(conn)
            print(f"User {os.getlogin()} with ip {addr} disconnected from the server\
                \nUsers online: {len(users)}")
            break
        recv_time = time.strftime("%D - %H:%M:%S", time.localtime())
        print(f'{os.getlogin()}: {data.decode()} [{recv_time}]')
        for user in users:
            if user != conn:
                user.sendall(data)
    conn.close()

def recv(host, port):
    users = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(5)
        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr, users))
            t.start()

def main():
    host = 'localhost'
    port = 65333
    recv(host, port)

main()

