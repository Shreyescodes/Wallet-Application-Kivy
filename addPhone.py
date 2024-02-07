from tkinter import Label

import requests
from kivy.clock import Clock
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

            Widget:  # Spacer
                size_hint_y: None
                height: dp(10)

            MDCard:
                orientation: 'vertical'
                size_hint_y: None
                height: dp(500)
                radius: [10, 10, 10, 10]
                spacing: dp(20)

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

                    MDIconButton:
                        icon: 'magnify'
                        theme_text_color: 'Custom'
                        text_color: [0, 0, 0, 0]

                ScrollView:
                    MDList:
                        id: phone_list_mdlist
                        size_hint_y: None
                        height: self.minimum_height

            MDBottomNavigation:
                spacing: dp(5)
                text_color_active: get_color_from_hex("F5F5F5")
                panel_color: app.theme_cls.primary_color
'''

Builder.load_string(KV)

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

    def on_enter(self, *args):
        app = MDApp.get_running_app()
        self.sender_number = app.authenticated_user_number
        selected_phone_number = getattr(app, 'selected_phone_number', '')

        try:
            self.top_app_bar.title = f"{selected_phone_number}"
        except AttributeError:
            print("Error: 'top_app_bar' not found")

        transaction_history = self.fetch_transaction_history()
        self.display_transaction_history(transaction_history)

    def fetch_transaction_history(self):
        url = f"https://e-wallet-realtime-database-default-rtdb.asia-southeast1.firebasedatabase.app/transactions/{self.sender_number}/user_transactions.json"
        print(f"Fetching from URL: {url}")

        try:
            response = requests.get(url)
            response.raise_for_status()

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
        main_layout = BoxLayout(orientation='vertical', spacing=dp(0),padding=[0, dp(0), 0, 0])

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

    def on_enter(self):
        database_url = "https://e-wallet-realtime-database-default-rtdb.asia-southeast1.firebasedatabase.app"
        self.phone_user_data = self.fetch_phone_user_data(database_url)

        if hasattr(self.ids, 'phone_list_mdlist'):
            self.ids.phone_list_mdlist.clear_widgets()
            self.populate_phone_list(self.phone_user_data)
        else:
            print("Error: phone_list_mdlist does not exist.")

    def fetch_phone_user_data(self, database_url):
        account_details_endpoint = f"{database_url}/account_details.json"

        try:
            response = requests.get(account_details_endpoint)
            response.raise_for_status()

            data = response.json()
            phone_user_data = {}
            for number, details in data.items():
                if 'accounts' in details:
                    for account_id, account_details in details['accounts'].items():
                        username = account_details.get('account_holder_name', '')
                        phone_user_data[number] = username

            return phone_user_data

        except requests.exceptions.RequestException as e:
            print(f"Error fetching phone numbers and usernames: {e}")
            return {}

    def populate_phone_list(self, phone_user_data):
        if not self.ids.phone_list_mdlist:
            return

        self.ids.phone_list_mdlist.clear_widgets()

        if not phone_user_data:
            return

        if self.ids.search_text_card.text.strip():
            search_text = self.ids.search_text_card.text.strip()
            if search_text in phone_user_data:
                number = search_text
                username = phone_user_data[search_text]
                self.show_username_in_search_result(number, username)
            else:
                self.show_not_found_in_search_result()
        else:
            for number, username in phone_user_data.items():
                item = OneLineListItem(text=f"[size=28]{number}[/size] ",
                                       on_release=lambda x, num=number: self.on_number_click(num))
                self.ids.phone_list_mdlist.add_widget(item)

    def on_search_text_entered(self):
        database_url = "https://e-wallet-realtime-database-default-rtdb.asia-southeast1.firebasedatabase.app"
        self.phone_user_data = self.fetch_phone_user_data(database_url)
        self.populate_phone_list(self.phone_user_data)

    def show_username_in_search_result(self, number, username):
        if not self.ids.phone_list_mdlist:
            return

        box_layout = BoxLayout(
            orientation="vertical", size_hint_y=None, height=dp(30),
            padding=(dp(25), 0, 0, 0)
        )

        username_label = MDLabel(
            text=f"[size=21][b]{username}[/b][/size]",
            markup=True,
            size_hint_y=None,
            height=dp(40),
            text_size=(None, dp(40)),
            theme_text_color="Custom",
            text_color=[0.435, 0.305, 0.216, 1],
        )
        number_label = MDLabel(
            text=f"[size=17]{number}[/size]", markup=True, size_hint_y=None, height=dp(2)
        )

        box_layout.add_widget(username_label)
        box_layout.add_widget(number_label)

        box_layout.bind(on_touch_down=lambda x, touch=None: self.on_number_click(number))

        self.ids.phone_list_mdlist.clear_widgets()

        if hasattr(self.ids, 'phone_list_mdlist'):
            self.ids.phone_list_mdlist.add_widget(box_layout)
        else:
            print("Error: phone_list_mdlist is not available.")

    def show_not_found_in_search_result(self):
        if not self.ids.phone_list_mdlist:
            return

        phone_list_mdlist = self.ids.get('phone_list_mdlist')
        if phone_list_mdlist:
            phone_list_mdlist.clear_widgets()
            item = OneLineListItem(text="Number not found", font_size=80)
            phone_list_mdlist.add_widget(item)
        else:
            print("Error: phone_list_mdlist is not available.")

    def on_number_click(self, number):
        app = MDApp.get_running_app()

        transaction_screen = next((screen for screen in app.root.screens if screen.name == 'transaction_bw_2users'),
                                  None)

        if not transaction_screen:
            transaction_screen = TransactionBetweenUsersScreen(name='transaction_bw_2users')
            app.root.add_widget(transaction_screen)

        transaction_screen.receiver_number = number
        transaction_screen.sender_number = self.ids.search_text_card.text.strip()  # Use the selected number as the sender_number
        transaction_screen.top_app_bar_title = f"Transactions - {number}"
        app.root.current = 'transaction_bw_2users'
        app = MDApp.get_running_app()
        app.selected_phone_number = number


class WalletApp(MDApp):

    def build(self):
        # Initialize screen manager
        screen_manager = ScreenManager()

        # Add screens to the screen manager
        screen_manager.add_widget(AddPhoneScreen(name='add_phone'))
        # Add other screens as needed

        return screen_manager