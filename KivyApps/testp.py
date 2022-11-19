from kivy.lang import Builder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform

kv = """
CustomBox:
    orientation: "vertical"
    Label:
        id:lbl
        text: ""
    Button:
        text: "vibrate"
        on_press: root.vibrate()
"""


class CustomBox(BoxLayout):
    def vibrate(self):
        self.ids.lbl.text = platform
        # print(platform.platform())


class ScreenshotApp(App):
    def build(self):
        return Builder.load_string(kv)


ScreenshotApp().run()
