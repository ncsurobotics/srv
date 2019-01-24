import net_commands
from srv_settings import SVR_ADDRESS
from nettools import MailBox
import cv2
import img_compression as ic
import pickle
from StreamFinishedException import StreamFinishedException
import socket
"""
Connection stream to SRV server. Can stream from the connection. Basically a client object.

TODO add in closing source
"""

"""
Object that has a connection to the server. It has its own mailbox.
Some connections are temporary and only send one message, such as kill, StartCams, and
SwapCams.
"""
class Connection:
  """
  Closes a connection with SRV.
  """
  def close(self):
    self.mailBox.send(net_commands.Disconnect(), SVR_ADDRESS)
    self.mailBox = None
  
  """
  Creates a connection with the given name. If the name is a command, it executes the
  command and closes itself. Otherwise, the connection remains open as a connection
  to request images from SRV. Also, connections can be used to post to a source that
  shares a name with the connection.
  """
  def __init__(self, name):
    self.mailBox = MailBox()
    #connect to SRV
    self.mailBox.send(net_commands.Connect(), SVR_ADDRESS)
    #one time execution commands
    if name == "kill":
      self.mailBox.send(net_commands.Kill(), SVR_ADDRESS)
      self.close()
    elif name == "StartCams":
      self.mailBox.send(net_commands.StartCams(), SVR_ADDRESS)
      self.close()
    elif name == "SwapCams":
      self.mailBox.send(net_commands.SwapCams(), SVR_ADDRESS)
      self.close()
    else:
      #connect to a specific source
      self.command = net_commands.Image(name)
      self.frame = None
      self.playingVideo = False
      self.name = name
  
  """Get server's sources"""
  def getSources(self):
    self.mailBox.send(net_commands.GetSources(), SVR_ADDRESS)
    try:
        sources,_ = self.mailBox.receive()
    except socket.timeout:
        raise Exception("SRV Connection lost")
    return sources
  
  """Get the next frame from the source that shares this connection's name."""
  def getNextFrame(self):
    self.mailBox.send(self.command, SVR_ADDRESS)
    try:
      msg,_ = self.mailBox.receive()
    except socket.timeout:
      raise Exception("SRV Connection lost")
    if msg.__class__.__name__ is 'StreamEnd':
      raise StreamFinishedException("Finished playing")
    if msg.__class__.__name__ is 'UnknownSource':
      raise Exception("Error: Unknown source name ")
    if msg.__class__.__name__ is 'ServerKilled':
      self.close()
      print("SRV server killed!")
      exit()

    self.frame = cv2.imdecode(msg, 1)
    return self.frame
  
  """Replacement for svr debug, client posts an image to the server. Then other clients can read it."""
  #TODO add handshake so that it waits for server to reply that it has read it
  def post(self, img, name=None):
    #compress image
    compressedImg = ic.compress(img)
    #name should default to this connection's name
    if name==None:
      name = self.name
    #tell server to post img
    self.mailBox.send(net_commands.Post(name, compressedImg), SVR_ADDRESS)