import kivy
from kivy.factory import Factory
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.clock import Clock
from kivymd.uix.toolbar import MDTopAppBar
import cv2
import numpy as np
from kivy.base import EventLoop
from kivy.lang.builder import Builder
import anvil
from anvil.tables import app_tables
from kivy.storage.jsonstore import JsonStore

Builder.load_string('''
<QRCodeScannerScreen>:
    BoxLayout:
        orientation: 'vertical'
        size: root.width, root.height
        MDTopAppBar:
            id: topbar
            elevation: 3
            left_action_items: [['arrow-left', lambda x:root.go_back()]]
            md_bg_color: "#1e75b9"
            specific_text_color: "#ffffff"
            pos_hint: {'top': 1}
        MDLabel:
            id: qr_label
            text: 'Scanned QR code will be displayed here'
            size_hint:(0.8,0.1)
            pos_hint:{'center_x':0.5}
            color: (0, 0, 1, 1)
        # Camera:
        #     id:camera
        #     resolution: (640, 480)
        #     play: True
''')


class QRCodeScannerScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        EventLoop.window.bind(on_back_pressed=self.go_back)
        # self.camera = Camera(resolution=(640, 480))

    def on_enter(self):
        self.start_qr_scan()

    def go_back(self):
        self.manager.current = 'dashboard'
        self.stop_qr_scan()

    def on_key(self, window, key, scancode, codepoint, modifier):
        if key in [27, 9]:
            self.go_back()
            return True
        return False

    def on_leave(self, *args):
        self.stop_qr_scan()

    def start_qr_scan(self):
        self.camera = Camera(resolution=(640, 480), play=True)
        self.add_widget(self.camera)
        Clock.schedule_interval(self.check_for_qr_code, 1.0 / 30.0)

    def stop_qr_scan(self):
        Clock.unschedule(self.check_for_qr_code)
        self.camera.play = False
        self.remove_widget(self.camera)
        self.camera.texture = None

    def check_for_qr_code(self, dt):
        frame = np.frombuffer(self.camera.texture.pixels, dtype=np.uint8)
        frame = frame.reshape((self.camera.texture.height, self.camera.texture.width, 4))

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2GRAY)
        qr_detector = cv2.QRCodeDetector()
        value, pts, qr_code = qr_detector.detectAndDecode(gray_frame)

        if value:
            self.stop_qr_scan()
            logged_user = JsonStore('user_data.json').get('user')['value']['phone']
            if logged_user != int(value):
                try:
                    user = app_tables.wallet_users.get(phone=int(value))
                    self.username = user['username']
                    if user:
                        print(self.username)
                    else:
                        print(f"No user found with phone number: {value}")
                except Exception as e:
                    print(f"Error: {e}")
                self.manager.add_widget(Factory.TransferScreen(name='transfer'))
                self.manager.current = 'transfer'
                details = self.manager.get_screen('transfer')
                details.ids.name.text = self.username
                details.ids.mobile_no_field.text = value
                print('im ended')
            else:
                self.ids.qr_label.text = 'Scanned QR code will be displayed here'
                self.manager.add_widget(Factory.DashBoardScreen(name='dashboard'))
                self.manager.current = 'dashboard'

# class MyScreenManager(ScreenManager):
#     pass
#
#
# class QRCodeScannerApp(MDApp):
#     def build(self):
#         screen_manager = MyScreenManager()
#
#         # Add screens to the screen manager
#         screen_manager.add_widget(QRCodeScannerScreen(name='qr_code_scanner'))
#
#         return screen_manager
#
#
# if __name__ == '__main__':
#     QRCodeScannerApp().run()
