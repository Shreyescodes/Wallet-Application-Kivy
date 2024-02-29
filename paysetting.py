from kivy.lang import Builder
from kivymd.uix.screen import Screen
from kivy.core.window import Window

KV = '''
<PaysettingScreen>:
    Screen:
        MDScreen:
            on_pre_enter: self.bind_keyboard()
            on_pre_leave: self.unbind_keyboard()

            BoxLayout:
                orientation: 'vertical'
                Label:
                    text: 'PaysettingScreen Content'
            BoxLayout:
                orientation: "vertical"
                MDTopAppBar:
                    title: 'Payment Settings'
                    elevation: 3
                    left_action_items: [['arrow-left', lambda x: root.go_back()]]
                    md_bg_color: "#1e75b9"
                    specific_text_color: "#ffffff"
                # Scrollable part
                ScrollView:
                
                    BoxLayout: 
                        size_hint_y: None
                        height: dp(220)
                        pos_hint: {'center_x': 0.45, 'y': 220}        

                        BoxLayout:
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height
                            spacing: '4dp'

                            OneLineIconListItem:
                                text: "UPI Settings"
                                IconLeftWidget:
                                    icon: "at"
                                    theme_text_color: 'Custom'
                                    text_color: get_color_from_hex("#3489eb")  
                            OneLineIconListItem:
                                text: "Auto Topup"
                                IconLeftWidget:
                                    icon: "refresh-auto" 
                                    theme_text_color: 'Custom'
                                    text_color: get_color_from_hex("#3489eb") 
                            OneLineIconListItem:
                                text: "UPI International"
                                IconLeftWidget:
                                    icon: "web"
                                    theme_text_color: 'Custom'
                                    text_color: get_color_from_hex("#3489eb") 
                            OneLineIconListItem:
                                text: "Reminders"
                                IconLeftWidget:
                                    icon: "bell-check-outline"
                                    theme_text_color: 'Custom'
                                    text_color: get_color_from_hex("#3489eb")     
                                                          
                        
'''
Builder.load_string(KV)


class PaysettingScreen(Screen):
    def go_back(self):
        self.manager.current = 'settings'

    def __init__(self, **kwargs):
        super(PaysettingScreen, self).__init__(**kwargs)
        lambda x: Window.bind(on_keyboard=self.on_key)
        print("hello")

    def on_key(self, key):
        # 27 is the key code for the back button on Android
        print(key)
        if key in [27, 9]:
            self.manager.current = 'settings'

            return True  # Indicates that the key event has been handled
        return False
