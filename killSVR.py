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
#sock.bind((ip, port))

sock.sendto("kill", (SRV_ip, SRV_port))