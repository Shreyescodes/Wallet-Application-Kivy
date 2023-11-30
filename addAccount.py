from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen, Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField

Window.size = (300, 500)

KV_STRING = '''
<AddAccountScreen>
    MDScreen:
        BoxLayout:
            orientation: 'vertical'

            MDTopAppBar:
                title: 'Add Account'
                elevation: 3
                left_action_items: [['arrow-left', lambda x: root.go_back()]]
                md_bg_color: app.theme_cls.primary_color

            ScrollView:
                GridLayout:
                    cols: 1
                    spacing: '10dp'
                    padding: '14dp'
                    size_hint_y: None
                    height: self.minimum_height  # This line ensures that the GridLayout adjusts its height based on its content
    
                    MDTextField:
                        id: account_holder_name
                        hint_text: "Account Holder's Name"
                        mode: "fill"
                        multiline: False
    
                    MDTextField:
                        id: account_number
                        hint_text: "Account Number"
                        mode: "fill"
                        multiline: False
    
                    MDTextField:
                        id: confirm_account_number
                        hint_text: "Confirm Account Number"
                        mode: "fill"
                        multiline: False
    
                    MDTextField:
                        id: bank_name
                        hint_text: "Bank Name"
                        mode: "fill"
                        multiline: False
    
                    MDTextField:
                        id: branch_name
                        hint_text: "Branch Name"
                        mode: "fill"
                        multiline: False
    
                    MDTextField:
                        id: ifsc_code
                        hint_text: "IFSC Code"
                        mode: "fill"
                        multiline: False
    
                    MDTextField:
                        id: account_type
                        hint_text: "Account Type"
                        mode: "fill"
                        multiline: False
    
                    Widget:
                        size_hint_y: None
                        height: '10dp'
    
                    MDRaisedButton:
                        text: "Add Account"
                        on_release: app.add_account()
                        elevation_normal: 0 
'''
Builder.load_string(KV_STRING)


class AddAccountScreen(Screen):
    def go_back(self):
        self.manager.current = 'dashboard'


class WalletApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV_STRING)


if __name__ == '__main__':
    WalletApp().run()
