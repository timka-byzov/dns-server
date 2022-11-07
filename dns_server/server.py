import asyncio

from local_api import LocalAPI


class EchoServerProtocol:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        a = 0
        # message = data.decode()
        print(data)
        print('Received from %s' % (addr,))

        # return data

        # self.transport.sendto(data, addr)
        LocalAPI.sender_transport.sendto(data)


