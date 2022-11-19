import json
import os
import socket
import struct
from kivy import platform
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

if platform == "android":
    from android.permissions import request_permissions, Permission

    request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE, Permission.CAMERA])

KV = """
<CameraClick>:
    BoxLayout:
       
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
        BoxLayout:
            orientation: "horizontal"
            size_hint_y: None
            ToggleButton:
                text: 'Play'
                on_press: camera.play = not camera.play
                size_hint_y: None
                height: '48dp'
            Button:
                text: "Home"
                size_hint_y: None
                height: '48dp'
                on_press: camera.play = not camera.play
                on_release: root.manager.current = 'home' 
            Button:
                text: "Exit"
                size_hint_y: None
                height: '48dp'
                on_press: app.stop() 


<CustomScreen@Screen>:
    canvas:
        Color:
            rgba: 255, 255, 255, 1
        Rectangle:
            pos: self.pos
            size: self.size
            
           

<CustomScreen>:
    GridLayout:
        rows: 4
        cols: 2
        Label: 
            text: "UserName"
            color: "black"
        TextInput:
            id: username
            hint_text: "Your name"
            text: "Ali Abdou Djalilou"
            on_text: root.on_property_changed()
        Label: 
            text: "IP Address"
            color: "black"
        TextInput:
            id: ip
            hint_text: "IP Address"
            text: "192.168.1.66"
            on_text: root.on_property_changed()
        Label:
            text: "PORT"
            color: "black"
        TextInput:
            id: port
            hint_text: "PORT"
            text: "4445"
            on_text: root.on_property_changed()
        Button:
            text: "Save Config"
            on_press: root.save()
        Button: 
            id: btn
            text: "Continue"      
            on_press: root.manager.current = 'camera'
            
"""
HOST = "192.168.1.66"  # The server's hostname or IP address
PORT = 4445  # The port used by the server


class CustomScreen(Screen):
    data = dict()

    def on_property_changed(self):
        if self.ids.username.text == "" or self.ids.ip.text == "" or self.ids.port.text == "":
            self.ids.btn.disabled = True
        else:
            self.ids.btn.disabled = False

    def save(self):
        self.data["Username"] = self.ids.username.text
        self.data["Ip"] = self.ids.ip.text
        self.data["Port"] = self.ids.port.text
        # Serializing json
        json_object = json.dumps(self.data)
        with open("sample.json", "w") as outfile:
            outfile.write(json_object)
            print("Saved...")


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


class CameraClick(Screen):
    def __init__(self, host, port, **kwargs):
        super().__init__(**kwargs)
        self.host = host
        self.port = port
        self.enable_analyze_frame = True
        self.client = Client(self.host, self.port)
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


class VideoStreamingApp(App):
    data = {'Username': '', 'Ip': '', 'Port': '4445'}

    def build(self):
        if os.path.exists("sample.json"):
            with open('sample.json') as f:
                self.data = json.load(f)
        Builder.load_string(KV)
        sm = ScreenManager()
        config = CustomScreen(name="home")
        config.ids.username.text = self.data["Username"]
        config.ids.ip.text = self.data["Ip"]
        config.ids.port.text = self.data["Port"]

        sm.add_widget(config)
        camera = CameraClick(host=self.data["Ip"], port=4445, name="camera")
        sm.add_widget(camera)
        return sm

    def on_start(self):
        pass


if __name__ == "__main__":
    VideoStreamingApp().run()
