from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDRoundFlatButton, MDIconButton
from kivy.metrics import dp
import random
import string
import pyperclip
import anvil.server

anvil.server.connect("server_7JA6PVL5DBX5GSBY357V7WVW-TLZI2SSXOVZCVYDM")

# Set the background color of the window to white
Window.clearcolor = (1, 1, 1, 1)

Builder.load_string('''
<ReferFriendScreen>
    MDBoxLayout:
        orientation: 'vertical'
        
        MDIconButton:
            icon: "arrow-left"
            pos_hint: {"center_x": 0.05, "center_y": 0.95}
            on_release: root.go_back()
    
        CustomLabel:
            text: 'Referral'
            font_size: 24
            canvas.before:
                Color:
                    rgba: 20 / 255, 142 / 255, 254 / 255, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
    
        CustomLabel:
            id: label1
            text: 'Invite friends to GWallet'
            padding: 20
            font_size: 42
            color: 0, 0, 0, 1
            size_hint_x: None  
            width: self.texture_size[0]  
            pos_hint: {'x': 0}  
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1  
                Rectangle:
                    pos: self.pos
                    size: self.size
    
        CustomLabel:
            id: label2
            text: 'Invite friends to GWallet and get ₹100 and when your friends make their first payment they get ₹50!'
            padding: 20
            font_size: 18
            color: 67 / 255, 67 / 255, 67 / 255, 1
            size_hint_x: None  
            width: self.texture_size[0] 
            pos_hint: {'x': 0}  
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1  
                Rectangle:
                    pos: self.pos
                    size: self.size
    
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(30)
            spacing: dp(120)
    
            MDTextField:
                id: textinput1
                hint_text: "#userfullname"
                font_size: 24
                color: 0, 0, 0, 1
                size_hint_x: 0.5
    
            MDTextField:
                id: textinput2
                hint_text: "#usercode"
                font_size: 24
                color: 0, 0, 0, 1
                size_hint_x: 0.5
    
        MDRaisedButton:
            text: 'Copy Code'
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            size_hint: (0.4, None)  # Increase button size
            on_release: root.copy_code()
    
        MDRoundFlatButton:
            id: button2
            text: 'Search Contacts'
            pos_hint: {'center_x': 0.5, 'center_y': 0.7}
            size_hint: (0.8, None)  # Increase button size
    
        CustomLabel:
            text: 'Your contacts who are not using Gwallet'
            font_size: 36
            color: 0, 0, 0, 1

    
''')


class CustomLabel(Label):
    pass


class ReferFriendScreen(Screen):
    def on_start(self):
        random_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        # Update textinput2 with the generated code
        self.root.ids.textinput2.text = random_code

    def copy_code(self):
        code_to_copy = self.root.ids.textinput2.text
        pyperclip.copy(code_to_copy)

    def go_back(self):
        self.manager.current = 'dashboard'
        self.ids.textinput1.text = ''
        self.ids.textinput2.text = ''
