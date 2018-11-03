import srv
import time


c = srv.stream("down")
c.openWindow()
while True:
  #time.sleep(.1)
  c.playWindow()
