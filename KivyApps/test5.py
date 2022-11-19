from kivy.app import App
from kivy.lang import Builder
from kivy import platform

if platform == "android":
    from android.permissions import request_permissions, Permission

    request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE, Permission.CAMERA])

kv = """
BoxLayout:
    orientation: "vertical"
    Button:
        text: "Click me"
"""


class MainApp(App):
    def build(self):
        return Builder.load_string(kv)


if __name__ == "__main__":
    MainApp().run()
