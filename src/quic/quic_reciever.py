import asyncio
import logging
import time
from aioquic.asyncio import connect
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import DatagramFrameReceived

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("receiver")

class VideoReceiverProtocol(asyncio.DatagramProtocol):
    def __init__(self):
        self.total_packets = 0
        self.total_bytes = 0
        self.start_time = None

    def datagram_received(self, data, addr):
        # İlk paket alındığında zamanlamayı başlat
        if self.start_time is None:
            self.start_time = time.time()
            logger.info("First packet received, timing started.")

        self.total_packets += 1
        self.total_bytes += len(data)
        logger.info(f"Received packet {self.total_packets} with {len(data)} bytes")

    def connection_lost(self, exc):
        # Son paket alındığında zamanlamayı durdur
        if self.start_time is not None:
            end_time = time.time()
            total_time = end_time - self.start_time
            avg_speed = (self.total_bytes / 1024) / total_time

            logger.info("--- Receiver Statistics ---")
            logger.info(f"Total packets received: {self.total_packets}")
            logger.info(f"Total data received: {self.total_bytes} bytes")
            logger.info(f"Total receiving time: {total_time:.2f} seconds")
            logger.info(f"Average receiving speed: {avg_speed:.2f} KB/s")
        else:
            logger.warning("No packets received.")

async def receive_video():
    configuration = QuicConfiguration(is_client=True)
    configuration.verify_mode = 0  # Doğrulamayı devre dışı bırak

    loop = asyncio.get_event_loop()
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: VideoReceiverProtocol(),
        remote_addr=('127.0.0.1', 4433)
    )

    try:
        logger.info("Connected to server")
        await asyncio.Future()  # Run forever
    except Exception as e:
        logger.error(f"Connection failed: {e}")
    finally:
        transport.close()

if __name__ == "__main__":
    asyncio.run(receive_video())