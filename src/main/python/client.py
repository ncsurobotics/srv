#!/usr/bin/env python2

import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 5005)

sock.sendto('message', server_address)

data, server = sock.recvfrom(5005)

print(data)

sock.close()
