import requests
from kivy.lang import Builder
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import Screen
from kivy.base import EventLoop
from kivy.core.window import Window
from anvil.tables import app_tables
from kivymd.uix.snackbar import Snackbar

KV = """
<EditUser>
    BoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: 'Edit Profile'
            elevation: 3
            left_action_items: [['arrow-left', lambda x: root.go_back()]]
            md_bg_color: "#1e75b9"
            specific_text_color: "#ffffff"
        ScrollView:
            BoxLayout:
                orientation: "vertical"
                spacing: "10dp"
                padding: ["10dp", "1dp", "10dp", "1dp"]
                size_hint_y: None
                height: self.minimum_height
                pos_hint: {'top': 1}

                MDTextField:
                    id: username
                    text:""
                    hint_text: "Username"
                    helper_text: "Enter your username"
                    icon_right: "account"

                MDTextField:
                    id: email
                    text:""
                    hint_text: "Email"
                    helper_text: "Enter your email"
                    icon_right: "email"

                MDTextField:
                    id: phone
                    text:""
                    hint_text: "Phone Number"
                    helper_text: "Enter your phone number"
                    icon_right: "phone"
                    readonly: False  # Allow editing

                MDTextField:
                    id: password
                    text:""
                    hint_text: "Password"
                    helper_text: "Enter your password"
                    icon_right: "lock"

                MDTextField:
                    id: aadhaar
                    text:""
                    hint_text: "Aadhaar Number"
                    helper_text: "Enter your Aadhaar number"
                    icon_right: "fingerprint"
                    readonly: False  # Allow editing

                MDTextField:
                    id: pan
                    text:""
                    hint_text: "PAN Number"
                    helper_text: "Enter your PAN number"
                    icon_right: "credit-card"
                    readonly: False  # Allow editing

                MDTextField:
                    id: address
                    text:""
                    hint_text: "Address"
                    helper_text: "Enter your address"
                    icon_right: "home"
                    readonly: False  # Allow editing

                MDRaisedButton:
                    text: "Save Edit"
                    on_release: root.save_edit()
                    pos_hint: {'center_x': 0.5}

"""
Builder.load_string(KV)


class EditUser(Screen):
    def go_back(self):
        self.manager.current = 'settings'

    def __init__(self, **kwargs):
        super(EditUser, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)

    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key == 27:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False

    def save_edit(self):
        edit_scr = self.manager.get_screen('edituser')
        phone = edit_scr.ids.phone.text
        username = edit_scr.ids.username.text
        email = edit_scr.ids.email.text
        password = edit_scr.ids.password.text
        aadhar = edit_scr.ids.aadhaar.text
        pan = edit_scr.ids.pan.text
        address = edit_scr.ids.address.text

        try:
            # Reference to the 'login' table in Anvil
            login_table = app_tables.wallet_users

            # Check if the user exists
            user = login_table.get(phone=float(phone))

            if user is not None:
                # Update the user details
                user.update(
                    username=username,
                    email=email,
                    password=password,
                    aadhar=float(aadhar),
                    pan=pan,
                    address=address,
                )

                print("User details updated successfully.")
                self.show_update_success_popup()
            else:
                print(f"User with phone number {phone} does not exist.")
                self.manager.show_error_popup(f"User with phone number {phone} does not exist.")

        except Exception as e:
            print(f"Error updating user details: {e}")

    def show_update_success_popup(self):
        dialog = MDDialog(
            title="Update Success",
            text="Your profile has been updated successfully. Please log in again.",
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda *args: (dialog.dismiss(), self.manager.logout()),
                )
            ]
        )
        dialog.open()



