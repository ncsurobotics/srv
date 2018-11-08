import srv
import cv2
import connection

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
    for i in range(len(sources)):
      cv2.imshow(sources[i], connections[i].getNextFrame())
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  for sourceName in sources:
    cv2.destroyWindow(sourceName)

def run2():
  sources = getSources()
  c = connection.Connection("down")
  cv2.namedWindow('image', cv2.WINDOW_NORMAL)
  
  
  pass
  while True:
    f = c.getNextFrame()
    cv2.imshow('image',f)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  cv2.destroyAllWindows()


run()