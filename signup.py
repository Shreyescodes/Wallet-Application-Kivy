from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp

from kivymd.uix.screen import Screen
Window.size = (300, 500)
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
                    on_release: root.manager.signup()
                
                   
                MDRectangleFlatButton:
                    spacing: dp(25)
                    text: "Back"
                    on_release: root.go_back()
                    size_hint_x: None
                    height: "60dp"
                    width: "60dp"
                    pos_hint: {'center_x':0.8,}
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                    md_bg_color: 0, 0, 0, 1            
            

'''
Builder.load_string(KV)
class SignUpScreen(Screen):
    def go_back(self):
        self.manager.current = 'login'
class SignUpApp(MDApp):
    def build(self):
        return Builder.load_string(KV)



if __name__ == '__main__':
    SignUpApp().run()
