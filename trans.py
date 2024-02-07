from kivy.lang import Builder
from kivymd.uix.screen import Screen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

import requests

KV = '''
<WalletApp>:
    Transaction:

<Transaction>:
    Screen:
        MDGridLayout:
            cols: 1
            spacing: dp(10)
            padding: dp(5), dp(5), dp(5), dp(5)
            radius: [10, 10, 10, 10]

            MDTopAppBar:
                title: 'Transaction History'
                elevation: 3
                left_action_items: [['arrow-left', lambda x: root.go_back()]]
                right_action_items: [['bell', lambda x: root.show_notification()]]
                md_bg_color: app.theme_cls.primary_color

            MDCard:
                orientation: 'vertical'
                size_hint_y: None
                height: dp(50)
                radius: [10, 10, 10, 10]
                spacing: dp(50)

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
                        hint_text: 'Search by Name, Amount or Date'
                        on_text: root.search_transactions_card()
                        multiline: False
                        size_hint_x: 0.7
                        radius: [20, 20, 0, 0]
                        padding: dp(0)
                        background_color: 1, 1, 1, 0

                    MDIconButton:
                        icon: 'magnify'
                        theme_text_color: 'Custom'
                        text_color: [0, 0, 0, 0]

            MDRaisedButton:
                text: 'Filter v'
                size_hint: None, None
                size: dp(100), dp(20)
                on_release: root.show_menu(self)
                radius: [60, 60, 60, 60]
                pos_hint: {'center_x': 0.5}
                canvas.before:
                    Color:
                        rgba: 0, 0, 0, 0
                    Rectangle:
                        size: self.size
                        pos: self.pos
                text_color: 0, 0, 0, 1

            MDCard:
                orientation: 'vertical'
                padding: dp(10), dp(10), dp(10), dp(10)
                size_hint_y: None
                height: dp(380)
                spacing: dp(20)
                radius: [10, 10, 10, 10]

                ScrollView:
                    MDList:
                        id: transaction_list

            MDBottomNavigation:
                spacing: dp(5)
                text_color_active: get_color_from_hex("F5F5F5")
                panel_color: app.theme_cls.primary_color
                MDBottomNavigationItem:
                    name: 'home'
                    text: 'Home'
                    icon: 'home'
                    on_tab_release: root.on_tab_selected('dashboard')
                MDBottomNavigationItem:
                    name: 'insurance'
                    text: 'Insurance'
                    icon: 'shield'
                    on_tab_release: root.on_tab_selected('insurance')
                MDBottomNavigationItem:
                    name: 'stores'
                    text: 'Stores'
                    icon: 'store'
                    on_tab_release: root.on_tab_selected('stores')
                MDBottomNavigationItem:
                    name: 'history'
                    text: 'History'
                    icon: 'history'
                    on_tab_release: root.on_tab_selected('history')
'''

Builder.load_string(KV)


class WalletApp(App):
    def build(self):
        self.scr_mgr = ScreenManager()
        return self.scr_mgr

    def get_icon_color(self):
        return [0, 0, 0, 1]


class Transaction(Screen):
    def __init__(self, **kwargs):
        super(Transaction, self).__init__(**kwargs)

        self.filter_button = MDRaisedButton(
            text="Filter",
            size_hint=(None, None),
            size=(dp(80), dp(40)),
            on_release=self.show_menu,
        )
        self.menu = None

    def show_menu(self, button):
        options = [
            {"viewclass": "OneLineListItem", "text": "All", "on_release": lambda x="All": self.set_filter(x)},
            {"viewclass": "OneLineListItem", "text": "Credit", "on_release": lambda x="Credit": self.set_filter(x)},
            {"viewclass": "OneLineListItem", "text": "Debit", "on_release": lambda x="Debit": self.set_filter(x)},
        ]
        self.menu = MDDropdownMenu(caller=button, items=options, position="center", width_mult=3)
        self.menu.open()

    def set_filter(self, filter_text):
        print(f"Filter selected: {filter_text}")
        if self.menu:
            self.menu.dismiss()

    def go_back(self):
        self.manager.current = 'dashboard'

    def on_tab_selected(self, tab_name):
        if tab_name == 'dashboard':
            self.manager.current = 'dashboard'
        else:
            print(f"Selected tab: {tab_name}")

    def show_notification(self):
        print("Notification icon clicked!")

    def search_transactions_card(self):
        search_text = self.ids.search_text_card.text.lower()
        transactions = self.fetch_transactions_from_database()
        searched_transactions = []

        for transaction in transactions:
            if search_text in transaction["account_number"].lower() or search_text in str(
                    transaction["amount"]) or search_text in transaction["date"]:
                searched_transactions.append(transaction)

        self.update_transaction_list(searched_transactions)

    def update_transaction_list(self, transactions):
        transaction_list = self.ids.transaction_list
        transaction_list.clear_widgets()

        for transaction in transactions:
            symbol = "＋" if transaction.get('type') == 'addition' else "-"

            # Customize font sizes
            description_font_size = 20
            amount_font_size = 20
            date_font_size = 13

            # Add space between account number and amount
            space = " " * 35 # Adjust the number of spaces as needed

            # Remove the rjust(45) to allow the amount to take its natural length
            amount_text = f"[color={'#00FF00' if transaction.get('type') == 'addition' else '#8b0000'}]" \
                          f"{symbol} {transaction['amount']:.2f} ₹[/color]"

            transaction_list.add_widget(
                TwoLineListItem(
                    text=f"[size={description_font_size}]{transaction['account_number']}{space}[/size]"
                         f"[size={amount_font_size}]{amount_text}[/size]",
                    secondary_text=f"[size={date_font_size}]{transaction['date']}[/size]"
                )
            )

    def fetch_transactions_from_database(self):
        try:
            url = 'https://e-wallet-realtime-database-default-rtdb.asia-southeast1.firebasedatabase.app/transactions/9380660939/user_transactions.json'
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                transactions = [{"account_number": entry["account_number"], "amount": float(entry["amount"]),
                                 "date": entry["date"]} for entry in data.values()]

                return transactions

            else:
                print(f"Failed to fetch data. Status code: {response.status_code}")
                return []

        except Exception as e:
            print(f"Error fetching transactions from the database: {e}")
            return []



