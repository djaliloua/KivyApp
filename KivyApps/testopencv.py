from kivy.app import App
from kivy.core.camera import CameraBase
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture


from kivy import platform


if platform == "android":
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE, Permission.CAMERA])
try:
    # opencv 1 case
    import opencv as cv

    try:
        import opencv.highgui as hg
    except ImportError:
        class Hg(object):
            '''
            On OSX, not only are the import names different,
            but the API also differs.
            There is no module called 'highgui' but the names are
            directly available in the 'cv' module.
            Some of them even have a different names.

            Therefore we use this proxy object.
            '''

            def __getattr__(self, attr):
                if attr.startswith('cv'):
                    attr = attr[2:]
                got = getattr(cv, attr)
                return got

        hg = Hg()

except ImportError:
    # opencv 2 case (and also opencv 3, because it still uses cv2 module name)
    try:
        import cv2
        # here missing this OSX specific highgui thing.
        # I'm not on OSX so don't know if it is still valid in opencv >= 2
    except ImportError:
        raise


class CamApp(App, CameraBase):
    _update_ev = None

    def __init__(self, **kwargs):
        # we will need it, because constants have
        # different access paths between ver. 2 and 3
        try:
            self.opencvMajorVersion = int(cv.__version__[0])
        except NameError:
            self.opencvMajorVersion = int(cv2.__version__[0])

        self._device = None
        super(CamApp, self).__init__(**kwargs)

    def init_camera(self):
        # consts have changed locations between versions 2 and 3
        if self.opencvMajorVersion in (3, 4):
            PROPERTY_WIDTH = cv2.CAP_PROP_FRAME_WIDTH
            PROPERTY_HEIGHT = cv2.CAP_PROP_FRAME_HEIGHT
            PROPERTY_FPS = cv2.CAP_PROP_FPS
        elif self.opencvMajorVersion == 2:
            PROPERTY_WIDTH = cv2.cv.CV_CAP_PROP_FRAME_WIDTH
            PROPERTY_HEIGHT = cv2.cv.CV_CAP_PROP_FRAME_HEIGHT
            PROPERTY_FPS = cv2.cv.CV_CAP_PROP_FPS
        elif self.opencvMajorVersion == 1:
            PROPERTY_WIDTH = cv.CV_CAP_PROP_FRAME_WIDTH
            PROPERTY_HEIGHT = cv.CV_CAP_PROP_FRAME_HEIGHT
            PROPERTY_FPS = cv.CV_CAP_PROP_FPS

        # Logger.debug('Using opencv ver.' + str(self.opencvMajorVersion))

        if self.opencvMajorVersion == 1:
            # create the device
            self._device = hg.cvCreateCameraCapture(self._index)
            # Set preferred resolution
            cv.SetCaptureProperty(self._device, cv.CV_CAP_PROP_FRAME_WIDTH,
                                  self.resolution[0])
            cv.SetCaptureProperty(self._device, cv.CV_CAP_PROP_FRAME_HEIGHT,
                                  self.resolution[1])
            # and get frame to check if it's ok
            frame = hg.cvQueryFrame(self._device)
            # Just set the resolution to the frame we just got, but don't use
            # self.resolution for that as that would cause an infinite
            # recursion with self.init_camera (but slowly as we'd have to
            # always get a frame).
            self._resolution = (int(frame.width), int(frame.height))
            # get fps
            self.fps = cv.GetCaptureProperty(self._device, cv.CV_CAP_PROP_FPS)

        elif self.opencvMajorVersion in (2, 3, 4):
            # create the device
            self._device = cv2.VideoCapture(self._index)
            # Set preferred resolution
            self._device.set(PROPERTY_WIDTH,
                             self.resolution[0])
            self._device.set(PROPERTY_HEIGHT,
                             self.resolution[1])
            # and get frame to check if it's ok
            ret, frame = self._device.read()

            # source:
            # http://stackoverflow.com/questions/32468371/video-capture-propid-parameters-in-opencv # noqa
            self._resolution = (int(frame.shape[1]), int(frame.shape[0]))
            # get fps
            self.fps = self._device.get(PROPERTY_FPS)

        if self.fps == 0 or self.fps == 1:
            self.fps = 1.0 / 30
        elif self.fps > 1:
            self.fps = 1.0 / self.fps

        if not self.stopped:
            self.start()
    def build(self):
        self.img1 = Image()
        layout = BoxLayout()
        layout.add_widget(self.img1)
        # opencv2 stuffs
        # self.capture = cv2.VideoCapture(0)
        # cv2.namedWindow("CV2 Image")
        Clock.schedule_interval(self.update, self.fps)

        return layout

    def update(self, dt):
        # display image from cam in opencv window
        ret, frame = self._device.read()
        # cv2.imshow("CV2 Image", frame)
        # convert it to texture
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tobytes()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        # if working on RASPBERRY PI, use colorfmt='rgba' here instead, but stick with "bgr" in blit_buffer.
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display image from the texture
        self.img1.texture = texture1


if __name__ == '__main__':
    CamApp().run()
    cv2.destroyAllWindows()
