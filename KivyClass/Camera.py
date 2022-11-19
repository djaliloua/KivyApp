__all__ = ('Camera',)

from kivy.lang import builder
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.uix.image import Image
from kivy.core.camera import Camera as CoreCamera
from kivy.properties import NumericProperty, ListProperty, \
    BooleanProperty


class Camera(Image):
    play = BooleanProperty(False)

    index = NumericProperty(-1)

    resolution = ListProperty([-1, -1])

    def __init__(self, **kwargs):
        self._camera = None
        super(Camera, self).__init__(**kwargs)
        if self.index == -1:
            self.index = 0
        on_index = self._on_index
        fbind = self.fbind
        fbind('index', on_index)
        fbind('resolution', on_index)
        on_index()

    def on_tex(self, camera):
        self.texture = texture = camera.texture
        self.texture_size = list(texture.size)
        x = texture.pixels
        self.canvas.ask_update()

    def _on_index(self, *largs):
        self._camera = None
        if self.index < 0:
            return
        if self.resolution[0] < 0 or self.resolution[1] < 0:
            self._camera = CoreCamera(index=self.index, stopped=True)
        else:
            self._camera = CoreCamera(index=self.index,
                                      resolution=self.resolution, stopped=True)
        if self.play:
            self._camera.start()

        self._camera.bind(on_texture=self.on_tex)

    def on_play(self, instance, value):
        if not self._camera:
            return
        if value:
            self._camera.start()
        else:
            self._camera.stop()


class MainApp(App):
    def build(self):
        box = BoxLayout(orientation="vertical")
        cam = Camera()
        box.add_widget(cam)
        cam.index = 0
        cam.resolution = (256, 256)
        cam.play = True
        return box


if __name__ == "__main__":
    MainApp().run()
