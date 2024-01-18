from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import Screen

KV = '''
<HelpScreen>:
    Screen:
        MDScreen:
            BoxLayout:
                orientation: "vertical"
                MDTopAppBar:
                    title: 'Help'
                    elevation: 3
                    left_action_items: [['arrow-left', lambda x: root.go_back()]]
                    md_bg_color: "#1e75b9"
                    specific_text_color: "#ffffff"
                # Scrollable part
                ScrollView:
                
                    BoxLayout: 
                        size_hint_y: None
                        height: dp(160)
                        pos_hint: {'center_x': 0.45, 'y': 220}        

                        BoxLayout:
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height
                            spacing: '4dp'

                            OneLineIconListItem:
                                text: "Contact Us"
                                on_release: root.manager.nav_contactus()
                                IconLeftWidget:
                                    icon: "email-outline"
                                    theme_text_color: 'Custom'
                                    text_color: get_color_from_hex("#3489eb")  
                            OneLineIconListItem:
                                text: "App info"
                                IconLeftWidget:
                                    icon: "information-outline" 
                                    theme_text_color: 'Custom'
                                    text_color: get_color_from_hex("#3489eb") 
                            OneLineIconListItem:
                                text: "Terms and Policies"
                                IconLeftWidget:
                                    icon: "file-document-outline"
                                    theme_text_color: 'Custom'
                                    text_color: get_color_from_hex("#3489eb")                      
                        
'''
Builder.load_string(KV)

class HelpScreen(Screen):
    def go_back(self):
        self.manager.current = 'navbar'

    def nav_contactus(self):
        self.manager.current = 'contactus'    

    