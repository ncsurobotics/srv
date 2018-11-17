import cPickle as pickle
import socket
import net_commands
from srv_settings import IMG_BUFFER
import sys

#40000 characeer limit for msg, probably could be up to 60k
PACKET_SIZE = 40000
PACKET_OVERHEAD = 250

#add modules to system so pickle knows of them
sys.modules['net_commands'] = net_commands



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
            self.ip_and_port = ip_and_port
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            ip = socket.gethostbyname(socket.gethostname())
            found_port = False
            for port in range(5006,7006):
                try:
                    self.ip_and_port = (ip,port)
                    self.sock.bind((ip,port))
                    found_port = True
                    break
                except:
                    pass
            if not found_port:
                raise Exception("Could not find client port.")
        """Dictionary of msg_address : partially assembled messages"""
        self.read_packets = dict()
        return

    """Send the msg to the to_addr location. Pickle the request if it is not pickled."""
    def send(self, msg, to_addr):
      str_data = pickle.dumps(msg)
      #print sys.getsizeof(str_data)
      #print '-'*10
      #print str_data
      #print '+'*10
      #print len(str_data)
      #print "*"*80
      s = ''
      i = 0
      end = len(str_data)
      sent_count = 1
      while(i < end):
        packet_end = min(i + PACKET_SIZE, end)
        #print i, packet_end
        msg_snippet = str_data[i:packet_end]
        if packet_end == end:
          sent_count = -sent_count
        #add on order stamp and sender address
        msg_snippet = str(sent_count) + ':' + msg_snippet
        sent_count += 1
        self.sock.sendto(msg_snippet, to_addr)
        #s += msg_snippet
        i += PACKET_SIZE
      #print s
      #print "*"*80
      
      return
    
    """Receive data and reassemble packets."""
    def receive(self):
      #keep reading until a msg has been fully read and assembled
      while True:
        data, addr = self.sock.recvfrom(PACKET_SIZE + PACKET_OVERHEAD)
        #print data
        #print "Data: ", data
        colon_idx = -1
        for i in range(len(data)):
          if data[i] == ':':
            colon_idx = i
            break
        if colon_idx == -1:
          #print "Bad packet"
          #print data
          raise Exception("Bad data packet format.")
        packet_info = data[colon_idx + 1:len(data)]
        if addr in self.read_packets:
          #add packet info to dictionary
          self.read_packets[addr] += packet_info
        else:
          self.read_packets[addr] = packet_info
        if data[0] == '-':
          msg = self.read_packets[addr]
          self.read_packets[addr] = ''
          return pickle.loads(msg), addr
    """Getter for (ip,port)"""
    def getAddress(self):
      return self.ip_and_port