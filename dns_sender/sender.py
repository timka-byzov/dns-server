import asyncio
import socket
import time

from cache.cache_utils import Cache
from dns_response.dns_response import DNSResponse
from utils import get_ipv4s


class Sender:
    def __init__(self, server_transport: asyncio.DatagramTransport, client_addr):
        self.server_transport = server_transport
        self.client_addr = client_addr

    def send_udp_message(self, message, addr):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.sendto(message, addr)
            bin_data, addr = sock.recvfrom(4000)
        finally:
            sock.close()
        return bin_data, addr

    def make_request(self, message):
        curr_ip = "198.41.0.4"

        while True:

            cache_data = Cache.get_cache(curr_ip, message)

            if cache_data is None:
                bin_response, _ = self.send_udp_message(message, (curr_ip, 53))
            else:
                bin_response = cache_data

            response = DNSResponse(bin_response)
            if cache_data is None:
                Cache.refresh_cache(curr_ip, message, response)

            # server is authority for domain or PTR response
            if response.flags[0] & 0x04 or response.query['type'] == b'\x00\x0c' or \
                    response.additional_records_count == 0:

                # print(curr_ip)
                self.server_transport.sendto(bin_response, self.client_addr)
                return

            else:
                curr_ip = get_ipv4s(response.additional_records)[0]
