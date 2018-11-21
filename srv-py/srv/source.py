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

  """Get the next frame in the video feed."""
  def getNextFrame(self):
    ret, frame = self.cap.read()
    if not ret:
      raise StreamFinishedException
    return frame

  """Free this source's resources."""
  def kill(self):
    self.cap.release()

"""
Source that has images posted to it. Basically just a 'still' image frame that
lives on SRV. Still images can be updated by clients posting images to the server.

Like a sub class of source that must implement getNextFrame and kill.
"""
class StillSource(object):
  def __init__(self, name, img):
    self.img = img
    self.name = name

  """
  A frame is updated by setting it to a new one.
  """
  def updateFrame(self, img):
    self.img = img
  
  """
  Since the source is a still image, the next frame is the current one.
  """
  def getNextFrame(self):
    return self.img
  
  """Dummy function. No resources freed."""
  def kill(self):
    pass