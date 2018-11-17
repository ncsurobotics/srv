import net_commands
from srv_settings import SVR_ADDRESS
from nettools import MailBox
import cv2
from server import compressFrame
import img_compression as ic
import pickle
from StreamFinishedException import StreamFinishedException
"""
Connection stream to SRV server. Can stream from the connection. Basically a client object.

TODO add in closing connection or source
"""

class Connection:
  def __init__(self, name):
    self.mailBox = MailBox()
    if name == "kill":
      self.mailBox.send(net_commands.Kill(), SVR_ADDRESS)
    elif name == "StartCams":
      self.mailBox.send(net_commands.StartCams(), SVR_ADDRESS)
    elif name == "SwapCams":
      self.mailBox.send(net_commands.SwapCams(), SVR_ADDRESS)
    else:
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
    self.frame = cv2.imdecode(msg, 1)
    return self.frame
  def closeWindow(self):
    self.playingVideo = False
    cv2.destroyWindow(self.name)

  def openWindow(self):
    self.playingVideo = True
    cv2.namedWindow(self.name, cv2.WINDOW_NORMAL)
      
  def playWindow(self):
    if self.playingVideo:
      self.getNextFrame()
      cv2.imshow(self.name, self.frame)
      if cv2.waitKey(1) & 0xFF == ord('q'):
          #self.closeWindow()
          self.playingVideo = False
          cv2.destroyWindow(self.name)

  #replacement for svr debug, client posts an image to the server. Then other clients can read it.
  #TODO add handshake so that it waits for server to reply that it has read it
  def post(self, img, name=None):
    #compress image
    compressedImg = ic.compress(img)
    #print "COMPRESSING"
    #print compressedImg
    #print "COMPRESSED"
    #name should default to self.name
    if name==None:
      name = self.name
    #tell server to post img
    self.mailBox.send(net_commands.Post(name, compressedImg), SVR_ADDRESS)