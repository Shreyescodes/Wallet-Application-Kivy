from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import Screen

KV = '''
<ContactUsScreen>:
    Screen:
        MDTopAppBar:
            left_action_items: [["arrow-left", lambda x: root.go_back()]]
            title: 'Contact Us'
            md_bg_color: "#1e75b9"
            specific_text_color: "#ffffff"
            pos_hint: {'top':1}
        
        BoxLayout:
            orientation: 'vertical'
            padding: dp(10)
            spacing: dp(10)
            size_hint_y: None
            height: dp(200)
            pos_hint: {'center_x': 0.5, 'center_y': 0.4}

            Image:
                source: 'images/service.jpg'  # Update with your image file path
                size_hint_y: None
                height: dp(250)  # Adjust the height as needed
                pos_hint: {'center_x': 0.5}
                
            MDTextField:
                hint_text: "Tell us how we can help you"
                multiline: True
                

            MDRectangleFlatButton:
                text: "Submit"
                on_release: root.Submit()
                size_hint_x: None
                width: "150dp"
                pos_hint: {'center_x': 0.5}                        

'''
Builder.load_string(KV)

class ContactUsScreen(Screen):
    def go_back(self):
        self.manager.current = 'help'
        
    def Submit(self):    
        self.show_popup("Your Query has been submited. \nOur Technical Executive will respond you shortly.")
        self.manager.current = 'dashboard'

    def show_popup(self, text):
        dialog = MDDialog(
            title="Success",
            text=text,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda *args: dialog.dismiss()
                    # pos_hint = {"center_x": 0.5, "center_y": 0.5}
                )
            ]
        )
        dialog.open()    
        


