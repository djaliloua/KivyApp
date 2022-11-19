import socket
from camera4kivy import Preview
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import builder
from kivy.utils import platform

if platform == "android":
    from android.permissions import request_permissions, Permission

    request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE, Permission.CAMERA])
kv = """
BoxLayout:
    orientation: "vertical"
    CustomAnalyzer:
        id: preview
	    aspect_ratio: '16:9'
	BoxLayout:
	    orientation: "horizontal"
	    Button:
	        text: "Play"
	        on_press: preview.connect_camera(enable_analyze_pixels = True, analyze_pixels_resolution = 720)
	    Button:
	        text: "Stop"
	        on_press: preview.disconnect_camera()
"""
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

    def close_socket(self):
        self.sockobject.close()


class CustomAnalyzer(Preview):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.enable_analyze_frame = True
        self.client = Client(HOST, PORT)
        self.client.initialize()
        try:
            self.client.connect_to()
        except:
            pass
        Clock.schedule_interval(self.analyze_filter, 1 / 33.0)

    def analyze_filter(self, dt):
        self.enable_analyze_frame = True

    def analyze_pixels_callback(self, pixels, size, image_pos,
                                image_scale, mirror):
        try:
            if self.enable_analyze_frame:
                self.enable_analyze_frame = False

                if self.client.sockobject is not None:
                    self.send_bytes(pixels)
                    print(size)
        except:
            print(size)

    def canvas_instructions_callback(self, texture, tex_size, tex_pos):
        pass

    def send_bytes(self, pixels):
        self.client.sockobject.sendall(pixels)


# 1166400
# (1024, 576)
class MainApp(App):
    def build(self):
        return builder.Builder.load_string(kv)


if __name__ == "__main__":
    MainApp().run()
