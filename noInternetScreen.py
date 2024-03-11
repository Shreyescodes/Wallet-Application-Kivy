from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.screen import Screen

KV = '''
<NoInternetPage>:
    BoxLayout:
        orientation: 'vertical'
        #spacing: dp(20)
        padding: dp(20)
        BoxLayout:
            orientation: 'vertical'
        Image:
            source: 'images/no-internet.png'
            size_hint_y: None
            height: dp(100)
            valign:"center"
            
    
        MDLabel:
            text: 'No Internet Connection'
            font_size: '18sp'
            halign: 'center'
            theme_text_color: "Custom"
            text_color: 0, 0, 0, 1
        
        MDRaisedButton:
            text: "Retry"
            pos_hint:{"center_x":0.5}
            on_release: root.manager.connect_to_anvil(0)
                
        BoxLayout:
            orientation: 'vertical'    
'''
Builder.load_string(KV)

class NoInternetPage(Screen):
    pass


class NoInternetApp(MDApp):
    def build(self):
        Builder.load_string(KV)
        sm = ScreenManager()
        nI = NoInternetPage(name="no_internet")
        sm.add_widget(nI)
        return sm


if __name__ == '__main__':
    NoInternetApp().run()
