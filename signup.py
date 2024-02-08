import anvil
from anvil.tables import app_tables
from kivy.lang import Builder
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import Screen
from kivymd.uix.snackbar import Snackbar
import requests
from kivy.base import EventLoop
from kivy.core.window import Window
KV = '''
<SignUpScreen>:
    BoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            left_action_items: [["arrow-left", lambda x: root.go_back()]]
            title: 'Sign Up'
            elevation: 5

        ScrollView:


            MDGridLayout:
                cols: 1
                adaptive_height: True
                padding: dp(16)
                required: True

                MDTextField:
                    id: gmail
                    hint_text: "Gmail"
                    required: True

                MDTextField:
                    id: username
                    hint_text: "Username"
                    required: True

                MDTextField:
                    id: password
                    hint_text: "Password"
                    password: True
                    required: True

                MDTextField:
                    id: phone_no
                    hint_text: "Phone Number"
                    required: True

                MDTextField:
                    id: aadhar_card
                    hint_text: "Aadhar Card Number"
                    required: True

                MDTextField:
                    id: pan_card
                    hint_text: "PAN Card Number"
                    required: True

                MDTextField:
                    id: address
                    hint_text: "Address"
                    required: True

                MDRectangleFlatButton:
                    text: "Sign Up"
                    pos_hint: {'center_x': 0.5}
                    on_release: root.signup()
          
'''
Builder.load_string(KV)


class SignUpScreen(Screen):
    def go_back(self):
        self.manager.current = 'landing'
    def __init__(self, **kwargs):
        super(SignUpScreen, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)


    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key in [27,9]:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False

    def signup(self):
        current_screen = self.manager.get_screen('signup')
        gmail = current_screen.ids.gmail.text
        username = current_screen.ids.username.text
        password = current_screen.ids.password.text
        phone_no = current_screen.ids.phone_no.text
        aadhar_card = current_screen.ids.aadhar_card.text
        pan_card = current_screen.ids.pan_card.text
        address = current_screen.ids.address.text
        # self.account_details(phone_no)
        # self.add_money(phone_no)
        # self.transactions(phone_no)
        try:
            if self.is_phone_number_registered(phone_no):
                Snackbar(text="Phone number already exists. Choose another.").open()
                return

            else:  # Add user data to the 'login' collection in Anvil
                app_tables.wallet_users.add_row(
                    email=gmail,
                    username=username,
                    password=password,
                    phone=float(phone_no),
                    aadhar=float(aadhar_card),
                    pan=pan_card,
                    address=address,
                    usertype="customer",
                    banned=False,
                )

                # Show a popup with a success message
                dialog = MDDialog(
                    title="Alert",
                    text="Successfully signed up.",
                    buttons=[
                        MDFlatButton(
                            text="OK",
                            on_release=lambda *args: (dialog.dismiss(), self.dismiss_and_navigate())
                        )
                    ]
                )
                dialog.open()
        except Exception as e:
            print(e)

    @anvil.server.callable
    def is_phone_number_registered(self, phone_number):
        user = app_tables.wallet_users.get(phone=float(phone_number))
        return user is not None

    def dismiss_and_navigate(self):
        self.manager.current = 'signin'
