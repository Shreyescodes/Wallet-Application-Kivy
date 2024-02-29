
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
import pyzbar.pyzbar as pyzbar


class QRCodeScanner(BoxLayout):
    def __init__(self):
        super().__init__()

        self.camera = cv2.VideoCapture(0)
        self.camera.set(3, 640)
        self.camera.set(4, 480)

        self.image_texture = Texture.create(size=(640, 480))
        self.image = Image(texture=self.image_texture)

        self.add_widget(self.image)

        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def update(self, dt):
        ret, frame = self.camera.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            decoded_objects = pyzbar.decode(frame)

            for obj in decoded_objects:
                print(obj.data)

            self.image_texture.blit_buffer(frame.tobytes(), colorfmt='rgb', bufferfmt='ubyte')

class QRCodeScannerApp(App):
    def build(self):
        return QRCodeScanner()

if __name__ == '__main__':
    QRCodeScannerApp().run()