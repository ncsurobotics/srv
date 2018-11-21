import pickle
import cv2
from srv_settings import IMG_BUFFER, SVR_ADDRESS, START_QUALITY, MIN_QUALITY, QUALITY_SHRINK_RATE
from nettools import MailBox
from source import Source, StillSource
import net_commands
from StreamFinishedException import StreamFinishedException
import os
import img_compression

"""
SRV data structures:

-sources
-commands
-clients
"""

"""Video sources on the server. These are either video streams or pictures that connections request."""
sources = {}

"""Commands executed by the server. All commands are in net_commands."""
commands = {}

"""Client connections to the server. Set of ip and port addresses of client connections."""
clients = set()

"""
Adds a source to SRV's sources.
"""
def addSource(source):
    sources[source.name] = source
    print "Added source:", source.name
    print "Sources: ", sources.keys()

"""
Removes a source (given the name) from SRV's sources.
"""
def removeSource(name):
    sources[name].kill()
    del sources[name]
    print "Removed source:", name
    print "Sources: ", sources.keys()

"""
Empties the sources on SRV.
"""
def clearSources():
    source = {}


"""
SRV COMMANDS

These are the commands executed by the server. Clients send the function name
and arguments, the server looks them up in the commands dictionary and executes
them.

When the server executes a command, it may need the request or address information.
For this reason, all commands have a request and address parameter.
"""

"""
Add a client to SRV's client list.
"""
def connect(request, addr):
    clients.add(addr)

"""
Remove a client from SRV's client list.
"""
def disconnect(request, addr):
    clients.remove(addr)

"""
Clean up function called when the server crashes or is killed.
Tells all clients the server died. Frees all sources as well.
Once everything is clean, the program exits.
"""
def cleanUp(request=None, addr=None):
    print '\n', "SRV killed!"
    for clientAddr in clients:
        print "Telling client", clientAddr, "to die"
        mailBox.send(net_commands.ServerKilled(), clientAddr)
    for name in sources:
        sources[name].cap.release()
    exit()

"""
Sends an image from a requested source to the client address.
"""
def sendImage(request, addr):
    outgoing_ip_port = addr
    try:
        if not (request.cam in sources):
            #Tell the client that the source is unknown
            print "server doesn't know source: ", request.cam
            print "Possible sources are: ", sources.keys()
            mailBox.send(net_commands.UnknownSource(), addr)
        try:
            data = img_compression.compress(sources[request.cam].getNextFrame())
            mailBox.send(data, addr)
        except StreamFinishedException:
            #tell the client that the video file has finished
            sources[request.cam].cap.release()
            mailBox.send(net_commands.StreamEnd(), addr)
            #remove the finished source
            removeSource(request.cam)
    except ValueError:
        print('Invalid camera name: {}'.format(request.cam))

"""
Posts an image to an SRV source. Updates the source's current frame.
"""
def postImage(request, addr):
    compressedImg = request.compressedImg
    #decompress image
    img = cv2.imdecode(compressedImg, 1)
    if request.name in sources:
        sources[request.name].updateFrame(img)
    else:
        newSource = StillSource(request.name, img)
        addSource(newSource)

"""
Gets the server's sources and send them out.
"""
def sendSources(request, addr):
    mailBox.send(sources.keys(), addr)

"""
Starts up camera sources.
"""
def startCams(request, addr):
    print "Started cams"
    addSource(Source("down", 0))
    #TODO uncomment this line when using computer with 2 web cams
    
    addSource(Source("front", 1))
    print "Sources: ", sources.keys()

"""
Swaps the front and down cameras.
"""
def swapCams(request, addr):
    oldDown = sources["down"]
    sources["down"] = sources["forward"]
    sources["down"].name = "down"
    sources["forward"] = oldDown
    sources["forward"].name = "forward"
 

"""Dictionary of commands that are executed by client functions."""
commands = {
    'Connect'     : connect,
    'Disconnect'  : disconnect,
    'Kill'        : cleanUp,
    'Image'       : sendImage,
    'Post'        : postImage,
    'GetSources'  : sendSources,
    'StartCams'   : startCams,
    'SwapCams'    : swapCams
}

"""
END OF SRV COMMANDS
"""

"""
Main function of the server. This function infinitely loops listening for client
requests to its mailbox. When it gets one, it executes it.
"""
def run():
    print "SRV has begun, Process Id:", os.getpid()

    clearSources()

    # Set up the socket for receiving requests
    global mailBox
    mailBox = MailBox(ip_and_port=SVR_ADDRESS)

    #loop and listen for client requests. Then grant them
    while True:
        #listen for command
        request, addr = mailBox.receive()
        #execute command
        commands[request.__class__.__name__](request, addr)