from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.uix.screen import Screen
from kivy.metrics import dp
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.list import OneLineListItem
from anvil.tables import app_tables
from kivymd.uix.spinner import MDSpinner

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
        self.manager.current = 'dashboard'

    def on_pre_enter(self, *args):
        # Called before the screen is displayed, show loading animation
        self.show_loading_animation()
        # Use Clock.schedule_once to simulate loading and update details after a delay
        Clock.schedule_once(lambda dt: self.update_details(), 2)

    def show_loading_animation(self):
        # Create and add an MDSpinner to the layout
        self.loading_spinner = MDSpinner(
            size_hint=(None, None),  # Use relative sizing for better scaling
            size=(dp(46), dp(46)),  # Adjust size as needed
            pos=(Window.width / 2 - dp(46) / 2, Window.height / 2 - dp(46) / 2)
        )
        self.ids.account_details_container.add_widget(self.loading_spinner)

    def hide_loading_animation(self):
        # Remove the loading MDSpinner from the layout
        self.ids.account_details_container.remove_widget(self.loading_spinner)

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

            self.hide_loading_animation()
        except Exception as e:
            print(f"Error updating details: {e}")
            self.hide_loading_animation()
