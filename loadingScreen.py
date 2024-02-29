from kivy.lang import Builder
from kivymd.uix.screen import Screen
loading_screen = """
<LoadingScreen>:
    BoxLayout:
        orientation: 'vertical'
        spacing: dp(20)
        MDBoxLayout:
            orientation: 'vertical'
        Image:
            source:"images/2.png"
            size_hint: None, None
            size: dp(60), dp(60)
            pos_hint: {'center_x': 0.5,'center_y':0.5} 
        MDBoxLayout:
            orientation: 'vertical'    
"""
Builder.load_string(loading_screen)


class loadingScreen(Screen):
    pass
