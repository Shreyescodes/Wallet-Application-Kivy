from kivy.lang import Builder
from kivymd.uix.button import MDFlatButton
from kivymd.uix.screen import Screen
from kivy.properties import ObjectProperty
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

                # Removed unnecessary MDLabel

                MDIconButton:
                    icon: "filter-variant"
                    pos_hint: {"center_x": 0.95}
                    theme_text_color: "Custom"
                    text_color: 0, 0, 1, 1  # Blue color for the icon
                    on_release: root.open_sort_filter()    

                ScrollView:
                    effect_kludge: True
                    MDList:
                        id: transaction_list


'''
Builder.load_string(KV)


class Transaction(Screen):
    filter_dialog = ObjectProperty(None)

    def open_sort_filter(self):
        if not self.filter_dialog:
            from kivymd.uix.dialog import MDDialog
            from kivymd.uix.list import MDList, OneLineListItem

            self.filter_dialog = MDDialog(
                title="Filter Payments",
                type="custom",
                content_cls=MDList,
                buttons=[
                    MDFlatButton(
                        text="CLEAR ALL", text_color=self.theme_cls.primary_color
                    ),
                    MDFlatButton(
                        text="APPLY", text_color=self.theme_cls.primary_color
                    ),
                ],
            )

            items = [
                OneLineListItem(text="Status"),  # Text for Status option
                OneLineListItem(text="Type"),  # Text for Type option
            ]
            self.filter_dialog.content_cls.add_widget(items[0])
            self.filter_dialog.content_cls.add_widget(items[1])

        self.filter_dialog.open()

    def go_back(self):
        existing_screen = self.manager.get_screen('transaction')
        self.manager.current = 'dashboard'
        self.manager.remove_widget(existing_screen)

    def __init__(self, **kwargs):
        super(Transaction, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)

    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key in [27, 9]:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False