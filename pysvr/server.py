import socket, pickle, cv2, time

IMG_BUFFER = 60000

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
    if camName == "down" or camName == "front":
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
        raise ValueError("Unknown camera")


BUFFER_SIZE = 60000

COMMAND_BUFFER = 1024

#the request port
port = 5005
#socket commands are issued on
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cap = cv2.VideoCapture(0)



ip = "127.0.0.1"
sock.bind((ip, port))


while True:
    print "reading"
    request, addr = sock.recvfrom(COMMAND_BUFFER)
    print request
    request = request.split(',')
    if len(request) == 3:
        command = request[0].split(' ')
        clientIp = request[1]
        clientPort = int(request[2])
        print command[0]
        if command[0] == "send":
            cam = command[1]
            try:
                data = compressFrame(cam)
                sock.sendto(data, (clientIp, clientPort))
            except ValueError as e:
                print "invalid camera name: ", cam
    elif len(request) == 1:
        if request[0] == "kill":
            break
    
cap.release()
"""
class SRV:
    class __SRV:
        def __init__(self):
            self.clients = []
            self.port = 5005
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #internet udp
            self.ip = socket.gethostbyname(socket.gethostname())
            self.ip = "127.0.0.1"
            self.sock.bind((self.ip, self.port))
    instance = None
    def __init__(self):
        if not SRV.instance:
            SRV.instance = SRV.__SRV()
        
    def addConnection(self, port=None):
        if port:
            self.instance.clients.append(port)
    def serve(self):
        while True:
            request, addr = reqSock.recvfrom(COMMAND_BUFFER)
            port = 5006
            self.instance.sock.sendto("sending down", (ip, port))
    def closeConnection(self, port):
        self.instance.clients.remove(port)

"""