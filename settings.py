from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivy.storage.jsonstore import JsonStore

KV = '''
<SettingsScreen>:
    Screen:
        MDScreen:
            BoxLayout:
                orientation: "vertical"
                MDTopAppBar:
                    title: 'Settings'
                    elevation: 3
                    left_action_items: [['arrow-left', lambda x: root.go_back()]]
                    md_bg_color: "#1e75b9"
                    specific_text_color: "#ffffff"
                # Scrollable part
                ScrollView:
                
                    BoxLayout: 
                        size_hint_y: None
                        height: dp(215)
                        pos_hint: {'center_x': 0.45, 'y': 220}        

                        BoxLayout:
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height
                            spacing: '4dp'

                            OneLineIconListItem:
                                text: "Payment Settings"
                                on_release: root.manager.nav_paysetting()
                                IconLeftWidget:
                                    icon: "wallet"
                                    theme_text_color: 'Custom'
                                    text_color: get_color_from_hex("#3489eb")  
                            OneLineIconListItem:
                                text: "Help & Support"
                                on_release: root.manager.nav_help()
                                IconLeftWidget:
                                    icon: "help-circle" 
                                    theme_text_color: 'Custom'
                                    text_color: get_color_from_hex("#3489eb") 
                            OneLineIconListItem:
                                text: "Profile Settings"
                                on_release: root.edit_profile()  
                                IconLeftWidget:
                                    icon: "account-cog"
                                    theme_text_color: 'Custom'
                                    text_color: get_color_from_hex("#3489eb")     
                            OneLineIconListItem:
                                text: "App info"
                                IconLeftWidget:
                                    icon: "information-outline" 
                                    theme_text_color: 'Custom'
                                    text_color: get_color_from_hex("#3489eb")                  
                        
'''
Builder.load_string(KV)

class SettingsScreen(Screen):
    def go_back(self):
        self.manager.current = 'navbar'

    def edit_profile(self):
        edit_screen = self.manager.get_screen('edituser')

        store = JsonStore('user_data.json').get('user')['value']

        edit_screen.ids.username.text = store["username"]
        edit_screen.ids.email.text = store["gmail"]
        edit_screen.ids.phone.text = store["phone"]
        edit_screen.ids.password.text = store["password"]
        edit_screen.ids.aadhaar.text = store["Aadhaar"]
        edit_screen.ids.pan.text = store["pan"]
        edit_screen.ids.address.text = store["address"]
        self.manager.current = 'edituser'