import cv2
import socket, pickle, time
from srv_settings import client_ip_port
from srv_settings import server_ip_port
from nettools import RequestSender
import commands

# Request sender
requestSender = RequestSender()

# The window in which the images are displayed
cv2.namedWindow('sent img', cv2.WINDOW_NORMAL)

# The request to send to the server
command = commands.Image("down")

connected = True

while connected:
    print("requesting")
    requestSender.send(command)
    try:
        data = requestSender.receive()
    except socket.timeout:
        print("SRV Connection lost")
        connected = False
        break

    img = cv2.imdecode(data, 1)

    cv2.imshow('recieved img', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
