"""
Record one of the SRV server's streams to a video file.

python record.py stream_name file_name saves the srv stream to file_name.avi
"""

import sys
import signal
import cv2
from connection import Connection
import socket

def saveAndQuit():
  print "Finishing recording"
  out.release()
  cv2.destroyAllWindows()
  c.close()
  sys.exit(0)

#when hit ctrl-c, save the video and exit
def signal_handler(sig, args):
  saveAndQuit()

out = None

def main(cameraName, outFile, show_feed=False):
  global out, c
  

  #maybe make this not a constant in future version
  #instead take delta between pictures
  frameRate = 24.0

  #connect to the video feed
  c = Connection(cameraName)

  print "Begun recording", cameraName, ". Hit ctrl-c to finish recording."

  signal.signal(signal.SIGINT, signal_handler)

  #get dim of the video being recorded by looking at a frame's size
  height, width, _ = c.getNextFrame().shape

  #used for video file format codec
  fourcc = cv2.cv.CV_FOURCC(*'MJPG')
  out = cv2.VideoWriter(outFile + '.avi', fourcc, frameRate, (width, height))

  while(True):
    try:
      frame = c.getNextFrame()
    except:
      exit(0)
    out.write(frame)
    if show_feed:
      cv2.imshow('frame',frame)
      if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  saveAndQuit()

if __name__ == "__main__":
  if len(sys.argv) != 3:
    print "Usage: python record.py [cameraName] [fileName]"
    exit()

  cameraName = sys.argv[1]
  outFile = sys.argv[2]
  main(cameraName, outFile)