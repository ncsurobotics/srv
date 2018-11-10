import srv
import cv2
import connection
from StreamFinishedException import StreamFinishedException

def getSources():
  c = connection.Connection("get sources")
  sources = c.getSources()
  return sources

def run():
  sources = getSources()
  connections = []
  for sourceName in sources:
    cv2.namedWindow(sourceName, cv2.WINDOW_NORMAL)
    connections.append(connection.Connection(sourceName))
  while True:
    if len(sources) == 0:
      break
    for i in range(len(sources)):
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

run()