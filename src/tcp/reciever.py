import socket
import time
import argparse
import struct

BUFFER_SIZE = 1024  # Paket boyutu

def receive_video(receiver_ip, receiver_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((receiver_ip, receiver_port))
    
    received_packets = 0
    total_data_received = 0
    total_packets = 63569  # Toplam paket sayısı sabit olarak belirlendi
    first =False
    print(f"Total packets to receive: {total_packets}")
    
    while received_packets < total_packets:
        # Veriyi al
        data = sock.recv(BUFFER_SIZE)
        if first == False:
            first = True
            start_time = time.time()
        
        if not data:
            break
        
        received_packets += 1
        total_data_received += len(data)
        
        print(f"Received packet {received_packets}/{total_packets}")
        
        # Son paket kontrolü
        if received_packets == total_packets:
            print(f"Last packet received: {received_packets}")
            break
    
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
    parser = argparse.ArgumentParser(description="Receive video from server using TCP.")
    parser.add_argument("--ip", type=str, default="127.0.0.1", help="Receiver IP address.")
    parser.add_argument("--port", type=int, required=True, help="Receiver port number.")
    args = parser.parse_args()
    
    receive_video(args.ip, args.port)