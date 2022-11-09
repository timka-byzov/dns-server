import asyncio
from threading import Thread

from dns_sender.sender import Sender


class EchoServerProtocol(asyncio.DatagramProtocol):

    def __init__(self):
        self.transport = None

    def connection_made(self, transport: asyncio.DatagramTransport):
        self.transport = transport

    def datagram_received(self, data: bytes, addr: tuple[str, int]):
        # message = data.decode()
        # print(self.transport.get_extra_info("peername"))
        # print('Received from %s' % (addr,))
        #
        thread = Thread(target=Sender(self.transport, addr).make_request, args=(data,))
        thread.run()
