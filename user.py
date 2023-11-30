from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivy.core.window import Window
from kivymd.uix.screen import Screen

Window.size = (400, 500)
KV = """
<Profile>
    name: 'view'
    BoxLayout:
        orientation: 'vertical'
        spacing: dp(10)
        # padding: dp(10)
        pos_hint: {'top': 1}
        
        MDTopAppBar:
            title: 'Profile'
            elevation: 3
            left_action_items: [['arrow-left', lambda x: root.go_back()]]
            md_bg_color: app.theme_cls.primary_color
            size_hint_y: None  # Disable automatic height adjustment
            height: dp(56)  # Set the desired height of the MDTopAppBar

        BoxLayout:
            orientation: 'vertical'
            spacing: dp(5)

            MDLabel:
                id: username_label
                text: "Username: "
                theme_text_color: "Secondary"

            MDLabel:
                id: email_label
                text: "Gmail: "
                theme_text_color: "Secondary"    

            MDLabel:
                id: contact_label
                text: "Contact Number: "
                theme_text_color: "Secondary"

            MDLabel:
                id: aadhaar_label
                text: "Aadhaar: "
                theme_text_color: "Secondary"

            MDLabel:
                id: pan_label
                text: "PAN: "
                theme_text_color: "Secondary"

            MDLabel:
                id: address_label
                text: "Address: "
                theme_text_color: "Secondary"

            MDRaisedButton:
                text: "Edit Profile"
                size_hint: None, None
                size: dp(150), dp(50)
                pos_hint: {'center_x':0.5 ,'bottom':0.9}
                on_release: root.edit_profile()

"""
Builder.load_string(KV)


class Profile(Screen):
    def edit_profile(self):
        app = MDApp.get_running_app()
        app.edit_profile()

    def go_back(self):
        self.manager.current = 'dashboard'


class WalletApp(MDApp):
    def build(self):
        return Builder.load_string(KV)


if __name__ == '__main__':
    WalletApp().run()

