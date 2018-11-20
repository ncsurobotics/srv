import srv
import cv2
import connection
from StreamFinishedException import StreamFinishedException
import sys

def getSources():
  c = connection.Connection("get sources")
  sources = c.getSources()
  return sources

def run(sources):
  connections = []
  for sourceName in sources:
    cv2.namedWindow(sourceName, cv2.WINDOW_NORMAL)
    connections.append(connection.Connection(sourceName))
  while True:
    #if len(sources) == 0:
    #  break
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

def help():
  print "To play specific sources:"
  print "\tusage: python watch.py source_1 source_2 ..."
  print "(indefinite amount of listed sources to be played)"
  print "To play all sources:"
  print "\tusage: python watch.py"

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