from kivy.lang import Builder
from kivymd.uix.screen import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp
from kivy.storage.jsonstore import JsonStore
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem

from anvil.tables import app_tables

KV = '''
<AccmanageScreen>:
    BoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "Account Management"
            left_action_items: [['arrow-left', lambda x: root.go_back()]]
            right_action_items: [["bank",lambda x: root.nav_account()]]
            elevation:4
        ScrollView:
            GridLayout:
                cols: 1
                spacing: dp(10)
                size_hint_y: None
                height: self.minimum_height
                id: account_details_container
        MDBottomAppBar:
            MDTopAppBar:
                mode: 'end'
                type: 'bottom'
                icon: 'bank'
                on_action_button: root.nav_account()        
'''
Builder.load_string(KV)

class AccmanageScreen(Screen):
    def go_back(self):
        self.manager.current = 'navbar'

    def on_pre_enter(self, *args):
        # Called before the screen is displayed, update the details here
        self.update_details()

    def nav_account(self):
        self.manager.current = 'addaccount'
    def update_details(self):
        try:
            store = JsonStore('user_data.json')
            phone = store.get('user')['value']["phone"]

            # Call the server function to fetch account details and bank names
            bank_names = app_tables.wallet_users_account.search(phone=phone)
            bank_names_str = [str(row['bank_name']) for row in bank_names]

            # Clear existing widgets in the GridLayout
            account_details_container = self.ids.account_details_container
            account_details_container.clear_widgets()

            # Add OneLineListItems for each bank name
            for bank_name in bank_names_str:
                list_item = OneLineListItem(text=bank_name)
                account_details_container.add_widget(list_item)

        except Exception as e:
            print(f"Error updating details: {e}")