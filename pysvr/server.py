import pickle
import cv2
from srv_settings import IMG_BUFFER
from nettools import RequestReceiver

#initial quality image compressed to
START_QUALITY = 70
#min jpeg quality is 5
MIN_QUALITY = 5
#rate quality decreases at
QUALITY_SHRINK_RATE = 10

downCam = 0
frontCam = 1

def swapCams():
    temp = downCam
    downCam = frontCam
    frontCam = temp

def compressFrame(camName):
    if camName == 'down' or camName == 'front':
        img = cap.read()[1]
        #goal here is to automatically scale down quality until length is small enough to be sent
        quality = START_QUALITY
        mustBeMoreCompressed = True
        while mustBeMoreCompressed and quality > MIN_QUALITY:
            result, encodedImg = cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
            data = pickle.dumps(encodedImg)
            mustBeMoreCompressed = (len(data) > IMG_BUFFER)
            quality -= QUALITY_SHRINK_RATE
        return data
    else:
        raise ValueError('Unknown camera')


# Set up the socket for receiving requests
requestReceiver = RequestReceiver()

# Set up the video capture
cap = cv2.VideoCapture(0)

while True:
    print('reading')
    request, addr = requestReceiver.receive()
    print(request)
    if request.__class__.__name__ is 'Kill':
        break
    elif request.__class__.__name__ is 'Image':
        outgoing_ip_port = request.ip_port
        try:
            data = compressFrame(request.cam)
            requestReceiver.send(data)
        except ValueError:
            print('Invalid camera name: {}'.format(request.cam))


cap.release()
