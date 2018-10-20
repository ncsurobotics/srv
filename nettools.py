import pickle
import socket
from srv_settings import IMG_BUFFER

"""Mailbox provides common methods for
sending and receiving requests and data."""
class MailBox(object):
    """The socket that requests and data will be sent through and received"""
    sock = []
    
    """Initialize the mailbox"""
    def __init__(self, ip_and_port=None, sock=None):
        if sock:
            self.sock = sock
        elif ip_and_port:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind(ip_and_port)
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            ip = socket.gethostbyname(socket.gethostname())
            found_port = False
            for port in range(5006,7006):
                try:
                    self.sock.bind((ip,port))
                    found_port = True
                    break
                except:
                    pass
            if not found_port:
                raise Exception("Could not find client port.")
        return

    """Send the request to the to_addr location. Pickle the request if it is not pickled."""
    def send(self, request, to_addr, pickled=False):
        if pickled:
            self.sock.sendto(request, to_addr)
        else:
            self.sock.sendto(pickle.dumps(request), to_addr)
        return
    
    """Receive data, fitting it into buffersize."""
    def receive(self, buffersize=None, unpickle=True):
        if not buffersize:
            buffersize = IMG_BUFFER
        data, addr = self.sock.recvfrom(buffersize)
        if unpickle:
            return pickle.loads(data), addr
        else:
            return data, addr