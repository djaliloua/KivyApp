import socket
import struct
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform


if platform == "android":
    from android.permissions import request_permissions, Permission

    request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE, Permission.CAMERA])

Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (640, 480)
        allow_stretch: True
        keep_ratio: True
        play: False
        canvas.before:
            PushMatrix
            Rotate:
                angle: -90 if root.is_android() else 0
                origin: self.center
        canvas.after:
            PopMatrix
    ToggleButton:
        text: 'Play'
        on_press: camera.play = not camera.play
        size_hint_y: None
        height: '48dp'
''')
HOST = "192.168.1.66"  # The server's hostname or IP address
PORT = 4445  # The port used by the server


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sockobject = None

    def initialize(self):
        self.sockobject = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to(self):
        self.sockobject.connect((self.host, self.port))
        platformbytes = bytes(platform, "utf-8")
        hdr = struct.pack("!i", len(platformbytes))
        self.sockobject.sendall(hdr)
        self.sockobject.sendall(platformbytes)

    def close_socket(self):
        self.sockobject.close()


class CameraClick(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.enable_analyze_frame = True
        self.client = Client(HOST, PORT)
        self.client.initialize()
        try:
            self.client.connect_to()
        except:
            pass
        Clock.schedule_interval(self.update, 1 / 33.0)

    def is_android(self):
        return platform == "android"

    def update(self, dt):
        try:
            camera = self.ids['camera']
            image = camera.texture
            if image is not None:
                self.send_bytes(image.pixels)
        except Exception as ex:
            print(f"Error client: {ex}")

    def send_bytes(self, pixels):
        nbytes = len(pixels)
        print(f'CLIENT: nBytes={nbytes}')
        # Send 4-byte network order frame size and image
        hdr = struct.pack('!i', nbytes)
        self.client.sockobject.sendall(hdr)
        self.client.sockobject.sendall(pixels)


class TestCamera(App):

    def build(self):
        # Window.maximize()
        return CameraClick()


if __name__ == "__main__":
    TestCamera().run()
