from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.screen import Screen

Window.size = (300, 500)
KV = ('''
<QRScreen>:
    MDTopAppBar:
        left_action_items: [["arrow-left", lambda x: root.go_back()]]
        title: "Top Up"
        pos_hint: {'top': 1}
        
    BoxLayout:
        orientation: 'vertical'
        size_hint: None, None
        size: 200, 350  # Adjust the size of your card
        
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}  # Center the card
        Widget:
        MDCard:
            orientation: "vertical"
            size_hint: None, None
            size: 250, 350  # Same as the size of the BoxLayout
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            # md_bg_color: 0.9, 0.9, 0.9, 1
            
            BoxLayout:
                orientation: 'vertical'
                padding: 10

                Image:
                    source:'qr_code.png'
    MDFlatButton:
        text: 'Or Scan' 
        size_hint: None, None
        md_bg_color: 0.9, 0.9, 0.9, 1
        pos_hint:{'center_y': 0.2,'center_x': 0.5}               
                                     
''')

Builder.load_string(KV)


class QRScreen(Screen):
    def go_back(self):
        self.manager.current = 'dashboard'


class WalletApp(MDApp):
    pass


if __name__ == '__main__':
    WalletApp().run()
"""
BoxLayout:
        orientation: 'vertical'
        RelativeLayout:
            MDCard:
                orientation: 'vertical'
                size_hint_y: None
                height: "10dp"
                padding: "10dp"
                pos_hint: {'center_x': 0.5, 'center_y': 0.005}
                Image:
                    id: qr_code_image
                    source: 'qr_code.png'
                    size_hint: None, None
                    size: 300, 300
                    allow_stretch: True
                    keep_ratio: True
                    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                    background_color: 1, 1, 1, 1  # Set background color to white
                MDLabel:
"""
