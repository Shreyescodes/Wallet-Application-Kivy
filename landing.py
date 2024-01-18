from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.image import AsyncImage
from kivymd.app import MDApp
Builder.load_string(
    """
<LandingScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(10)

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(50)
            spacing: dp(10)

            AsyncImage:
                source: 'images/2.png'  # Change this to your image path
                size_hint_x: None
                width: dp(30)
                pos_hint: {'top': 1}

            MDLabel:
                text: 'G-Wallet Payment'
                theme_text_color: 'Primary'
                font_size: '20sp'
                bold: True

        MDLabel:
            text: 'Fast, simple and secure way to pay'
            font_size: '26sp'
            bold: True
            theme_text_color: 'Primary'

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(50)
            spacing: dp(10)
            pos_hint: {'center_x': 0.5}

            MDRectangleFlatButton:
                text: 'Login'
                on_release: root.manager.current = 'signin'
                size_hint: (0.5, 1)
                width: dp(50)
                pos_hint: {'center_x': 0.5, 'y': 0.7}  # Adjust the value as needed
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                md_bg_color: 0, 193/255, 245/255, 1

            MDRectangleFlatButton:
                text: 'Signup'
                on_press: root.manager.current = 'signup'
                size_hint: (0.5, 1)
                width: dp(50)
                pos_hint: {'center_x': 0.5, 'y': 0.7}  # Adjust the value as needed
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                md_bg_color: 0, 193/255, 245/255, 1

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(50)
            spacing: dp(10)
            pos_hint: {'center_x': 0.5}

            BoxLayout:
                orientation: 'vertical'
                spacing: dp(5)
                pos_hint: {'center_x': 0.3}

                MDIconButton:
                    icon: 'shield'
                    pos_hint:{'center_x': 0.5}
                    valign:"center"

                MDLabel:
                    text: 'Safe'
                    theme_text_color: 'Primary'
                    font_size: '16sp'
                    bold: True
                    pos_hint:{'center_x': 0.5}
                    halign:"center"

            BoxLayout:
                orientation: 'vertical'
                spacing: dp(5)
                pos_hint: {'center_x': 0.5}

                MDIconButton:
                    icon: 'lock'
                    pos_hint:{'center_x': 0.5}
                    valign:"center"

                MDLabel:
                    text: 'Secure'
                    theme_text_color: 'Primary'
                    font_size: '16sp'
                    bold: True
                    pos_hint:{'center_x': 0.5}
                    halign:"center"

            BoxLayout:
                orientation: 'vertical'
                spacing: dp(5)
                pos_hint: {'center_x': 0.7}

                MDIconButton:
                    icon: 'credit-card'
                    pos_hint:{'center_x': 0.55}
                    valign:"center"

                MDLabel:
                    text: 'Easy'
                    theme_text_color: 'Primary'
                    font_size: '16sp'
                    bold: True
                    pos_hint:{'center_x': 0.55}
                    halign:"center"
"""
)


class LandingScreen(Screen):
    pass


class WalletApp(MDApp):
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(LandingScreen(name='landing'))
        return screen_manager

