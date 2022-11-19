import asyncio
import socket
import struct
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
        self.platform = ""

    def initialize(self):
        self.sockobject = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockobject.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def binding(self):
        self.sockobject.bind((self.host, self.port))
        self.sockobject.listen()

    def accept(self):
        self.conn, self.addr = self.sockobject.accept()
        print(f"{self.addr}")
        self.get_platform()

    def recvall(self, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = bytearray()
        while len(data) < n:
            packet = self.conn.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data

    def get_platform(self):
        try:
            header = self.conn.recv(4)
            nbytes = struct.unpack("!i", header)[0]
            self.platform = self.recvall(nbytes)
            self.platform = bytes(self.platform)
            self.platform = self.platform.decode('utf-8')
        except:
            pass

    def take_photo(self):
        try:
            # Get header with number of bytes
            header = self.conn.recv(4)
            nBytes = struct.unpack('!i', header)[0]
            # Receive actual image
            img = self.recvall(nBytes)
            return img
        except:
            pass

    def close_connection(self):
        self.conn.close()

    def close_socket(self):
        self.sockobject.close()


if __name__ == "__main__":

    server = Server(hostname, port)
    server.initialize()
    server.binding()
    server.accept()
    platform = server.platform
    print(platform)
    while True:
        data = server.take_photo()
        pil_image = Image.frombuffer("RGBA", (640, 480), data)
        # pil_image = pil_image.convert('RGB')
        image = np.array(pil_image, dtype=np.uint8)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        if platform == "android":
            image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        cv2.imshow("Video", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    server.close_connection()
    server.close_socket()
    cv2.destroyAllWindows()
