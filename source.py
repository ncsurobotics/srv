import cv2
from StreamFinishedException import StreamFinishedException

"""
There are two kinds of sources, video file streams and camera streams.
A camera stream has a name and a camera id. A video file stream just
has a name.
"""

class Source(object):
  """Create a source as either a camera stream or as a video file stream"""
  def __init__(self, name, camId=""):
    if camId == "":
      self.camId = None
      self.type = "VidSource"
    else:
      self.camId = camId
      self.type = "CamSource"
    self.name = name
    
    if self.type == "VidSource":
      self.cap = cv2.VideoCapture(name)
    if self.type == "CamSource":
      #may throw exception if source isn't found
      #TODO test if this throws exception
      self.cap = cv2.VideoCapture(self.camId)
  
  #TODO Add in release of video capture with self.cap.release() after it finishes playing

  def getNextFrame(self):
    ret, frame = self.cap.read()
    if not ret:
      raise StreamFinishedException
    return frame

class StillSource(object):
  def __init__(self, name, img):
    self.img = img
    self.name = name
  def updateFrame(self, img):
    self.img = img
  def getNextFrame(self):
    return self.img
    