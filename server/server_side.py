import socket

hostname = "192.168.1.66"
port = 4444


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

    def recvall(self, sock, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = bytearray()
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data

    def send_message(self):
        b = "server"
        i = 0
        while True:
            data = self.conn.recv(1024)
            print(data.decode())
            if not data:
                break
            # msg = input("Send message: ")
            self.conn.sendall(f"{b} {i}".encode())
            i += 1

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
