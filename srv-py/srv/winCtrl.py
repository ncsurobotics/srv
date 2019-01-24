from subprocess import call
import cv2
#assumes you have installed wmctrl

# this function is probably open to hacking because
# you can add a name like 'name; evil command;'
def destroyWindow(name):
  cv2.destroyWindow(name)
  call(['wmctrl', '-c', name])