import base64
import io
import qrcode
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.base import EventLoop
kv_string = '''         
<QRCodeScreen>:
    BoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "Receive Money"
            anchor_title:'left'
            left_action_items: [["arrow-left", lambda x: root.go_back()]]
            md_bg_color: app.theme_cls.primary_color
            specific_text_color: 1, 1, 1, 1
            pos_hint: {"top":1}
        BoxLayout:
            orientation: 'vertical'
    
            Image:
                id: qr_code_image
                source: ''
    
            BoxLayout:
                orientation: 'horizontal'
                size_hint_y: None
                height: dp(48)
                padding:dp(20)
                spacing:dp(10)
                
                MDRoundFlatButton:
                    text: 'Download QR Code'
                    on_release: root.download_qr_code()
                    pos_hint: {'center_y': 0.5}  # Center vertically
                Widget:
                    size_hint_y: None
                    height: '5dp'
                MDRoundFlatButton:
                    text: 'Share QR Code'
                    on_release: root.share_qr_code()
                    pos_hint: {'center_y': 0.5}  # Center vertically

'''

Builder.load_string(kv_string)


class QRCodeScreen(Screen):
    def go_back(self):
        existing_screen = self.manager.get_screen('qrcode')
        self.manager.current = 'dashboard'
        self.manager.remove_widget(existing_screen)
        
    def __init__(self, **kwargs):
        super(QRCodeScreen, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)
        self.generate_qr_code()

    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key in [27, 9]:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False

    def generate_qr_code(self):
        phone = str(JsonStore('user_data.json').get('user')['value']["phone"])
        qr_code = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=20,
            border=4,
        )
        qr_code.add_data(phone)
        qr_code.make(fit=True)

        img = qr_code.make_image(fill_color="#148EFE", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        png_data = buffer.getvalue()

        # Update QR code image source
        self.ids.qr_code_image.source = 'data:image/png;base64,' + base64.b64encode(png_data).decode('utf-8')

    def download_qr_code(self):
        # Download QR code functionality goes here
        pass

    def share_qr_code(self):
        # Share QR code functionality goes here
        pass


class QRCodeApp(MDApp):
    def build(self):
        return QRCodeScreen()


if __name__ == '__main__':
    QRCodeApp().run()
