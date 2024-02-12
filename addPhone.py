from tkinter import Label

import requests
from anvil.tables import app_tables
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineListItem, MDList
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.toolbar import MDTopAppBar
from kivy.uix.boxlayout import BoxLayout as box_layout

KV = '''
<AddPhoneScreen>:
    Screen:
        BoxLayout:
            orientation: 'vertical'

            MDTopAppBar:
                title: root.top_app_bar_title
                elevation: 3
                left_action_items: [['arrow-left', lambda x: root.go_back()]]
                md_bg_color: app.theme_cls.primary_color

            BoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: dp(120)  # Adjust the height as needed

                MDBoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: dp(80)

                    MDIconButton:
                        icon: 'magnify'
                        theme_text_color: 'Custom'
                        text_color: [0, 0, 0, 1]

                    MDTextField:
                        id: search_text_card
                        hint_text: 'Search by New Phone Number'
                        multiline: False
                        size_hint_x: 0.7
                        radius: [20, 20, 0, 0]
                        padding: dp(0)
                        background_color: 1, 1, 1, 0
                        on_text_validate: root.on_search_text_entered()
                        pos_hint: {"center_y": 0.4}  # Adjust the value to move it down

                Widget:  # Spacer
                    size_hint_y: None
                    height: dp(10)  # Adjust the height as needed

                OneLineListItem:
                    id: search_result_item
                    text: "no result"
                    on_release: root.on_number_click(float(root.ids.search_text_card.text))

            MDBottomNavigation:
                spacing: dp(5)
                text_color_active: get_color_from_hex("F5F5F5")
                panel_color: app.theme_cls.primary_color

'''

Builder.load_string(KV)
Builder.load_string("""
<UserDetailsScreen>:
    BoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: root.top_app_bar_title
            elevation: 3
            left_action_items: [['arrow-left', lambda x: root.go_back()]]
            md_bg_color: app.theme_cls.primary_color

        ScrollView:
            BoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height

                Label:
                    text: 'Transaction History'
                    size_hint_y: None
                    height: dp(36)
                    font_size: 18
                    halign: 'center'

                BoxLayout:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: dp(400)

                    MDList:
                        id: transaction_list_mdlist

        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: dp(50)

            MDTextField:
                text: "This is a text box at the bottom."
                multiline: True
""")


class TransactionBetweenUsersScreen(MDScreen):
    sender_number = ""
    receiver_number = ""
    top_app_bar_title = ""
    transaction_list_mdlist = None

    def go_back(self):
        self.manager.current = 'dashboard'

    def on_top_app_bar_title(self, instance, value):
        app = MDApp.get_running_app()
        try:
            self.top_app_bar.title = value
        except AttributeError:
            print("Error: 'top_app_bar' not found")

    def fetch_transaction_history(self):
        phone = JsonStore("userdata.json").get("user")["value"]["phone"]
        response = app_tables.wallet_users_transaction.get(phone=phone)

        try:

            transaction_history = response.json()
            print(f"Transaction History Response: {transaction_history}")

            return transaction_history

        except requests.exceptions.RequestException as e:
            import traceback
            traceback.print_exc()
            print(f"Error fetching transaction history: {e}")
            return {}

    def display_transaction_history(self, transaction_history):
        if not self.transaction_list_mdlist:
            return

        self.transaction_list_mdlist.clear_widgets()

        if not transaction_history:
            item = MDLabel(text="No transactions found", font_size=20, size_hint_y=None, height=dp(50))
            self.transaction_list_mdlist.add_widget(item)
        else:
            scroll_view = ScrollView(size_hint=(1, None), height=dp(400), scroll_y=0)
            scroll_layout = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None,
                                      padding=[0, dp(10), 0, 0])

            for transaction_id, transaction in transaction_history.items():
                print(f"Processing transaction: {transaction}")

                sender_phone = transaction.get("phone", "")
                receiver_account_number = transaction.get("account_number", "")
                date = transaction.get("date", "")
                amount = transaction.get("amount", "")
                transaction_type = transaction.get("type", "")  # Get the "type" directly as a string

                # Check if both sender_phone and receiver_account_number match
                if sender_phone == self.sender_number and receiver_account_number == self.receiver_number:
                    transaction_layout = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None,
                                                   padding=[0, 0, 0, 0])

                    # Format date and time
                    date_time_split = date.split(" ")
                    formatted_date = date_time_split[0] if len(date_time_split) > 1 else date
                    formatted_time = date_time_split[1] if len(date_time_split) > 1 else ""

                    # Show date
                    date_label = MDLabel(text=f"{formatted_date}", font_size=16,
                                         halign='center' if transaction_type.lower() != "credit" else 'center')
                    transaction_layout.add_widget(date_label)

                    # Show amount
                    amount_label = MDLabel(text=f"Amount: ${amount:.2f}", font_size=24,
                                           halign='left' if transaction_type.lower() != "credit" else 'right')
                    transaction_layout.add_widget(amount_label)

                    # Show time
                    time_label = MDLabel(text=f"{formatted_time}", font_size=12,
                                         halign='left' if transaction_type.lower() != "credit" else 'right')
                    transaction_layout.add_widget(time_label)

                    scroll_layout.add_widget(transaction_layout)

            if not scroll_layout.children:
                item = MDLabel(text=" ", font_size=20, size_hint_y=None, height=dp(50))
                self.transaction_list_mdlist.add_widget(item)
            else:
                scroll_view.add_widget(scroll_layout)
                self.transaction_list_mdlist.add_widget(scroll_view)
                scroll_view.scroll_y = 0

                # Set the scroll position to the bottom
                Clock.schedule_once(lambda dt: setattr(scroll_view, 'scroll_y', 0), 0)

    def on_transaction_click(self, instance, receiver_number):
        self.receiver_number = receiver_number
        print(f"Receiver Number: {self.receiver_number}")

        # Fetch and display transaction history with the updated receiver_number
        transaction_history = self.fetch_transaction_history()
        self.display_transaction_history(transaction_history)

    def __init__(self, **kwargs):
        super(TransactionBetweenUsersScreen, self).__init__(**kwargs)

        try:
            self.top_app_bar = MDTopAppBar(
                title=self.top_app_bar_title,
                elevation=3,
                left_action_items=[['arrow-left', lambda x: self.go_back()]],
                md_bg_color=MDApp.get_running_app().theme_cls.primary_color
            )
        except AttributeError:
            print("Error: 'top_app_bar' not created")

        # Initialize transaction_list_mdlist as an MDList
        self.transaction_list_mdlist = MDList(padding=[0, 0])

        # Create a BoxLayout with vertical orientation to hold other widgets
        main_layout = BoxLayout(orientation='vertical', spacing=dp(0), padding=[0, dp(0), 0, 0])

        try:
            main_layout.add_widget(self.top_app_bar)

            # Nested BoxLayout for the middle section
            middle_layout = BoxLayout(orientation='vertical', spacing=dp(0))
            middle_layout.add_widget(self.transaction_list_mdlist)
            main_layout.add_widget(middle_layout)

            main_layout.add_widget(MDTextField(text="This is a text box at the bottom.", multiline=True))
        except AttributeError:
            print("Error: Adding widgets to main_layout")

        self.add_widget(main_layout)


class AddPhoneScreen(Screen):
    top_app_bar_title = "Add Phone Number"

    def go_back(self):
        self.manager.current = 'dashboard'

    def on_top_app_bar_title(self, instance, value):
        app = MDApp.get_running_app()
        try:
            self.top_app_bar.title = value
        except AttributeError:
            print("Error: 'top_app_bar' not found")

    def on_search_text_entered(self):
        number = float(self.ids.search_text_card.text)
        try:
            userdata = app_tables.wallet_users.get(phone=number)
            username = userdata['username']
            self.ids.search_result_item.text = username
            return username

        except Exception as e:
            print(e)
            return {}

    def on_number_click(self, number):
        username = self.on_search_text_entered()
        print(f"Selected username: {username}, Phone number: {number}")
        if username:
            # Create a new screen instance with the selected username and phone number
            next_screen = UserDetailsScreen(username=username, phone_number=number)
            # Switch to the new screen
            self.manager.add_widget(next_screen)
            self.manager.current = 'user_details'


class UserDetailsScreen(Screen):
    top_app_bar_title = ""
    def go_back(self):
        self.manager.current = 'addphone'

    def __init__(self, username='', phone_number='', **kwargs):
        super().__init__(**kwargs)
        self.username = username
        self.phone_number = phone_number
        self.top_app_bar_title = username
        self.transaction_list_mdlist = None  # Added attribute for MDList
        print(f"UserDetailsScreen initialized with username: {self.username}, Phone number: {self.phone_number}")
        if self.phone_number:
            transaction_history = self.fetch_transaction_history(self.phone_number)
            self.display_transaction_history(transaction_history)
        else:
            pass

    def fetch_transaction_history(self, receiver_phone):
        store = JsonStore('user_data.json')
        phone = store.get('user')['value']["phone"]
        print(type(receiver_phone))
        #print("phone" + receiver_phone)

        try:
            response = app_tables.wallet_users_transaction.get(phone=phone, receiver_phone=receiver_phone)
            transaction_history = response
            print(f"Transaction History Response: {transaction_history}")
            return transaction_history
        except requests.exceptions.RequestException as e:
            print(f"Error fetching transaction history: {e}")
            return {}

    def display_transaction_history(self, transaction_history):
        if not self.transaction_list_mdlist:
            return

        self.transaction_list_mdlist.clear_widgets()

        if not transaction_history:
            item = MDLabel(text="No transactions found", font_size=20, size_hint_y=None, height=dp(50))
            self.transaction_list_mdlist.add_widget(item)
        else:
            for transaction_id, transaction in transaction_history.items():
                # Display transactions based on your design preference
                transaction_layout = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None,
                                               padding=[dp(10), dp(10), dp(10), 0])

                # Format date and time
                date_time_split = transaction.get("date", "").split(" ")
                formatted_date = date_time_split[0] if len(date_time_split) > 1 else transaction.get("date", "")
                formatted_time = date_time_split[1] if len(date_time_split) > 1 else ""

                # Show date
                date_label = MDLabel(text=f"Date: {formatted_date}", font_size=16)
                transaction_layout.add_widget(date_label)

                # Show transaction type
                transaction_type_label = MDLabel(text=f"Type: {transaction.get('transaction_type', '')}", font_size=16)
                transaction_layout.add_widget(transaction_type_label)

                # Show transaction status
                transaction_status_label = MDLabel(text=f"Status: {transaction.get('transaction_status', '')}",
                                                   font_size=16)
                transaction_layout.add_widget(transaction_status_label)

                # Show amount
                amount_label = MDLabel(text=f"Amount: {transaction.get('fund', 0):.2f}", font_size=16)
                transaction_layout.add_widget(amount_label)

                # Show time
                time_label = MDLabel(text=f"Time: {formatted_time}", font_size=12)
                transaction_layout.add_widget(time_label)

                self.transaction_list_mdlist.add_widget(transaction_layout)


class WalletApp(MDApp):

    def build(self):
        # Initialize screen manager
        screen_manager = ScreenManager()

        # Add screens to the screen manager
        screen_manager.add_widget(AddPhoneScreen(name='add_phone'))
        # Add other screens as needed

        return screen_manager
