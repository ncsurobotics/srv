import net_commands
from srv_settings import SVR_ADDRESS
from nettools import MailBox
import cv2
"""
Connection stream to SRV server. Can stream from the connection. Basically a client object.
"""

class Connection:
  def __init__(self, name):
    self.mailBox = MailBox()
    if name == "kill":
      self.mailBox.send(net_commands.Kill(), SVR_ADDRESS, pickled=False)
    else:
      self.command = net_commands.Image(name)
      self.frame = None
      self.playingVideo = False
      self.name = name

  def getNextFrame(self):
    self.mailBox.send(self.command, SVR_ADDRESS, pickled=False)
    try:
        msg,_ = self.mailBox.receive()
    except socket.timeout:
        raise Exception("SRV Connection lost")
    if msg.__class__.__name__ is 'StreamEnd':
        raise Exception("Finished playing")
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

  
