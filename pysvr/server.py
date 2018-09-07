import cv2
import socket, pickle, time

ip = "127.0.01"

port = 5005

msg = "hello there"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #internet and udp

cap = cv2.VideoCapture(0)

while True:
    #img = cv2.imread('3.jpg',1)
    img = cap.read()[1]
    #print img

    result, encodedImg = cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 70])

    data = pickle.dumps(encodedImg)

    print len(data)


    sock.sendto(data, (ip, port))

cap.release()