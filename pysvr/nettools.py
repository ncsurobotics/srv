import pickle
import socket
from srv_settings import client_ip_port
from srv_settings import server_ip_port
from srv_settings import IMG_BUFFER

"""Sends requests to the server."""
class RequestSender(object):
    """The socket that requests will be sent through"""
    sock = []

    """Initialize the RequestSender."""
    def __init__(self, **kwargs):
        sock = kwargs.get('sock', None)
        if sock:
            self.sock = sock
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind(client_ip_port)
        return

    """Send a request."""
    def send(self, request):
        self.sock.sendto(pickle.dumps(request), server_ip_port)
        return

    """Attempt to recieve a response.
When no request is recieved, throw the exception
socket.timeout."""
    def receive(self):
        data, _ = self.sock.recvfrom(IMG_BUFFER)
        return pickle.loads(data)

class RequestReceiver(object):
    """The socket that requests will be sent through"""
    sock = []

    """Initialize the RequestReceiver."""
    def __init__(self, **kwargs):
        sock = kwargs.get('sock', None)
        if sock:
            self.sock = sock
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind(server_ip_port)
        return

    """Send some data.
Assume the data is already pickled."""
    def send(self, data, pickled=True):
        if pickled:
            self.sock.sendto(data, client_ip_port)
        else:
            self.sock.sendto(pickle.dumps(data), client_ip_port)
        return


    """Receive a request and the address as a tuple.
When no request is recieved, throw the exception
socket.timeout."""
    def receive(self):
        data, addr = self.sock.recvfrom(IMG_BUFFER)
        return pickle.loads(data), addr
