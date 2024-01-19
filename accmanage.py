from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivy.storage.jsonstore import JsonStore

KV = '''
<AccmanageScreen>:
    Screen:
        MDScreen:
            BoxLayout:
                orientation: "vertical"
                MDTopAppBar:
                    title: 'Account Management'
                    elevation: 3
                    left_action_items: [['arrow-left', lambda x: root.go_back()]]
                    md_bg_color: "#1e75b9"
                    specific_text_color: "#ffffff"
                # Scrollable part
                ScrollView:
                
                    BoxLayout: 
                        size_hint_y: None
                        height: dp(320)
                        pos_hint: {'center_x': 0.45, 'y': 220}        

                        BoxLayout:
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height
                            spacing: '4dp'

                            Image:
                                source: 'images/accmanage.webp'  # Update with your image file path
                                size_hint_y: None
                                height: dp(180)  # Adjust the height as needed
                                pos_hint: {'center_x': 0.5} 

                            OneLineIconListItem:
                                text: "Add Bank Account"
                                on_release: root.manager.nav_account()
                                IconLeftWidget:
                                    icon: "account-plus"
                                    theme_text_color: 'Custom'
                                    text_color: get_color_from_hex("#3489eb")  
                            OneLineIconListItem:
                                text: "Remove Account"
                                IconLeftWidget:
                                    icon: "account-remove" 
                                    theme_text_color: 'Custom'
                                    text_color: get_color_from_hex("#3489eb") 
                            OneLineIconListItem:
                                text: "Close Account"
                                IconLeftWidget:
                                    icon: "account-cancel"
                                    theme_text_color: 'Custom'
                                    text_color: get_color_from_hex("#3489eb")                      
                        
'''
Builder.load_string(KV)

class AccmanageScreen(Screen):
    def go_back(self):
        self.manager.current = 'navbar'
