import socket
import argparse

BUFFER_SIZE = 1024 + 10  # Paket numarası için ek alan

def broadcast(server_ip, server_port, receiver_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((server_ip, server_port))
    
    print(f"Server is listening on {server_ip}:{server_port}...")
    
    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        try:
            # İlk paket: Toplam paket sayısı
            if data.startswith(b"total:"):
                packet_info = data.decode()
                print(f"Received total packet info: {packet_info}")
            else:
                # Diğer paketler
                packet_number = data.split(b":")[0].decode()  # Paket numarasını al
                print(f"Received packet {packet_number} from {addr}")
        except UnicodeDecodeError:
            print(f"Received binary data packet from {addr}")
        
        # Paketi receiver'a ilet
        sock.sendto(data, (server_ip, receiver_port))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Broadcast video packets.")
    parser.add_argument("--ip", type=str, default="127.0.0.1", help="Server IP address.")
    parser.add_argument("--port", type=int, required=True, help="Server port number.")
    parser.add_argument("--receiver_port", type=int, required=True, help="Receiver port number.")
    args = parser.parse_args()
    
    broadcast(args.ip, args.port, args.receiver_port)