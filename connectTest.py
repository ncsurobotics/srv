import srv
import time


c = srv.stream("the_post")
c.openWindow()
while True:
  #time.sleep(.1)
  c.playWindow()
