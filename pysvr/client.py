import cv2
import socket, pickle, time

COMMAND_BUFFER = 1024

IMG_BUFFER = 60000

#the client's ip + port for recieving images
ip = "127.0.01"
port = 5006

#SRV's ip + port that client mails
SRV_ip = "127.0.01"
SRV_port = 5005


#img socket recv img
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, port))
sock.settimeout(1.0)

cv2.namedWindow('sent img', cv2.WINDOW_NORMAL)

command = "send down," + ip + "," + str(port)

connected = True

while connected:
    print "requesting"
    sock.sendto(command, (SRV_ip, SRV_port))
    try:
        data, addr = sock.recvfrom(IMG_BUFFER)
    except socket.timeout:
        print "SRV Connection lost"
        connected = False
        break

    encodedImg = pickle.loads(data)
    
    img = cv2.imdecode(encodedImg, 1)

    cv2.imshow('recieved img', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()