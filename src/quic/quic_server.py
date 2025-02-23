import asyncio
import logging
from aioquic.asyncio import QuicConnectionProtocol, serve
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import DatagramFrameReceived, ConnectionTerminated

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("server")

class VideoServerProtocol(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel = asyncio.Queue()
        self.sequence_number = 0  # Paket sıra numarasını takip etmek için
        logger.info("New connection established.")

    async def broadcast(self):
        while True:
            data = await self.channel.get()
            for connection in self._quic._connections.values():
                connection.send_datagram_frame(data)
            logger.info(f"Broadcasted packet: {data[:10]}...")

    def quic_event_received(self, event):
        if isinstance(event, DatagramFrameReceived):  # Sadece DatagramFrameReceived olaylarını işle
            self.sequence_number += 1  # Her paket için sıra numarasını artır
            self.channel.put_nowait(event.data)
            logger.info(f"Received packet with sequence: {self.sequence_number}, data: {event.data[:10]}...")
        elif isinstance(event, ConnectionTerminated):  # Bağlantı sonlandığında log at
            logger.info(f"Connection closed: {event}")

async def run_server():
    configuration = QuicConfiguration(is_client=False)
    configuration.load_cert_chain('ssl/certificate.pem', 'ssl/private.key')
    configuration.verify_mode = 0  # Doğrulamayı devre dışı bırak

    server = await serve(
        '127.0.0.1', 4433, configuration=configuration, create_protocol=VideoServerProtocol
    )
    logger.info("Server started on 127.0.0.1:4433")
    await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(run_server())