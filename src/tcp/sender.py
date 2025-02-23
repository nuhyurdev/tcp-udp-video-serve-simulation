import socket
import time
import os
import argparse

BUFFER_SIZE = 1024

def send_video(file_path, server_ip, server_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip, server_port))
    
    file_size = os.path.getsize(file_path)
    total_packets = (file_size // BUFFER_SIZE) + 1
    start_time = time.time()
    total_data_sent = 0
    
    # İlk paket olarak toplam paket sayısını gönder
    sock.send(f"total:{total_packets}".encode())
    
    with open(file_path, "rb") as f:
        for i in range(total_packets):
            data = f.read(BUFFER_SIZE)
            sock.send(data)  # Sadece veriyi gönder
            total_data_sent += len(data)
            print(f"Sent packet {i+1}/{total_packets}")
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    average_speed = (total_data_sent / elapsed_time) / 1024  # KB/s cinsinden
    
    print("\n--- Sender Statistics ---")
    print(f"Total packets sent: {total_packets}")
    print(f"Total data sent: {total_data_sent} bytes")
    print(f"Total sending time: {elapsed_time:.2f} seconds")
    print(f"Average sending speed: {average_speed:.2f} KB/s")
    
    # Bağlantıyı kapat
    sock.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send video to server using TCP.")
    parser.add_argument("--file", type=str, required=True, help="Path to the video file.")
    parser.add_argument("--ip", type=str, default="127.0.0.1", help="Server IP address.")
    parser.add_argument("--port", type=int, required=True, help="Server port number.")
    args = parser.parse_args()
    
    send_video(args.file, args.ip, args.port)