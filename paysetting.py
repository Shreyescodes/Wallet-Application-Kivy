from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import Screen

KV = '''
<PaysettingScreen>:
    Screen:
        MDScreen:
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

   