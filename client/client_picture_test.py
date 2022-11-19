# echo-client.py

import socket
import base64
import cv2
import numpy as np

HOST = "localhost"  # The server's hostname or IP address
PORT = 4445  # The port used by the server


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sockobject = None
        self.vid = cv2.VideoCapture(0)

    def initialize(self):
        self.sockobject = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to(self):
        self.sockobject.connect((self.host, self.port))

    def send_message(self):
        while True:
            try:
                # Capture the video frame
                # by frame
                ret, frame = self.vid.read()
                # convert frame to bytes
                retval, buffer = cv2.imencode('.jpg', frame)
                data = base64.b64encode(buffer)
                self.sockobject.sendall(data)
                # Display the resulting frame
                cv2.imshow('frame', frame)
            except:
                pass
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # the 'q' button is set as the
            # quitting button you may use any
            # desired button of your choice
        self.vid.release()

    def close_socket(self):
        self.sockobject.close()


if __name__ == "__main__":
    client = Client(HOST, PORT)
    client.initialize()
    client.connect_to()
    client.send_message()

    client.close_socket()
