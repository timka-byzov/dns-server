import asyncio

from dns_sender.sender import EchoClientProtocol
from dns_server.server import EchoServerProtocol
from local_api import LocalAPI


async def main():
    print("Starting UDP server")

    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    # One protocol instance will be created to serve all
    # client requests.
    server_transport, server_protocol = await loop.create_datagram_endpoint(
        lambda: EchoServerProtocol(),
        local_addr=('127.0.0.1', 53))
    client_transport, client_protocol = await loop.create_datagram_endpoint(
        lambda: EchoClientProtocol(),
        remote_addr=("198.41.0.4", 53))

    LocalAPI.init(server_transport, client_transport)

    try:
        await asyncio.sleep(3600)  # Serve for 1 hour.
    finally:
        server_transport.close()


asyncio.run(main())
