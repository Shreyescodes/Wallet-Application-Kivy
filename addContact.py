from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.textfield import MDTextField


# KV = '''
# <AddContactScreen>:
#     Screen:
#         BoxLayout:
#             orientation: 'vertical'

#             MDTopAppBar:
#                 title: 'Add Contact'
#                 elevation: 3
#                 left_action_items: [['arrow-left', lambda x: root.go_back()]]
#                 md_bg_color: app.theme_cls.primary_color
#             # Scrollable part
#             ScrollView:
#                 MDList:
#                     id: contact_list

#             MDCard:
#                 orientation: 'vertical'
#                 size_hint_y: None
#                 height: dp(50)
#                 radius: [10, 10, 10, 10]
#                 spacing: dp(50)

#                 MDBoxLayout:
#                     orientation: 'horizontal'
#                     size_hint_y: None
#                     height: dp(80)

#                     MDIconButton:
#                         icon: 'magnify'
#                         theme_text_color: 'Custom'
#                         text_color: [0, 0, 0, 1]

#                     MDTextField:
#                         id: search_text_card
#                         hint_text: 'Search by Name or Phone Number'
#                         multiline: False
#                         size_hint_x: 0.7
#                         radius: [20, 20, 0, 0]
#                         padding: dp(0)
#                         background_color: 1, 1, 1, 0

#             MDRaisedButton:
#                 text: 'Filter'
#                 size_hint: None, None
#                 size: dp(100), dp(20)
#                 radius: [60, 60, 60, 60]
#                 pos_hint: {'center_x': 0.5}
#                 canvas.before:
#                     Color:
#                         rgba: 0, 0, 0, 0
#                     Rectangle:
#                         size: self.size
#                         pos: self.pos
#                 text_color: 0, 0, 0, 1

#             MDCard:
#                 orientation: 'vertical'
#                 padding: dp(10), dp(10), dp(10), dp(10)
#                 size_hint_y: None
#                 height: dp(380)
#                 spacing: dp(20)
#                 radius: [10, 10, 10, 10]

#                 ScrollView:
#                     MDList:
#                         id: contact_list

#             MDBottomNavigation:
#                 spacing: dp(5)
#                 text_color_active: get_color_from_hex("F5F5F5")
#                 panel_color: app.theme_cls.primary_color
                
# '''
# Builder.load_string(KV)


# class AddContactScreen(Screen):
#     def go_back(self):
#         self.manager.current = 'dashboard'

########################

KV = '''
<AddContactScreen>:
    Screen:
        MDScreen:
            BoxLayout:
                orientation: "vertical"
                MDTopAppBar:
                    title: 'Select Contact'
                    elevation: 3
                    left_action_items: [['arrow-left', lambda x: root.go_back()]]
                    #right_action_items: [['magnify', lambda x: root.search()]]
                    md_bg_color: "#1e75b9"
                    specific_text_color: "#ffffff"

                # Scrollable part
                ScrollView:
                    BoxLayout: 
                        orientation: "vertical"
                        size_hint_y: None
                        height: dp(120)
                        pos_hint: {'center_x': 0.45, 'y': 220}        

                        # OneLineIconListItem:
                        #     text: "Contacts on G-wallet"

                        BoxLayout:
                            orientation: "horizontal"
                            size_hint_y: None
                            height: self.minimum_height
                            spacing: '4dp'

                            MDIconButton:
                                icon: 'magnify'
                                theme_text_color: 'Custom'
                                text_color: [0, 0, 0, 1]

                            CustomMDTextField:
                                id: search_text_card
                                hint_text: 'Search name or phone number'
                                multiline: False
                                size_hint_x: 0.7
                                radius: [20, 20, 0, 0]
                                padding: dp(0)
                                background_color: 1, 1, 1, 0

                        OneLineIconListItem:
                            text: "Contacts on G-wallet"        

                        # MDRaisedButton:
                        #     text: 'Filter'
                        #     size_hint: None, None
                        #     size: dp(100), dp(20)
                        #     radius: [60, 60, 60, 60]
                        #     pos_hint: {'center_x': 0.5}
                        #     canvas.before:
                        #         Color:
                        #             rgba: 0, 0, 0, 0
                        #         Rectangle:
                        #             size: self.size
                        #             pos: self.pos
                        #     text_color: 0, 0, 0, 1
                            
'''
Builder.load_string(KV)

class CustomMDTextField(MDTextField):
    pass

class AddContactScreen(Screen):
    def go_back(self):
        self.manager.current = 'dashboard'

    def search(self):
        pass

##################################
            



