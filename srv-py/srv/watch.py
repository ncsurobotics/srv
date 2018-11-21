"""
Watch some or all SRV video streams.
"""
import srv
import cv2
import connection
from StreamFinishedException import StreamFinishedException
import sys

"""
Connection and function to get sources from SRV.
"""
sourcesConnection = connection.Connection("get sources")
def getSources():
  sources = sourcesConnection.getSources()
  return sources

"""
Forever loop and play SRV streams.
"""
def run(sources):
  connections = []
  for sourceName in sources:
    cv2.namedWindow(sourceName, cv2.WINDOW_NORMAL)
    connections.append(connection.Connection(sourceName))
  while True:
    #if the system argument just wanted to watch all videos, constantly update sources
    #TODO fix this so that it blocks when there are no sources
    #TODO fix this so that the server notifies it when sources are added and removed
    if len(sys.argv) == 1:
      sources = getSources()
    for i in range(len(sources)):
      if sources[i] not in srvSources:
        connections.pop(i)
        src = sources.pop(i)
        cv2.destroyWindow(src)
        print "Error:", src, "not in SRV Sources"
        print "SRV Sources:", getSources()
        break
      try:
        cv2.imshow(sources[i], connections[i].getNextFrame())
      except StreamFinishedException:
        connections.pop(i)
        src = sources.pop(i)
        cv2.destroyWindow(src)
        print src, "stream finished."
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  for sourceName in sources:
    cv2.destroyWindow(sourceName)

"""
Print out help messages.
"""
def help():
  print "To play specific sources:"
  print "\tusage: python watch.py source_1 source_2 ..."
  print "(indefinite amount of listed sources to be played)"
  print "To play all sources:"
  print "\tusage: python watch.py"

"""
Parse command line arguments and start playing windows.
The main function area.
"""

srvSources = getSources()

if len(sys.argv) == 1:
  sources = getSources()
elif len(sys.argv) == 2:
  if sys.argv[1].lower() == "help":
    help()
  else:
    #just 1 source
    sources = [sys.argv[1]]
else:
  #each command line argument is a source name
  sources = []
  for i in range(1,len(sys.argv)):
    sources.append(sys.argv[i])

run(sources)