import sys
import cv2
import socket, pickle, time
from srv_settings import SVR_ADDRESS
from nettools import MailBox
import commands

if len(sys.argv) != 2:
    print "Usage: python client.py [command / stream name]\n(possible commands = kill, possible streams = down,forward)"
    exit()
streamName = sys.argv[1]

# Request sender
mailBox = MailBox()

# The window in which the images are displayed
cv2.namedWindow('sent img', cv2.WINDOW_NORMAL)

# The request to send to the server
if sys.argv[1] == "kill":
    command = commands.Kill()
else:
    command = commands.Image(sys.argv[1])
connected = True

while connected:
    mailBox.send(command, SVR_ADDRESS, pickled=False)
    if sys.argv[1] == "kill":
        break
    try:
        msg,_ = mailBox.receive()
    except socket.timeout:
        print("SRV Connection lost")
        connected = False
        break
    if msg.__class__.__name__ is 'StreamEnd':
        print "Finished playing"
        break
    if msg.__class__.__name__ is 'UnknownSource':
        print "Error: Unknown source name "
        break
    #otherwise, treat msg as an image's encoded data
    img = cv2.imdecode(msg, 1)

    cv2.imshow('recieved img', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
