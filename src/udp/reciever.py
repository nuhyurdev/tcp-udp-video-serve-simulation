import socket
import time
import argparse

BUFFER_SIZE = 1024 + 10  # Paket numarası için ek alan

def receive_video(receiver_ip, receiver_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((receiver_ip, receiver_port))
    
    received_packets = 0
    total_data_received = 0
    first_packet_received = False
    total_packets = 0
    received_packet_numbers = set()  # Alınan paket numaralarını takip etmek için
    
    # İlk paket: Toplam paket sayısı
    data, addr = sock.recvfrom(BUFFER_SIZE)
    if data.startswith(b"total:"):
        total_packets = int(data.decode().split(":")[1])
        print(f"Total packets to receive: {total_packets}")
    
    while len(received_packet_numbers) < total_packets:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        try:
            packet_number = int(data.split(b":")[0].decode())  # Paket numarasını al
            
            if packet_number not in received_packet_numbers:
                received_packet_numbers.add(packet_number)
                received_packets += 1
                total_data_received += len(data)
                
                if not first_packet_received:
                    print(f"First packet received: {packet_number}")
                    first_packet_received = True
                    start_time = time.time()

                
                print(f"Received packet {packet_number}/{total_packets}")
                
                # Son paket kontrolü
                if packet_number == total_packets:
                    print(f"Last packet received: {packet_number}")
                    break  # Döngüden çık
        except UnicodeDecodeError:
            print(f"Received binary data packet")
    
    # İstatistikleri hesapla ve göster
    end_time = time.time()
    elapsed_time = end_time - start_time
    average_speed = (total_data_received / elapsed_time) / 1024  # KB/s cinsinden
    
    print("\n--- Receiver Statistics ---")
    print(f"Total packets received: {received_packets}")
    print(f"Total data received: {total_data_received} bytes")
    print(f"Total receiving time: {elapsed_time:.2f} seconds")
    print(f"Average receiving speed: {average_speed:.2f} KB/s")
    
    # Bağlantıyı kapat
    sock.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Receive video from server.")
    parser.add_argument("--ip", type=str, default="127.0.0.1", help="Receiver IP address.")
    parser.add_argument("--port", type=int, required=True, help="Receiver port number.")
    args = parser.parse_args()
    
    receive_video(args.ip, args.port)