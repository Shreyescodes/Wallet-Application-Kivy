from anvil.tables import app_tables
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.lang import Builder
import random
import string
import pyperclip
from kivy.storage.jsonstore import JsonStore

Builder.load_string('''
<ReferFriendScreen>:
    MDBoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "Referral"
            left_action_items: [["arrow-left", lambda x: root.go_back()]]  # Back button
            background_color: (173, 216, 230)  # Light blue color

        BoxLayout:
            orientation: 'vertical'
            padding: [20, 0, 20, 0]  # Adjust outer padding
            spacing: 0  # Adjust spacing between label1 and label2

            CustomLabel:
                id: label1
                text: 'Invite friends to GWallet'
                font_size: 23
                color: 0, 0, 0, 1
                height: dp(100)
                size_hint_x: None  
                width: self.texture_size[0]  
                pos_hint: {'x': 0}  

            CustomLabel:
                id: label2
                text: 'Invite friends to GWallet and get ₹100 and when your friends make their first payment they get ₹50!'
                font_size: 18
                color: 67 / 255, 67 / 255, 67 / 255, 1
                size_hint_y: None  # Allow fixed height
                height: self.texture_size[1]  # Set height to fit text
                size_hint_x: 1  # Relative width
                text_size: self.width, None  # Allow dynamic text wrapping  

                canvas:
                    Color:
                        rgba: 190 / 255, 190 / 255, 190 / 255, 1  # Set color to rgba(190, 190, 190, 1)
                    Line:
                        points: self.x, self.y - dp(20), self.x + self.width, self.y - dp(20) # Draw line separator   
                    Line:
                        points: self.x, self.y - dp(137), self.x + self.width, self.y - dp(137)     

            BoxLayout:
                orientation: 'horizontal'
                size_hint_y: None
                height: dp(100)
                padding:[0,dp(10)]
                spacing: dp(20)

                MDTextField:
                    id: textinput1
                    hint_text: "userfullname"
                    font_size: 24
                    color: 0, 0, 0, 1
                    size_hint_x: 0.5

                MDTextField:
                    id: textinput2
                    hint_text: "usercode"
                    font_size: 24
                    color: 0, 0, 0, 1
                    size_hint_x: 0.5

            MDRectangleFlatButton:
                text: 'Copy Code'
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                size_hint: (0.4, None)  # Increase button size
                on_release: app.copy_code()
                text_color: (67 / 255, 67 / 255, 67 / 255, 1)  # Set text color to rgba(67, 67, 67, 1)
                line_color: [0, 0, 0, 0]  # Set line color to transparent

            MDRoundFlatButton: 
                id: button2
                text: 'Search Contacts'
                pos_hint: {'center_x': 0.5, 'center_y': 0.7}
                size_hint: (0.8, None)  # Increase button size
                theme_text_color: "Custom"  # Use custom text color
                text_color: (67 / 255, 67 / 255, 67 / 255, 1)  # Set text color to rgba(67, 67, 67, 1)
                md_bg_color: (217 / 255, 217 / 255, 217 / 255, 1)  # Set background color to rgba(217, 217, 217, 1)
                line_color: [0, 0, 0, 0]  # Set line color to transparent

        CustomLabel:
            id: label3
            text: '  Your contacts who are not using Gwallet'
            font_size: 20
            color: 0, 0, 0, 1
            width: self.texture_size[0]  
            pos_hint: {'x': 0, 'y': 0.2}  # Adjust the position along the y-direction

''')

class CustomLabel(Label):
    pass

class ReferFriendScreen(Screen):

    def __init__(self, **kwargs):
        super(ReferFriendScreen, self).__init__(**kwargs)
        phone = JsonStore('user_data.json').get('user')['value']['phone']
        username = JsonStore('user_data.json').get('user')['value']['username']
        self.ids.textinput1.text = username
        user = app_tables.wallet_users.get(phone=phone)
        if not user['userreferral']:
            random_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            self.ids.textinput2.text = random_code
            user.update(userreferral=random_code)
        else:
            self.ids.textinput2.text = user['userreferral']

    def copy_code(self):
        code_to_copy = self.root.ids.textinput2.text
        pyperclip.copy(code_to_copy)

    def go_back(self):
        existing_screen = self.manager.get_screen('refer')
        self.manager.current = 'dashboard'
        self.manager.remove_widget(existing_screen)
