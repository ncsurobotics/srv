import pickle
import cv2
from srv_settings import IMG_BUFFER
from nettools import RequestReceiver
from source import Source
import commands
from StreamFinishedException import StreamFinishedException

#initial quality image compressed to
START_QUALITY = 70
#min jpeg quality is 5
MIN_QUALITY = 5
#rate quality decreases at
QUALITY_SHRINK_RATE = 10

sources = {}

def addSource(source):
    sources[source.name] = source

"""Start video capture of the cam streams."""
def startCams():
    addSource(Source("down", 0))
    #TODO uncomment this line when using computer with 2 web cams
    #addSource(Source("front", 1))

def startFeed():
    #addSource(Source("/home/ben/Videos/fast.mp4"))
    print("SOURCES {}".format(sources))


def swapCams():
    temp = downCam
    downCam = frontCam
    frontCam = temp

def compressFrame(sourceName):
    if sourceName in sources:
        img = sources[sourceName].getNextFrame()
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
        raise ValueError('Unknown source')


# Set up the socket for receiving requests
requestReceiver = RequestReceiver()

#start up the cam sources
startCams()
startFeed()

while True:
    print('reading')
    request, addr = requestReceiver.receive()
    print(request)
    if request.__class__.__name__ is 'Kill':
        for name in sources:
            sources[name].cap.release()
        break
    elif request.__class__.__name__ is 'Image':
        outgoing_ip_port = request.ip_port
        try:
            if not (request.cam in sources):
                #Tell the client that the source is unknown
                requestReceiver.send(commands.UnknownSource(), pickled=False)
            try:
                data = compressFrame(request.cam)
                requestReceiver.send(data)
            except StreamFinishedException:
                #tell the camera that the video file has finished
                sources[request.cam].cap.release()
                requestReceiver.send(commands.StreamEnd(), pickled=False)
        except ValueError:
            print('Invalid camera name: {}'.format(request.cam))


#cap.release()
