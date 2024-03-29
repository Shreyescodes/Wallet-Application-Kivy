from kivy.lang import Builder
from kivymd.uix.screen import Screen
from kivy.base import EventLoop

KV = '''
<Transaction>:
    Screen:
        BoxLayout:
            orientation: 'vertical'
            spacing: dp(20)
            pos_hint:{'top':1}

            MDTopAppBar:
                title: 'Transaction History'
                elevation: 3
                left_action_items: [['arrow-left', lambda x: root.go_back()]]
                md_bg_color: "#148EFE"
                specific_text_color: "#ffffff"
                pos_hint: {'top': 1}

            BoxLayout:
                orientation: 'vertical'
                spacing: dp(20)
                padding: dp(5),0,dp(5),0


                # # Scrollable part
                # ScrollView:
                #     MDList:
                #         id: transaction_list

                MDCard:
                    orientation: "vertical"
                    size_hint: None, None
                    size: "300dp", "30dp"
                    md_bg_color: "#C4E3FF"
                    radius: [dp(15), dp(15), dp(15), dp(15)]
                    pos_hint: {"center_x": 0.5}

                    MDLabel:
                        text: "Search Transaction"
                        theme_text_color: "Custom"
                        text_color: 0, 0, 0, 1
                        font_size: "15sp"
                        halign: "center"
                        size_hint_y: None
                        height: self.texture_size[1] + dp(10)  # Adjust height based on text size

                ScrollView:
                    effect_kludge: True
                    MDList:
                        id: transaction_list




'''
Builder.load_string(KV)


class Transaction(Screen):

    def go_back(self):
        existing_screen = self.manager.get_screen('transaction')
        self.manager.current = 'dashboard'
        self.manager.remove_widget(existing_screen)

    def release(self):  # Explicitly define the release method for the root widget
        print("Root widget released!")

    def __init__(self, **kwargs):
        super(Transaction, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)

    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key in [27, 9]:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False