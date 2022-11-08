import asyncio


class LocalAPI:
    server_transport: asyncio.DatagramTransport = None
    intermediate_client_transport: asyncio.DatagramTransport = None

    addr_queue = []

    @staticmethod
    def init(server_transport, intermediate_client_transport):
        LocalAPI.server_transport = server_transport
        LocalAPI.intermediate_client_transport = intermediate_client_transport

    @staticmethod
    def send_dns_request(data: bytes, addr: tuple[str, int]):
        LocalAPI.addr_queue.append(addr)
        LocalAPI.intermediate_client_transport.sendto(data)

    # @staticmethod
    # def next_iteration(data, addr):
    #     LocalAPI.send_dns_request(data, addr)

    @staticmethod
    def resend_dns_response_to_client(data: bytes):
        LocalAPI.server_transport.sendto(data, LocalAPI.addr_queue.pop())
