import commands
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
      self.mailBox.send(commands.Kill(), SVR_ADDRESS, pickled=False)
    else:
      self.command = commands.Image(name)
      self.frame = None
      self.playingVideo = False

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

  def openWindow(self):
    self.playingVideo = True
    cv2.namedWindow('sent img', cv2.WINDOW_NORMAL)
    while self.playingVideo:
      self.getNextFrame()
      cv2.imshow('recieved img', self.frame)
      if cv2.waitKey(1) & 0xFF == ord('q'):
          break

  def closeWindow(self):
    self.playingVideo = False
    cv2.destroyAllWindows()
