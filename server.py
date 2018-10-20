import pickle
import cv2
from srv_settings import IMG_BUFFER
from srv_settings import SVR_ADDRESS
from nettools import MailBox
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
mailBox = MailBox(ip_and_port=SVR_ADDRESS)

#start up the cam sources
startCams()
startFeed()

while True:
    print('reading')
    request, addr = mailBox.receive()
    print "Got client stuff"
    #print(request)
    print request.__class__.__name__
    if request.__class__.__name__ is 'Kill':
        for name in sources:
            sources[name].cap.release()
        break
    elif request.__class__.__name__ is 'Image':
        print "IMAGE" * 4
        outgoing_ip_port = addr
        try:
            print "Request cam: " * 14, request.cam
            if not (request.cam in sources):
                #Tell the client that the source is unknown
                mailBox.send(commands.UnknownSource(), addr)
            try:
                data = compressFrame(request.cam)
                #data should already be pickled
                mailBox.send(data, addr, pickled=True)
            except StreamFinishedException:
                #tell the camera that the video file has finished
                sources[request.cam].cap.release()
                mailBox.send(commands.StreamEnd(), addr)
        except ValueError:
            print('Invalid camera name: {}'.format(request.cam))


#cap.release()
