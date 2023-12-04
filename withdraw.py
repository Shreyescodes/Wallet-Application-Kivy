from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import Screen
from kivymd.app import MDApp

Window.size = (300, 500)

KV = '''
<WithdrawScreen>:
    orientation: 'vertical'
    padding: dp(10)
    spacing: dp(10)
    size_hint_y: None
    height: self.minimum_height
    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
    size_hint_x: None
    width: 300
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1  # Set the background color to white
        Rectangle:
            pos: self.pos
            size: self.size

    MDLabel:
        id: wallet_label
        text: "Wallet Money:"
        size_hint: 1, None
        font_size: "20sp"
        bold: True
        height: "20dp"
        halign: "center"
        valign: "center"

    BoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(10)
        size_hint_y: None
        height: self.minimum_height
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint_x: None
        width: 300

        Spinner:
            id: currency_spinner
            text: 'Currency'
            values: ['INR', 'USD', 'EUROS', 'POUND']
            size_hint: None, None
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            size: "150dp", "50dp"
            on_text: app.select_currency(self.text)

        MDTextField:
            id: mobile_textfield
            hint_text: "Mobile"
            helper_text: "Enter your mobile number"
            helper_text_mode: "on_focus"
            input_filter: "int"

        MDTextField:
            id: amount_textfield
            hint_text: "Amount"
            helper_text: "Enter withdrawal amount"
            helper_text_mode: "on_focus"
            input_filter: "float"

        MDRaisedButton:
            text: "Withdraw"
            on_release: app.withdraw()
'''


class WithdrawScreen(Screen, MDBoxLayout):
    pass


class WithdrawApp(MDApp):
    def build(self):
        return Builder.load_string(KV)


WithdrawApp().run()
