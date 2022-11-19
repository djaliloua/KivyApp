import asyncio
import socket

import PIL
import cv2
import base64
import numpy as np
from PIL import Image
import io

hostname = "192.168.1.66"
port = 4445

print(PIL.__version__)


class Server:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sockobject = None
        self.conn = None
        self.addr = None

    def initialize(self):
        self.sockobject = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def binding(self):
        self.sockobject.bind((self.host, self.port))
        self.sockobject.listen()

    def accept(self):
        self.conn, self.addr = self.sockobject.accept()
        print(f"{self.addr}")

    def send_message(self):
        image_size = (720, 405)
        while True:
            try:
                data = self.conn.recv(720*405*4)
                # print(data)
                if not data:
                    break
                pil = np.frombuffer(data, dtype=np.uint8).reshape(*image_size)
                # byte_image = io.BytesIO(data)
                # pil = Image.frombuffer("RGB", image_size, data)
                # pil = pil.convert("RGB")
                # cv_img = np.array(pil, dtype=np.uint8)
                # convert
                print(type(pil))
                # cv2.imshow("CCCCC", cv_img)
                # print(type(pil))
            except Exception as ex:
                print(f"ERROR: {ex}")
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # 360400

    def close_connection(self):
        self.conn.close()

    def close_socket(self):
        self.sockobject.close()


if __name__ == "__main__":
    server = Server(hostname, port)
    server.initialize()
    server.binding()
    server.accept()
    server.send_message()
    server.close_connection()
    server.close_socket()
    cv2.destroyAllWindows()
