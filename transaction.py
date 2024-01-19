from kivy.lang import Builder
from kivymd.uix.screen import Screen

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

