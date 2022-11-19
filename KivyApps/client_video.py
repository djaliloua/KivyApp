import numpy as np
from kivy.app import App
from kivy.core.image import Image
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform
import time

if platform == "android":
    from android.permissions import request_permissions, Permission

    request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE, Permission.CAMERA])

Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (640, 480)
        play: False
    ToggleButton:
        text: 'Play'
        on_press: camera.play = not camera.play
        size_hint_y: None
        height: '48dp'
    Button:
        text: 'Capture'
        size_hint_y: None
        height: '48dp'
        on_press: root.capture()
''')


def get_methods(object, spacing=20):
    methodList = []
    for method_name in dir(object):
        try:
            if callable(getattr(object, method_name)):
                methodList.append(str(method_name))
        except Exception:
            methodList.append(str(method_name))
    processFunc = (lambda s: ' '.join(s.split())) or (lambda s: s)
    for method in methodList:
        try:
            print(str(method.ljust(spacing)) + ' ' +
                  processFunc(str(getattr(object, method).__doc__)[0:90]))
        except Exception:
            print(method.ljust(spacing) + ' ' + ' getattr() failed')


class CameraClick(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def is_android():
        return platform == 'android'

    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        image = camera.export_as_image()
        # print(type(image))
        print(image)
        # print(image.size)
        # print(get_image.read_pixel(0,0))
        # print(get_image(image))
        # get_methods(image)
        timestr = time.strftime("%Y%m%d_%H%M%S")
        # camera.export_to_png("IMG_{}.png".format(timestr))
        print("Captured")


def get_image(image):
    img = np.zeros(image.size)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i, j] = image.read_pixel(i, j)
    return img


class TestCamera(App):

    def build(self):
        return CameraClick()


if __name__ == "__main__":
    TestCamera().run()
