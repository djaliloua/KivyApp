import json
import socket
import struct
import time
from kivy.app import App
from kivy.clock import Clock
from kivy.core import window
from kivy.core.image import Texture
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager


window.size = (1200, 900)

kv = """

<CustomBox>:
    #orientation: "vertical"
    GridLayout:
        rows: 5
        cols: 2
        Label:
            text: "Username"
        Label:
            id: username
            text: "Username"
        Label:
            text: "IP address"
        Label:
            id: ip
            text: "ip"
        Label:
            text: "Port"
        TextInput:
            id: port
            hint_text: "Port"
            text: "4445"
            on_text: root.property_changed(self.text)
        Button:
            text: "Save"
            on_press: root.save(port.text)
        Button:
            id: server
            text: "Start Server"
            on_press: root.connect()
            on_release: root.manager.current = 'camera'


<CustomBoxCam>:
    id: box
    #orientation: "vertical"
    Image:
        id: img
        canvas.before:
            PushMatrix
            Rotate:
                angle: -90
                origin: self.center
        canvas.after:
            PopMatrix
    BoxLayout:
        orientation: "horizontal"
        ToggleButton:
            text: 'Play'
            on_press: root.on_play()
            size_hint_y: None
            height: '48dp'
        Button:
            text: 'Capture'
            size_hint_y: None
            height: '48dp'
            on_press: root.capture()
        Button:
            text: "Exit"
            size_hint_y: None
            height: '48dp'
            on_press: app.stop()


"""


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


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
        print("waiting for connection...")
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


class CustomBox(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.server = None
        self.set_names()

    def set_names(self):
        hostname = socket.gethostname()
        self.ids.ip.text = get_ip()
        self.ids.username.text = hostname

    def property_changed(self, value):
        if value == "":
            self.ids.server.disabled = True
        else:
            self.ids.server.disabled = False

    def save(self, value):
        data = dict()
        data["Port"] = value
        # Serializing json
        json_object = json.dumps(data)

        # Writing to sample.json
        with open("sample.json", "w") as outfile:
            outfile.write(json_object)

    def connect(self):
        if self.server is not None:
            self.server.accept()


class CustomBoxCam(Screen):
    def __init__(self, server, **kwargs):
        super().__init__(**kwargs)
        self.img1 = None
        self.server = server
        self.play = True
        # platform = self.server.platform
        if self.server is not None:
            Clock.schedule_interval(self._update, 1.0 / 33.0)

    def _update(self, dt):
        try:
            if self.play:
                data = self.server.take_photo()
                texture1 = Texture.create(size=(640, 480), colorfmt='rgba')
                texture1.blit_buffer(data, colorfmt='rgba', bufferfmt='ubyte')
                self.ids.img.texture = texture1
        except:
            pass

    def on_play(self):
        self.play = not self.play

    def close(self):
        self.server.close_connection()
        self.server.close_socket()

    def capture(self):

        timestr = time.strftime("%Y%m%d_%H%M%S")
        self.ids.img.export_to_png("IMG_{}.png".format(timestr))
        print("Captured")


class TestApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Builder.load_string(kv)
        self.home_screen = CustomBox(name="home")
        self.server = Server(self.home_screen.ids.ip.text, int(self.home_screen.ids.port.text))
        self.server.initialize()
        self.server.binding()

    def build(self):
        sc = ScreenManager()
        # instantiate screens

        self.home_screen.server = self.server
        # home_screen.ids.server.bind(on_release=self.connect())
        cam_screen = CustomBoxCam(name="camera", server=self.server)
        # home_screen.set_names()
        # Add screens to the screen manager
        sc.add_widget(self.home_screen)
        sc.add_widget(cam_screen)
        return sc


if __name__ == "__main__":
    TestApp().run()
