import pickle
import socket
from srv_settings import client_ip_port
from srv_settings import server_ip_port
from srv_settings import IMG_BUFFER

"""Mailbox provides common methods for
sending and receiving requests and data."""
class Mailbox(object):
    """The socket that requests and data will be sent through and received"""
    sock = []
    
    """Initialize the mailbox"""
    def __init__(self, **kwargs):
        with_sock = kwargs.get('sock', None)
        with_ip_and_port = kwargs.get('ip_and_port', None)
        if with_sock:
            self.sock = with_sock
        elif with_ip_and_port is not None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind(with_ip_and_port)
        else:
            raise ValueError("No socket nor ip and port given")
        return

    """Send the request to the to_ip_port location. Pickle the request if it is not pickled."""
    def send(self, request, to_ip_port, pickled):
        if pickled:
            self.sock.sendto(request, to_ip_port)
        else:
            self.send(pickle.dumps(request), to_ip_port, False)
        return
    
    """Receive data, fitting it into buffersize.."""
    def receive(self, request, buffersize):
        return self.sock.recvfrom(buffersize)

        
"""Sends requests to the server."""
class RequestSender(object):
    """The mailbox that requests will be sent through"""
    mailbox = []

    """Initialize the RequestSender."""
    def __init__(self, **kwargs):
        sock = kwargs.get('sock', None)
        self.mailbox = Mailbox(with_sock=sock) if sock else Mailbox(with_ip_and_port=client_ip_port)
        return

    """Send a request."""
    def send(self, request):
        self.mailbox.send(request, server_ip_port, False)
        return

    """Attempt to recieve a response. When no request is recieved, throw the exception socket.timeout."""
    def receive(self):
        data, _ = self.mailbox.receive(IMG_BUFFER)
        return pickle.loads(data)


class RequestReceiver(object):
    """The mailbox that requests will be received through"""
    mailbox = []

    """The mailbox of the """

    """Initialize the RequestReceiver."""
    def __init__(self, **kwargs):
        sock = kwargs.get('sock', None)
        self.mailbox = Mailbox(with_sock=sock) if sock else Mailbox(with_ip_and_port=server_ip_port)
        return

    """Send some data.
Assume the data is already pickled.
If the data is not already pickled,
set the pickled option to False."""
    def send(self, data, pickled=True):
        self.mailbox.send(data, client_ip_port, pickled)
        return


    """Receive a request and the address as a tuple.
When no request is recieved, throw the exception
socket.timeout."""
    def receive(self):
        data, addr = self.mailbox.receive(IMG_BUFFER)
        return pickle.loads(data), addr
