from kivymd.app import MDApp
from datetime import datetime
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivy.properties import StringProperty
from kivy.metrics import dp
import requests
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.menu import MDDropdownMenu
from kivymd.toast import toast
from kivymd.uix.list import OneLineListItem
from kivy.base import EventLoop
from kivy.core.window import Window

Builder.load_string(
    """

<AddMoneyScreen>:
    
    canvas.before:
        Color:
            rgba: 0.8706, 0.9451, 1, 1  # Background color (#DEF1FF)
        Rectangle:
            pos: self.pos
            size: self.size
    MDBoxLayout:
        
        
        orientation: 'vertical'
        padding: [dp(10), dp(0), dp(10), dp(20)]  # Padding: left, top, right, bottom
        spacing: dp(20)
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}
        size_hint_y: None
        height: self.minimum_height
        
        MDTopAppBar:
            title: 'Money Transfer'
            elevation: 3
            left_action_items: [['arrow-left', lambda x: root.go_back()]]
            md_bg_color: "#1e75b9"
            specific_text_color: "#ffffff"
            pos_hint:{'top':1}
            
        MDCard:
            orientation: 'vertical'
            size_hint: 0.9, None  # 90% of parent width
            height: dp(140)
            pos_hint: {"center_x": 0.5}
            elevation: 1
            radius: [20, 20, 20, 20]
            padding: dp(20)
            spacing: dp(20)

            MDLabel:
                text: 'Total Wallet Balance'
                halign: 'left'  # Align text to the left
                valign: 'top'  # Align text to the top
                size_hint_y: None
                height: self.texture_size[1]
                pos_hint: {'x': 0}  # Align label to the left side of the MDCard

            MDBoxLayout:
                padding: dp(10)
                spacing: dp(10)
                adaptive_height: True
                pos_hint: {'center_x': 0.5, 'center_y': 0.5} 
                    
                MDTextField:
                    id: balance_lbl
                    text: 'Balance'
                    halign: 'center'
                    readonly: True
                    size_hint_y: None
                    height: dp(25)  # Adjust height as needed
                    mode: "fill"
                    fill_mode: True
                    radius: [15, 15, 15, 15]  # Rounded edges
                    padding: dp(5), dp(5)
                    theme_text_color: "Custom"
                    text_color: 0, 0, 0, 1  # Black text color
                  
                    
                MDIconButton:
                    id: options_button
                    icon: "currency-inr"
                    pos_hint: {'center_y':0.5}
                    md_bg_color: 0.7, 0.7, 0.7, 1  # Blue background color
                    theme_text_color: "Custom"
                    text_color: 0, 0, 0, 1  # White text color
                    on_release: root.show_currency_options(self)
                                        

        MDCard:
            orientation: 'vertical'
            size_hint: 0.9, None  # 90% of parent width
            height: dp(280)
            pos_hint: {"center_x": 0.5}
            elevation: 1
            radius: [20, 20, 20, 20]
            padding: dp(20)

            MDLabel:
                text: 'Add Money to Wallet'
                halign: 'left'  # Align text to the left
                valign: 'top'  # Align text to the top
                size_hint_y: None
                height: self.texture_size[1]
                pos_hint: {'x': 0}  # Align label to the left side of the MDCard

            MDBoxLayout:
                size_hint_y: None
                height: dp(10)  # This will create a 10dp gap

            MDTextField:
                id: balance
                halign: 'center'
                size_hint_y: None
                height: dp(20)
                mode: "fill"
                fill_mode: True
                radius: [15, 15, 15, 15]  # Rounded edges
                padding: dp(5), dp(5)
                theme_text_color: "Custom"
                text_color: 0, 0, 0, 1  # Black text color
                line_color_normal: 0, 0, 0, 1 

            MDSeparator:
                height: dp(1)

            MDBoxLayout:
                padding: dp(10)
                spacing: dp(10)
                adaptive_height: True
                
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                MDFlatButton:
                    text: '+100'
                    size_hint: 1, None  # Set the size_hint_x to 1 to fill the width
                    height: dp(40)
                    width: dp(64)
                    md_bg_color: 0.85, 0.85, 0.85, 1
                    on_release: root.update_balance(100)
                    
                MDFlatButton:
                    text: '+200'
                    size_hint: 1, None  # Set the size_hint_x to 1 to fill the width
                    width: dp(64)
                    height: dp(40)
                    md_bg_color: 0.85, 0.85, 0.85, 1
                    on_release: root.update_balance(200)
                MDFlatButton:
                    text: '+500'
                    size_hint: 1, None
                    width: dp(64)
                    height: dp(40)
                    md_bg_color: 0.85, 0.85, 0.85, 1
                    on_release: root.update_balance(500)
                MDFlatButton:
                    text: '+1000'
                    0size_hint: 1, None
                    width: dp(64)
                    height: dp(40)
                    md_bg_color: 0.85, 0.85, 0.85, 1
                    on_release: root.update_balance(1000)
            MDRectangleFlatButton:
                id: bank_dropdown
                text: "change bank account"
                theme_text_color: "Custom"
                text_color: 0, 0, 0, 1  # White text color
                line_color: 0, 0, 0, 1  # Black border color
                size_hint: None, None
                on_release: root.dropdown()
                size: dp(200), dp(48)
                pos_hint: {'center_x': 0.5, 'center_y': 0.45}        
            MDBoxLayout:
                padding: dp(10)
                adaptive_height: True
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                MDRaisedButton:
                    text: 'Proceed to add'
                    md_bg_color: 0, 180/255, 219/255, 1
                    size_hint: 1, None  # Set the size_hint_x to 1 to fill the width
                    height: dp(50)
                    on_press: root.add_money()
    MDBoxLayout:
        size_hint_y: None
        height: dp(50)
        pos_hint: {'center_x': 0.5, 'center_y': 0.1}
        size_hint_x: None
        width: dp(100)

       
""")

class AddMoneyScreen(Screen):

    def go_back(self):
        self.manager.current = 'dashboard'

    def __init__(self, **kwargs):
        super(AddMoneyScreen, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)


    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key in [27,9]:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False

    def dropdown(self):
        try:
            store = JsonStore('user_data.json')
            phone_number = store.get('user')['value']["phone"]

            # Reference to the 'accounts' subcollection under the user's document
            accounts_endpoint = f"https://e-wallet-realtime-database-default-rtdb.asia-southeast1.firebasedatabase.app/account_details/{phone_number}/accounts.json"

            # Make a GET request to fetch the user's account details
            response = requests.get(accounts_endpoint)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the JSON response
                account_details = response.json()

                # Check if the 'accounts' subcollection exists
                if account_details:
                    # Extract unique bank names
                    bank_names = set(entry['bank_name'] for entry in account_details.values())

                    # Create the menu list dynamically based on the fetched bank names
                    self.menu_list = [
                        {"viewclass": "OneLineListItem", "text": bank_name,
                         "on_release": lambda x=bank_name: self.test(x)}
                        for bank_name in bank_names
                    ]

                    # Create and open the dropdown menu
                    self.menu = MDDropdownMenu(
                        caller=self.ids.bank_dropdown,
                        items=self.menu_list,
                        width_mult=4
                    )
                    self.menu.open()
                else:
                    toast("No accounts found")

            else:
                toast(f"Failed to fetch account details. Status code: {response.status_code}")

        except Exception as e:
            print(f"Error fetching bank names: {e}")

        finally:
            # No need to close a connection in Firebase Realtime Database
            pass

    def test(self, text):
        self.account_number = None
        self.ids.bank_dropdown.text = text
        store = JsonStore('user_data.json')
        phone_number = store.get('user')['value']["phone"]

        try:
            # Reference to the 'accounts' sub collection under the user's document
            accounts_endpoint = f"https://e-wallet-realtime-database-default-rtdb.asia-southeast1.firebasedatabase.app/account_details/{phone_number}/accounts.json"

            # Make a GET request to fetch the user's account details
            response = requests.get(accounts_endpoint)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the JSON response
                account_details = response.json()

                # Query the documents with the specified bank name
                matching_accounts = [
                    account for account in account_details.values() if account['bank_name'] == text
                ]

                # Check if any matching accounts were found
                if matching_accounts:
                    # Fetch the account number from the first matching account
                    self.account_number = matching_accounts[0]['account_number']
                else:
                    toast("Account not found")
            else:
                toast(f"Failed to fetch account details. Status code: {response.status_code}")
            self.menu.dismiss()
        except Exception as e:
            print(f"Error fetching account number: {e}")

    def add_money(self):
        topup_scr = self.manager.get_screen('Wallet')
        amount = float(topup_scr.ids.balance.text)
        bank_name = topup_scr.ids.bank_dropdown.text
        store = JsonStore('user_data.json')
        phone = store.get('user')['value']["phone"]

        # Check if the amount is within the specified range
        if 100 <= amount <= 100000:
            try:
                # Replace "your-project-id" with your actual Firebase project ID
                database_url = "https://e-wallet-realtime-database-default-rtdb.asia-southeast1.firebasedatabase.app/"

                # Reference to the 'add_money' collection
                add_money_endpoint = f"{database_url}/add_money/{phone}.json"

                # Make a PUT request to check if the user's account exists and update the 'add_money' record
                response = requests.get(add_money_endpoint)
                print(response.json())
                # Check if the user's account exists (status code 200)
                if response.status_code == 200:
                    existing_record = response.json()

                    # Check if 'e_money' is present in the existing record
                    current_e_money = existing_record.get('e_money', 0)
                    print(current_e_money)
                    # Calculate the new values
                    new_e_money = current_e_money + amount

                    # Update the record with the new values
                    response = requests.put(add_money_endpoint, json={
                        'currency_type': 'INR',
                        'e_money': new_e_money,
                        'phone': phone
                    })
                else:
                    # No existing record found, add a new record with only the amount
                    response = requests.put(add_money_endpoint, json={
                        'currency_type': 'INR',
                        'e_money': amount,
                        'phone': phone
                    })

                # Reference to the 'transactions' collection
                transactions_endpoint = f"{database_url}/transactions/{phone}/user_transactions.json"
                current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Make a POST request to add a new transaction record
                response = requests.post(transactions_endpoint, json={
                    'description': 'Wallet',
                    'amount': amount,
                    'date': current_datetime,
                    'phone': phone,
                    'account_number': self.account_number
                })

                # Show a success toast
                toast("Money added successfully.")
                self.manager.current = 'dashboard'
                self.manager.show_balance()

            except Exception as e:
                print(f"Error adding money: {e}")
                toast("An error occurred. Please try again.")

        else:
            # Show an error toast
            toast("Invalid amount. Please enter an amount between 500 and 100000.")

    def update_balance(self, amount):
        # Update the text of the balance MDTextField with the selected amount
        self.ids.balance.text = str(amount)



    def get_transaction_history(self):
        try:
            # Replace "your-project-id" with your actual Firebase project ID
            database_url = "https://e-wallet-realtime-database-default-rtdb.asia-southeast1.firebasedatabase.app/"

            # Get the phone number from user data
            phone = JsonStore('user_data.json').get('user')['value']["phone"]

            # Reference to the 'transactions' collection
            transactions_endpoint = f"{database_url}/transactions/{phone}/user_transactions.json"

            # Make a GET request to fetch the transaction history
            response = requests.get(transactions_endpoint)

            if response.status_code == 200:
                transaction_history = response.json()

                trans_screen = self.manager.get_screen('transaction')
                # Clear existing widgets in the MDList
                trans_screen.ids.transaction_list.clear_widgets()

                # Display the transaction history in LIFO order
                for transaction_id, transaction_data in sorted(transaction_history.items(), key=lambda x: x[1]['date'],
                                                               reverse=True):
                    transaction_item = f"{transaction_data['amount']}₹\n" \
                                       f"{transaction_data['description']}\n"

                    trans_screen.ids.transaction_list.add_widget(OneLineListItem(text=transaction_item))

            else:
                print(f"Error getting transaction history. Status Code: {response.status_code}")

        except Exception as e:
            print(f"Error getting transaction history: {e}")

    menu = None  # Add this line to declare the menu attribute
    options_button_icon_mapping = {
        "INR": "currency-inr",
        "POUND": "currency-gbp",
        "USD": "currency-usd",
        "EUROS": "currency-eur"
    }

    def show_currency_options(self, button):
        currency_options = ["INR", "POUND", "USD", "EUROS"]
        self.menu_list = [
            {"viewclass": "OneLineListItem", "text": currency, "on_release": lambda x=currency: self.menu_callback(x)}
            for currency in currency_options
        ]

        # Create and open the dropdown menu
        self.menu = MDDropdownMenu(
            caller=button,
            items=self.menu_list,
            width_mult=4
        )
        self.menu.open()

    def menu_callback(self, instance_menu_item):
        print(f"Selected currency: {instance_menu_item}")
        store = JsonStore('user_data.json')
        phone_no = store.get('user')['value']["phone"]
        total_balance = self.manager.get_total_balance(phone_no)
        # Convert the total balance to the selected currency
        converted_balance = self.convert_currency(total_balance, instance_menu_item)

        # Update the label with the selected currency and converted balance
        self.ids.balance_lbl.text = f'{converted_balance} {instance_menu_item}'
        self.ids.options_button.icon = self.options_button_icon_mapping.get(instance_menu_item, "currency-inr")
        self.menu.dismiss()

    def convert_currency(self, amount, to_currency):
        # Implement your currency conversion logic here
        # You may use an external API or a predefined exchange rate table

        # For simplicity, let's assume a basic conversion formula
        exchange_rate = {
            "USD": 0.014,  # Example exchange rates, replace with actual rates
            "EUROS": 0.012,
            "INR": 1.0,
            "POUND": 0.011
        }

        converted_amount = amount * exchange_rate.get(to_currency, 1.0)
        return round(converted_amount, 2)  # Round to two decimal places    
    def go_back(self):
        self.manager.current = 'dashboard'
class WalletApp(MDApp):
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(AddMoneyScreen(name='Wallet'))
        return screen_manager
    
if __name__ == '__main__':
    WalletApp().run()