import asyncio

from local_api import LocalAPI


class EchoClientProtocol:
    def __init__(self, on_con_lost=None):
        # self.on_con_lost = on_con_lost
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        # print('Send:', self.message)
        # self.transport.sendto(self.message)

    def datagram_received(self, data, addr):
        print("Received in client:", data)

        # print("Close the socket")
        # self.transport.close()

    def error_received(self, exc):
        print('Error received:', exc)

    def connection_lost(self, exc):
        print("Connection closed")
        # self.on_con_lost.set_result(True)


# async def run_sender_loop():
#     # Get a reference to the event loop as we plan to use
#     # low-level APIs.
#     loop = asyncio.get_running_loop()
#
#     on_con_lost = loop.create_future()
#     # message = "Hello World!"
#
#     transport, protocol = await loop.create_datagram_endpoint(
#         lambda: EchoClientProtocol(on_con_lost),
#         remote_addr=("198.41.0.4", 53))
#
#     LocalAPI.sender_transport = transport
#
#     try:
#         await on_con_lost
#     finally:
#         transport.close()
