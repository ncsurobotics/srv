
from multiprocessing import Process, Queue, Value
import cv2
import time

"""
File containing helper methods for managing opencv windows.
There is a global dictionary of {name : window} pairs
accessed via windows() function. Each window is its own
process.

Window functions for:
-creating
-updating
-destroying

To exit window, hit q. To exit all windows, hit k.
"""

"""
Record for each window
(process, queue, alive, lastTimeKilled)
"""
class WindowRecord(object):
  commonQueue = Queue()
  def __init__(self, name, images, alive, lastTimeKilled, responseQueue):
    self.name = name
    self.images = images
    self.alive = alive
    self.lastTimeKilled = lastTimeKilled
    self.responseQueue = responseQueue

"""
Function that returns the same instance of a dictionary,
used as a global variable of the dictionary of windows
name : windowRecord
"""
def windows(windows={}):
  return windows

"""
Function run by process.

Displays the images from the image queue in order. Will close window after
images stop coming for 2 seconds.
"""
def winProc(name, images, alive, lastTimeKilled, responseQueue):
  try:
    #cv2.namedWindow(name)
    # first frame
    frame = images.get()
    #print "I am the frame", len(frame)
    while True:
      try:
        #print "I am getting the frame"
        frame = images.get(timeout=2)
        #print "I got the frame"
      except Exception as e:
        #print "FINISHED"
        break
      if frame.__class__.__name__ == 'NoneType':
        #print "THe frame was none"
        break
      #print "About to show the frame"
      cv2.imshow(name, frame)
      #print "Showing the frame"
      key = cv2.waitKey(1) & 0xFF
      if key == ord('q'):
        responseQueue.put('kill')
        responseQueue.put('kill')
        responseQueue.put('kill')
        
        break
      if key == ord('k'):
        responseQueue.put('kill all')
        break
  except:
    pass
  finally:
    # the process is no longer alive, set its alive value to 0
    alive.value = 0
    lastTimeKilled.value = time.clock()
    cv2.destroyWindow(name)

"""
Create a window with the given name and response queue.
"""
def window(name, responseQueue=None):
  # if the name is in the dictionary and it is alive, do nothing
  if name in windows() and windows()[name].alive.value == 1:
    return
  
  queue = Queue()

  alive = Value('d', 1)

  lastTimeKilled = Value('f', -1)

  if responseQueue == 'common':
    responseQueue = WindowRecord.commonQueue

  proc = Process(target=winProc, args=(name, queue, alive, lastTimeKilled, responseQueue))

  windows()[name] =  WindowRecord(proc, queue, alive, lastTimeKilled, responseQueue)
  proc.start()

"""
Make a group of windows with the given names and response queue.
"""
def windowPool(names, responseQueue=None):
  if responseQueue == 'common':
    responseQueue = WindowRecord.commonQueue
  for name in names:
    window(name, responseQueue)

"""
Makes the window with the name play the image by putting
the image into the window's image queue.

Updates the window
"""
def imshow(name, img):
  # if the window is alive
  if name in windows() and windows()[name].alive.value == 1:
    windows()[name].images.put(img)
  else:
    window(name)
    imshow(name, img)
  
  if allKilled():
    destroyAllWindows()

def allKilled():
  try:
    return WindowRecord.commonQueue.get_nowait() == 'kill all'
  except Exception:
    return False

"""
Destroys the window with the given name.
"""
def destroyWindow(name):
  windows()[name].images.put(None)

"""
Destroy all windows in the windows() dictionary.
"""
def destroyAllWindows():
  for name in windows():
    destroyWindow(name)

"""
Return number of open windows.
"""
def openWindows():
  count = 0
  for name in windows():
    if windows()[name].alive.value == 1:
      count += 1
  return count

"""
Print windows() dictionary.
"""
def printWindows():
  w = windows()
  for name in w:
    # print name of window and if alive
    print name, w[name].alive.value



"""
Determines if the window with the name was killed within the given time.
If ago is none, return if it was ever killed.
"""
def wasKilled(name, ago=None):
  w = windows()
  if ago == None:
    return name in w and w[name].lastTimeKilled.value != -1
  if name in w and w[name].lastTimeKilled.value != -1:
    return time.clock() - w[name] <= ago
  return False