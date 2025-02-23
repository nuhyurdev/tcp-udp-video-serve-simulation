import asyncio
import logging
import time
from aioquic.asyncio import connect
from aioquic.quic.configuration import QuicConfiguration

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sender")

async def send_video():
    configuration = QuicConfiguration(is_client=True)
    configuration.verify_mode = 0  # Doğrulamayı devre dışı bırak

    try:
        async with connect('127.0.0.1', 4433, configuration=configuration) as client:
            logger.info("Connected to server")

            with open('../../docs/video.mp4', 'rb') as file:
                total_packets = 0
                total_bytes = 0
                start_time = None

                while True:
                    data = file.read(1024)
                    if not data:
                        break

                    # İlk paket gönderildiğinde zamanlamayı başlat
                    if start_time is None:
                        start_time = time.time()
                        logger.info("First packet sent, timing started.")

                    client._quic.send_datagram_frame(data)
                    total_packets += 1
                    total_bytes += len(data)
                    logger.info(f"Sent packet {total_packets} with {len(data)} bytes")

                # Son paket gönderildiğinde zamanlamayı durdur
                if start_time is not None:
                    end_time = time.time()
                    total_time = end_time - start_time
                    avg_speed = (total_bytes / 1024) / total_time

                    logger.info("--- Sender Statistics ---")
                    logger.info(f"Total packets sent: {total_packets}")
                    logger.info(f"Total data sent: {total_bytes} bytes")
                    logger.info(f"Total sending time: {total_time:.2f} seconds")
                    logger.info(f"Average sending speed: {avg_speed:.2f} KB/s")
                else:
                    logger.warning("No packets sent.")
    except Exception as e:
        logger.error(f"Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(send_video())