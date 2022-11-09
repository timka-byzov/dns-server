import asyncio

from dns_server.server import EchoServerProtocol


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

    try:
        await asyncio.sleep(3600)  # Serve for 1 hour.
    finally:
        server_transport.close()


asyncio.run(main())
