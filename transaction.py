from kivy.lang import Builder
from kivymd.uix.screen import Screen
import requests
import json
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.widget import Widget
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.list import OneLineListItem

KV = '''
<Transaction>:
    Screen:
        BoxLayout:
            orientation: 'vertical'

            MDTopAppBar:
                title: 'Transaction History'
                elevation: 3
                left_action_items: [['arrow-left', lambda x: root.go_back()]]
                md_bg_color: "#1e75b9"
                specific_text_color: "#ffffff"

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
                    hint_text: 'Search Transaction'
                    #on_text: root.search_transactions_card()
                    multiline: False
                    size_hint_x: 0.7
                    radius: [20, 20, 0, 0]
                    padding: dp(0)
                    background_color: 1, 1, 1, 0

            MDRaisedButton:
                text: 'Filter'
                #size_hint: None, None
                size: dp(50), dp(10)
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
                 
            # Scrollable part
            ScrollView:
                MDList:
                    id: transaction_list




# '''
Builder.load_string(KV)


class Transaction(Screen):

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

        # Get the full transaction history
        full_transaction_history = self.get_full_transaction_history()

        # Check if the structure is as expected
        if not isinstance(full_transaction_history, dict):
            print("Error: Unexpected structure for full_transaction_history")
            return
        # Convert the dictionary values to a list
        transactions_list = list(full_transaction_history.values())

        # Sort transactions by date in descending order
        transactions_list.sort(key=lambda x: x['date'], reverse=True)


        # Filter transactions based on the selected filter
        if filter_text == "All":
            filtered_transactions = transactions_list
        else:
            filtered_transactions = [transaction for transaction in transactions_list if transaction.get('type') == filter_text]

        # Display the filtered transactions in the UI
        self.display_transactions(filtered_transactions)

        if self.menu:
            self.menu.dismiss()

    def get_full_transaction_history(self):
        try:
            # Replace "your-project-id" with your actual Firebase project ID
            database_url = "https://e-wallet-realtime-database-default-rtdb.asia-southeast1.firebasedatabase.app/"

            # Get the phone number from user data
            phone = JsonStore('user_data.json').get('user')['value']["phone"]

            # Reference to the 'transactions' collection
            transactions_endpoint = f"{database_url}/transactions/{phone}/user_transactions.json"

            # Make a GET request to fetch the full transaction history
            response = requests.get(transactions_endpoint)

            if response.status_code == 200:
                full_transaction_history = json.loads(response.text)
                return full_transaction_history
            else:
                print(f"Error getting full transaction history. Status Code: {response.status_code}")
                return {}

        except Exception as e:
            print(f"Error getting full transaction history: {e}")
            return {}
        
    def display_transactions(self, transactions):
        trans_screen = self.manager.get_screen('transaction')
        trans_screen.ids.transaction_list.clear_widgets()

        current_date = ""

        for transaction_data in transactions:
            transaction_datetime = transaction_data['date']
            transaction_date = transaction_datetime.split(' ')[0]

            transaction_item = f"{transaction_data['description']}"

            if transaction_date != current_date:
                current_date = transaction_date
                header_text = f"[b]{transaction_date}[/b]"
                trans_screen.ids.transaction_list.add_widget(OneLineListItem(text=header_text, theme_text_color='Custom', text_color=[0, 0, 0, 1]))

            transaction_container = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(36))
            transaction_item_widget = OneLineListItem(text=transaction_item, theme_text_color='Custom', text_color=[0, 0, 0, 1])
            transaction_container.add_widget(transaction_item_widget)
            transaction_container.add_widget(Widget(size_hint_x=None, width=dp(20)))

            amount_color = [0, 0.5, 0, 1] if transaction_data['type'] == 'Credit' else [1, 0, 0, 1]
            amount_label = MDLabel(text=f"₹{transaction_data['amount']}", theme_text_color='Custom', text_color=amount_color, halign='right')
            transaction_container.add_widget(amount_label)

            trans_screen.ids.transaction_list.add_widget(transaction_container)        


    def go_back(self):
        self.manager.current = 'dashboard'

    def release(self):  # Explicitly define the release method for the root widget
        print("Root widget released!")



