import asyncio

from dns_response.dns_response import DNSResponse
from local_api import LocalAPI
from utils import get_ipv4s


class EchoClientProtocol(asyncio.DatagramProtocol):
    def __init__(self, on_con_lost=None):
        self.on_con_lost = on_con_lost
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        print("Received in client:", data)

        dns_response = DNSResponse(data)
        ips = get_ipv4s(dns_response.authority_records)

        if dns_response.flags[0] & 0x04 or not ips:
            LocalAPI.resend_dns_response_to_client(data)
            return

        # LocalAPI.send_dns_request(data, (ips[0], 53))

        # LocalAPI.resend_dns_response_to_client(data)
