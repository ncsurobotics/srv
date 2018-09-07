import socket, pickle, cv2, time

BUFFER_SIZE = 60000

ip = "127.0.0.1"
port = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #internet udp

sock.bind((ip, port))

 #buffer size
cv2.namedWindow('sent img', cv2.WINDOW_NORMAL)
while True:
    data, addr = sock.recvfrom(BUFFER_SIZE)
    print len(data)
    encodedImg = pickle.loads(data)
    
    img = cv2.imdecode(encodedImg, 1)

    
    cv2.imshow('recieved img', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
#cv2.waitKey(0)
cv2.destroyAllWindows()