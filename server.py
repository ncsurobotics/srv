import pickle
import cv2
from srv_settings import IMG_BUFFER, SVR_ADDRESS, START_QUALITY, MIN_QUALITY, QUALITY_SHRINK_RATE
from nettools import MailBox
from source import Source, StillSource
import net_commands
from StreamFinishedException import StreamFinishedException
import os



SERVER_STARTED = False
sources = {}

def addSource(source):
    sources[source.name] = source
    print "Added source:", source.name
    print "Sources: ", sources.keys()
def removeSource(name):
    sources[name].kill()
    del sources[name]
    print "Removed source:", name
    print "Sources: ", sources.keys()

def clearSources():
    source = {}

def startFeed():
    #addSource(Source("/home/ben/Videos/fast.mp4"))
    pass

#fix to eventually just kill old cams, then start cams with inverted 0 and 1
#TODO grand architecture rewrite: instead of command names, send commands as
#funcs and params
def swapCams():
    oldDown = sources["down"]
    sources["down"] = sources["forward"]
    sources["down"].name = "down"
    sources["forward"] = oldDown
    sources["forward"].name = "forward"


def startCams():
    print "Started cams"
    pass
    addSource(Source("down", 0))
    #TODO uncomment this line when using computer with 2 web cams
    
    addSource(Source("front", 1))
    addSource(Source("/home/ben/Videos/buoy1.avi"))
    addSource(Source("/home/ben/Videos/croppedDice"))
    addSource(Source("/home/ben/Videos/croppedDice2"))
    addSource(Source("/home/ben/Videos/diceReal.avi"))
    addSource(Source("/home/ben/Videos/down0.mp4"))
    addSource(Source("/home/ben/Videos/down_crash.avi"))
    addSource(Source("/home/ben/Videos/DownFalse.avi"))
    addSource(Source("/home/ben/Videos/pathC1.mp4"))
    
    
    
    print "Sources: ", sources.keys()


def compressFrame(sourceName):
    if sourceName in sources:
        img = sources[sourceName].getNextFrame()
        #compress at 80% quality
        result, encodedImg = cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
        return encodedImg
    else:
        raise ValueError('Unknown source')

def run():
    print "SRV has begun, Process Id:", os.getpid()
    SERVER_STARTED = True

    clearSources()

    # Set up the socket for receiving requests
    mailBox = MailBox(ip_and_port=SVR_ADDRESS)

    #start up the cam sources
    #startCams()
    #startFeed()

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
                    mailBox.send(data, addr)
                except StreamFinishedException:
                    #tell the client that the video file has finished
                    sources[request.cam].cap.release()
                    mailBox.send(net_commands.StreamEnd(), addr)
                    #remove the finished source
                    removeSource(request.cam)
            except ValueError:
                print('Invalid camera name: {}'.format(request.cam))
        elif request.__class__.__name__ is 'Post':
            #need to unpickle the image
            #print "Got compressed img: ", request.compressedImg
            compressedImg = request.compressedImg
            #print "GOT POST IMG: ", compressedImg, "GOT POST"
            #decompress image
            img = cv2.imdecode(compressedImg, 1)
            if request.name in sources:
                sources[request.name].updateFrame(img)
            else:
                newSource = StillSource(request.name, img)
                addSource(newSource)
        elif request.__class__.__name__ is 'GetSources':
            mailBox.send(sources.keys(), addr)
        elif request.__class__.__name__ is 'StartCams':
            startCams()
        elif request.__class__.__name__ is 'SwapCams':
            swapCams()



def getSource(streamName):
    if not streamName in sources:
        raise ValueError("Invalid Stream Name: " + streamName)
    else:
        return sources[streamName]