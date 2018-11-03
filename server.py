import pickle
import cv2
from srv_settings import IMG_BUFFER
from srv_settings import SVR_ADDRESS
from nettools import MailBox
from source import Source
import net_commands
from StreamFinishedException import StreamFinishedException
import os

#initial quality image compressed to
START_QUALITY = 70
#min jpeg quality is 5
MIN_QUALITY = 5
#rate quality decreases at
QUALITY_SHRINK_RATE = 10

SERVER_STARTED = False
sources = {}

def addSource(source):
    sources[source.name] = source

"""Start video capture of the cam streams."""
def startCams():
    print "Started cams"
    addSource(Source("down", 0))
    #TODO uncomment this line when using computer with 2 web cams
    addSource(Source("front", 1))
    print "Sources: ", sources.keys()
def clearSources():
    source = {}

def startFeed():
    #addSource(Source("/home/ben/Videos/fast.mp4"))
    pass

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

def run():
    print "SRV has begun, Process Id:", os.getpid()
    SERVER_STARTED = True

    clearSources()

    # Set up the socket for receiving requests
    mailBox = MailBox(ip_and_port=SVR_ADDRESS)

    #start up the cam sources
    startCams()
    startFeed()

    while True:
        request, addr = mailBox.receive()
        if request.__class__.__name__ is 'Kill':
            for name in sources:
                sources[name].cap.release()
            break
        elif request.__class__.__name__ is 'Image':
            outgoing_ip_port = addr
            try:
                if not (request.cam in sources):
                    #Tell the client that the source is unknown
                    print "server doesn't know source: ", request.cam
                    print "Possible sources are: ", sources.keys()
                    mailBox.send(net_commands.UnknownSource(), addr)
                try:
                    data = compressFrame(request.cam)
                    #data should already be pickled
                    mailBox.send(data, addr, pickled=True)
                except StreamFinishedException:
                    #tell the camera that the video file has finished
                    sources[request.cam].cap.release()
                    mailBox.send(net_commands.StreamEnd(), addr)
            except ValueError:
                print('Invalid camera name: {}'.format(request.cam))


def getSource(streamName):
    if not streamName in sources:
        raise ValueError("Invalid Stream Name: " + streamName)
    else:
        return sources[streamName]