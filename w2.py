from kivy.lang import Builder
from kivymd.uix.screen import Screen
from kivymd.app import MDApp

import sqlite3
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivymd.uix.label import MDLabel
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

Window.size = (300, 500)
KV = '''
<WithdrawScreen>
    MDTopAppBar:
        left_action_items: [["arrow-left", lambda x: root.go_back()]]
        title: "Withdraw"
        pos_hint: {'top': 1}
    BoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(10)
        size_hint_y: None
        height: self.minimum_height
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint_x:None
        width:300
    
    
        MDLabel:
            id: wallet_label
            text: "Wallet Money:"  # Replace this with the actual wallet amount
            size_hint: 1, None
            font_size:"20sp"
            bold: True
            height:"20dp"
            halign: "center"
            valign: "center"
    
        BoxLayout:
            orientation: 'vertical'
            padding: dp(10)
            spacing: dp(10)
            size_hint_y: None
            height: self.minimum_height
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            size_hint_x:None
            width:300
    
            Spinner:
                id: currency_spinner
                text: 'Currency'
                values: ['INR', 'USD', 'EUROS', 'POUND']
                size_hint: None, None
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                size: "150dp", "50dp"
                on_text: root.manager.select_currency(self.text)
    
        MDTextField:
            id: mobile_textfield
            hint_text: "Mobile"
            helper_text: "Enter your mobile number"
            helper_text_mode: "on_focus"
            input_filter: "int"
    
        MDTextField:
            id: amount_textfield
            hint_text: "Amount"
            helper_text: "Enter withdrawal amount"
            helper_text_mode: "on_focus"
            input_filter: "float"
    
        MDRaisedButton:
            text: "Withdraw"
            on_release: root.manager.withdraw()

'''
Builder.load_string(KV)


class WithdrawScreen(Screen):
    def go_back(self):
        self.manager.current = 'dashboard'
    def create_tables_if_not_exist(self):
        # Connect to the database
        pass




class WalletApp(MDApp):
    def build(self):
        return Builder.load_string(KV)




if __name__ == "__main__":
    WalletApp().run()
