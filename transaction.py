from kivy.lang import Builder
from kivymd.uix.screen import Screen
from kivy.base import EventLoop
from kivy.core.window import Window
KV = '''
<Transaction>:
    Screen:
        BoxLayout:
            orientation: 'vertical'

            MDTopAppBar:
                title: 'Transaction History'
                elevation: 3
                left_action_items: [['arrow-left', lambda x: root.go_back()]]
                md_bg_color: app.theme_cls.primary_color
            # Scrollable part
            ScrollView:
                MDList:
                    id: transaction_list




'''
Builder.load_string(KV)


class Transaction(Screen):
    def go_back(self):
        self.manager.current = 'dashboard'

    def release(self):  # Explicitly define the release method for the root widget
        print("Root widget released!")

    def __init__(self, **kwargs):
        super(Transaction, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)


    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key in [27,9]:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False

