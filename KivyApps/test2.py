from kivy.lang import Builder

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

KV = '''
CustomBox:
    orientation: "vertical"
    Label:
        id: lbl
        text: "0"
        halign: "center"
    Button:
        text: "Click me"
        on_press: root.increment()
'''


class CustomBox(BoxLayout):
    def increment(self):
        x = int(self.ids.lbl.text) + 1
        self.ids.lbl.text = str(x)


class Test(App):
    def build(self):
        return Builder.load_string(KV)


Test().run()
