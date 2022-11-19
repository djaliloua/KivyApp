from kivy.lang import Builder
from kivymd.app import MDApp

kv2 = """
MDBoxLayout:
    orientation: "vertical"
    MDLabel:
        text: "Hello second window" 
"""


class SecondApp(MDApp):
    def build(self):
        return Builder.load_string(kv2)


if __name__ == "__main__":
    SecondApp().run()
