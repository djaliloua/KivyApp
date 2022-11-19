import cv2
import socket
import os
import struct

ip, port = 'localhost', 24999
s = socket.socket()
s.connect((ip, port))

# Start video reader
video = cv2.VideoCapture(0)

while True:
    # Wait till data requested, as indicated by receipt of single byte
    s.recv(1)
    print('CLIENT: Image requested')

    # Read a frame of video and reduce size
    _, img = video.read()
    img = cv2.resize(img, (0, 0), fx=0.4, fy=0.4)

    # JPEG-encode into memory buffer and get size
    _, buffer = cv2.imencode('.jpg', img)
    nBytes = buffer.size
    print(f'CLIENT: nBytes={nBytes}')

    # Send 4-byte network order frame size and image
    hdr = struct.pack('!i', nBytes)
    s.sendall(hdr)
    s.sendall(buffer)
