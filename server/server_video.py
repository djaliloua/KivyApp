import asyncio
import socket
import cv2
import base64
import numpy as np

hostname = "localhost"
port = 4445


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
        while True:
            try:
                data = self.conn.recv(400 * 901 * 3)
                # print(data)
                if not data:
                    break
                b = base64.b64decode(data)
                nparr = np.frombuffer(b, np.uint8)
                img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # cv2.IMREAD_COLOR in OpenCV 3.1
                image = cv2.flip(img_np, 1)
                # print(image.shape)
                # image = image.reshape(400, 901, 3)
                # image = cv2.resize(image, (400, 901))
                cv2.imshow("Cal", image)
            except:
                pass
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
