# echo-client.py

import socket

HOST = "192.168.1.66"  # The server's hostname or IP address
PORT = 4444  # The port used by the server


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sockobject = None

    def initialize(self):
        self.sockobject = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to(self):
        self.sockobject.connect((self.host, self.port))

    def send_message(self):
        for _ in range(10):
            self.sockobject.sendall(b"Hello, world")
            data = self.sockobject.recv(1024)
            print(f"Received {data!r}")

    def close_socket(self):
        self.sockobject.close()


if __name__ == "__main__":
    client = Client(HOST, PORT)
    client.initialize()
    client.connect_to()
    client.send_message()
    client.close_socket()
