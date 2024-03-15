from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
import cv2
import numpy as np
from kivy.base import EventLoop
from kivy.lang.builder import Builder

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
            text: 'Scan QR Code'
            size_hint:(0.8,0.1)
            pos_hint:{'center_x':0.5}
            color: (0, 0, 1, 1)
        Camera:
            id:camera
            resolution: (1280, 720)  # Adjust resolution as needed
            play: True
            # Set rotation to 180 for horizontal flip, 270 for vertical flip (adjust accordingly)
            rotation: 270
''')


class QRCodeScannerScreen(Screen):
    def __init__(self, **kwargs):
        super(QRCodeScannerScreen, self).__init__(**kwargs)
        EventLoop.window.bind(on_back_pressed=self.go_back)
        self.last_frame = None  # Store last captured frame for optimization
        Clock.schedule_interval(self.check_for_qr_code, 1.0 / 30.0)  # Schedule QR code detection

    def on_enter(self):
        self.start_qr_scan()

    def go_back(self):
        self.manager.current = 'dashboard'

    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key in [27, 9]:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False

    def on_leave(self, *args):
        Clock.unschedule(self.check_for_qr_code)

    def check_for_qr_code(self, dt):
        # Capture frame from the camera
        frame = np.frombuffer(self.ids.camera.texture.pixels, dtype=np.uint8)
        frame = frame.reshape((self.ids.camera.texture.height, self.ids.camera.texture.width, 4))

        # Check if frame has changed significantly to avoid unnecessary processing
        if self.last_frame is None or not np.array_equal(frame, self.last_frame):
            self.last_frame = frame

            # Convert frame to grayscale for QR code detection
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2GRAY)

            # Decode QR code using pyzbar
            try:
                detector = cv2.QRCodeDetector()
                data, points, _ = detector.detectAndDecode(gray_frame)
                if data:
                    # Handle successful QR code detection
                    self.ids.qr_label.text = f'Scanned QR Code: {data}'
                    # Implement your further actions based on the scanned data (e.g., navigate to a screen, process information)
                    Clock.unschedule(self.check_for_qr_code)  # Stop scheduling after successful detection (optional)
            except Exception as e:
                # Handle potential errors
                print(f"Error decoding QR code: {e}")

    def start_qr_scan(self):
        pass  # No need for continuous scanning, use the button press instead


class QRCodeScannerApp(MDApp):
    def build(self):
        screen_manager = ScreenManager()

        # Add screens to the screen manager
        screen_manager.add_widget(QRCodeScannerScreen(name='qr_code_scanner'))

        return screen_manager


if __name__ == '__main__':
    QRCodeScannerApp().run()