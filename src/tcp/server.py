import socket
import argparse
from threading import Thread

BUFFER_SIZE = 1024  # Paket boyutu

clients = []  # Bağlı tüm receiver'ları tutmak için

def handle_client(conn, addr):
    print(f"New connection from {addr}")
    clients.append(conn)
    while True:
        try:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            # Veriyi tüm receiver'lara yayınla
            for client in clients:
                if client != conn:  # Gönderen hariç
                    client.send(data)
        except ConnectionResetError:
            break
    print(f"Connection closed: {addr}")
    clients.remove(conn)
    conn.close()

def broadcast(server_ip, server_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((server_ip, server_port))
    sock.listen(5)
    print(f"Server is listening on {server_ip}:{server_port}...")
    
    while True:
        conn, addr = sock.accept()
        Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Broadcast video packets using TCP.")
    parser.add_argument("--ip", type=str, default="127.0.0.1", help="Server IP address.")
    parser.add_argument("--port", type=int, required=True, help="Server port number.")
    args = parser.parse_args()
    
    broadcast(args.ip, args.port)