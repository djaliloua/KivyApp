from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import socket

KV = """
CustomBox:
    orientation: "vertical"
    BoxLayout:
        orientation: "horizontal"
        Button:
            id: conn
            text: "Connect"
            on_press: root.connect()
        Button:
            id: close
            text: "close Connect"
            on_press: root.close_connection()
    BoxLayout:
        orientation: "horizontal"
        BoxLayout:
            orientation: "vertical"
            TextInput:
                id: txt
                text: ""
            Label:
                id: resp
                text: "response"
        Button:
            id: send
            text: "Send"
            on_press: root.send_message()
"""
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

    def send_message(self, msg):
        self.sockobject.sendall(msg.encode())
        data = self.sockobject.recv(1024)

    def close_socket(self):
        self.sockobject.close()


class CustomBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = Client(HOST, PORT)
        self.client.initialize()

    def connect(self):
        try:
            self.client.connect_to()
            self.ids.resp.text = "Connected!!!!"
        except:
            self.ids.resp.text = "Server is OFF"

    def close_connection(self):
        try:
            self.client.close_socket()
            self.ids.resp.text = "Close socket"
        except:
            pass

    def send_message(self):
        try:
            self.client.send_message(self.ids.txt.text)
            self.ids.resp.text = "Message sent"
        except:
            pass


class SocketApp(App):
    def build(self):
        return Builder.load_string(KV)


if __name__ == "__main__":
    SocketApp().run()
