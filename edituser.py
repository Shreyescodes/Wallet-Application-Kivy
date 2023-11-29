from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.screen import Screen

Window.size = (300, 500)
KV = """
<EditUser>
    ScrollView:
        BoxLayout:
            orientation: "vertical"
            spacing: "10dp"
            padding: ["10dp", "1dp", "10dp", "1dp"]
            size_hint_y: None
            height: self.minimum_height
            pos_hint: {'top': 1}
    
            MDLabel:
                text: "Edit Profile"
                theme_text_color: "Secondary"
                size_hint_y: None
                height: self.texture_size[1] 
    
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
                readonly: True
                
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
    
            MDTextField:
                id: pan
                text:""
                hint_text: "PAN Number"
                helper_text: "Enter your PAN number"
                icon_right: "credit-card"
    
            MDTextField:
                id: address
                text:""
                hint_text: "Address"
                helper_text: "Enter your address"
                icon_right: "home"
    
            MDRaisedButton:
                text: "Save Edit"
                on_release: root.save_edit()
"""
Builder.load_string(KV)


class EditUser(Screen):
    def save_edit(self):
        app = MDApp.get_running_app()
        app.save_edit()


class WalletApp(MDApp):
    def build(self):
        return Builder.load_string(KV)


if __name__ == '__main__':
    WalletApp().run()
