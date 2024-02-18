from anvil.tables import app_tables
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
from kivymd.uix.menu import MDDropdownMenu

Builder.load_string(
    """

<AddMoneyScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        size_hint_y: 0.1
        pos_hint: {"top":1}
         
        
        MDTopAppBar:
            title: 'Add Money'
            elevation: 3
            left_action_items: [['arrow-left', lambda x: root.go_back()]]
            md_bg_color: "#148EFE"
            specific_text_color: "#ffffff"
            pos_hint:{'top':1}
    
    MDBoxLayout:
        orientation: 'vertical'
        size_hint_y: 0.25 
        pos_hint: {"top":0.86} 
        #md_bg_color: "fefe16" 
        
        MDCard:
            orientation: 'vertical'
            size_hint: 0.9, None  # 90% of parent width
            height: dp(140)
            pos_hint: {"center_x": 0.5}
            elevation: 1
            radius: [20, 20, 20, 20]
            padding: dp(20)
            spacing: dp(20)
            md_bg_color: "#148EFE"
            MDLabel:
                text: 'Total Wallet Balance'
                theme_text_color: "Custom"  # Disable theme color
                text_color: 1, 1, 1, 1
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
    MDBoxLayout:
        orientation: 'vertical'
        size_hint_y: 0.5 
        pos_hint: {"top":0.60} 
        #md_bg_color: "fe1616"
        
        MDCard:
            orientation: 'vertical'
            size_hint: 0.9, None  # 90% of parent width
            height: dp(280)
            pos_hint: {"center_x": 0.5}
            elevation: 1
            radius: [20, 20, 20, 20]
            padding: dp(20)
            md_bg_color: "#148EFE"

            MDLabel:
                text: 'Add Money to Wallet'
                halign: 'left'  # Align text to the left
                valign: 'top'  # Align text to the top
                size_hint_y: None
                height: self.texture_size[1]
                pos_hint: {'center_y': 0.1}  # Align label to the left side of the MDCard
                theme_text_color: "Custom"  # Disable theme color
                text_color: 1, 1, 1, 1
            MDBoxLayout:
                padding: dp(5)
                spacing: dp(10)  # Adjust the spacing as needed
                adaptive_height: True
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}  # This will create a 10dp gap
                
                MDTextField:
                    id: balance
                    halign: 'center'
                    size_hint_y: None
                    height: dp(25)  # Adjust height as needed
                    mode: "fill"
                    fill_mode: True
                    radius: [15, 15, 15, 15]  # Rounded edges
                    padding: dp(5), dp(5)
                    theme_text_color: "Custom"
                    text_color: 0, 0, 0, 1  # Black text color
                    pos_hint: {'center_y': 0.5}
                    spacing: dp(5)
                
                MDRectangleFlatButton:
                    id: currency_dropdown
                    text: "Select Currency"
                    theme_text_color: "Custom"  # Disable theme color
                    text_color: 1, 1, 1, 1
                    line_color: 1, 1, 1, 1  # Black border color
                    size_hint: None, None
                    size: dp(100), dp(48)
                    pos_hint: {"center_x": 0.5, "center_y": 0.45}
                    on_release: root.currencyDropdown()
    
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
                text: "select bank account"
                #theme_text_color: "Custom"  # Disable theme color
                text_color: 1, 1, 1, 1
                line_color: 1, 1, 1, 1  # white border color
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
                    theme_text_color: "Custom"  # Disable theme color
                    text_color: 20/255, 142/255, 254/255, 1
                    md_bg_color: "#ffffff"
                    size_hint: 1, None  # Set the size_hint_x to 1 to fill the width
                    height: dp(50)
                    on_press: root.add_money()

       
""")


class AddMoneyScreen(Screen):

    def go_back(self):
        self.manager.current = 'dashboard'

    def __init__(self, **kwargs):
        super(AddMoneyScreen, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)

    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key in [27, 9]:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False

    def dropdown(self):
        try:
            store = JsonStore('user_data.json')
            phone = store.get('user')['value']["phone"]

            # Call the server function to fetch account details and bank names
            bank_names = app_tables.wallet_users_account.search(phone=phone)
            bank_names_str = [str(row['bank_name']) for row in bank_names]
            print(bank_names_str)
            if bank_names_str:
                # Create the menu list dynamically based on the fetched bank names
                self.menu_list = [
                    {"viewclass": "OneLineListItem", "text": bank_name,
                     "on_release": lambda x=bank_name: self.test(x)}
                    for bank_name in bank_names_str
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

        except Exception as e:
            print(f"Error fetching bank names: {e}")

        finally:
            # No need to close a connection in Firebase Realtime Database
            pass

    def test(self, text):
        self.account_number = None
        self.ids.bank_dropdown.text = text
        store = JsonStore('user_data.json')
        phone = store.get('user')['value']["phone"]

        try:
            # Call the server function to fetch account details and update dropdown
            matching_accounts = app_tables.wallet_users_account.search(phone=phone, bank_name=text)
            account = [str(row['account_number']) for row in matching_accounts]
            if matching_accounts:
                # Fetch the account number from the first matching account
                self.account_number = account[0]
                print(self.account_number)
            else:
                toast("Account not found")

            self.menu.dismiss()

        except Exception as e:
            print(f"Error fetching account number: {e}")

    def add_money(self):
        wallet_scr = self.manager.get_screen('Wallet')
        money = wallet_scr.ids.balance.text
        amount = float(money)
        # print("amount " + amount)
        bank_name = wallet_scr.ids.bank_dropdown.text
        date = datetime.now()
        currency = wallet_scr.ids.currency_dropdown.text
        rate_response = self.currency_rate(currency, amount)
        print(rate_response)
        if 'response' in rate_response and rate_response['meta']['code'] == 200:
            # Access the 'value' from the 'response' dictionary
            self.exchange_rate_value = rate_response['response']['value']
            print(f"The exchange rate value is: {self.exchange_rate_value}")
        else:
            print("Error fetching exchange rates.")
        store = JsonStore('user_data.json')
        phone = store.get('user')['value']["phone"]
        balance_table = app_tables.wallet_users_balance.get(phone=phone, currency_type=currency)
        print(balance_table)
        # Check if the amount is within the specified range
        if 500 <= amount <= 100000:
            if balance_table is None:
                app_tables.wallet_users_balance.add_row(
                    currency_type=currency,
                    balance=self.exchange_rate_value,
                    phone=phone
                )
            else:
                if balance_table["balance"] is not None:
                    new_e_money = self.exchange_rate_value + balance_table['balance']
                    balance_table['balance'] = new_e_money
                    balance_table.update()
                else:
                    new_e_money = self.exchange_rate_value
                    balance_table['balance'] = new_e_money
                    balance_table.update()
            try:
                app_tables.wallet_users_transaction.add_row(
                    receiver_phone=float(self.account_number),
                    phone=phone,
                    fund=self.exchange_rate_value,
                    date=date,
                    transaction_type="credit",
                    transaction_status="Wallet-Topup"
                )
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

    def currency_rate(self, currency_type, money):
        # Set API Endpoint and access key (replace 'API_KEY' with your actual API key)
        endpoint = 'convert'
        api_key = 'a2qfoReWfa7G3GiDHxeI1f9BFXYkZ2wT'

        # Set base currency and any other parameters (replace 'USD' with your desired base currency)
        base_currency = 'INR'
        target_currency = currency_type  # Replace with your desired target currency

        # Build the URL
        url = f'https://api.currencybeacon.com/v1/{endpoint}?from={base_currency}&to={currency_type}&amount={money}&api_key={api_key}'

        try:
            # Make the request
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses

            # Decode JSON response
            exchange_rates = response.json()

            return exchange_rates

        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")

        except requests.exceptions.RequestException as err:
            print(f"Request Error: {err}")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def update_balance(self, amount):
        # Update the text of the balance MDTextField with the selected amount
        self.ids.balance.text = str(amount)

    def show_currency_options(self, button):
        currency_options = ["INR", "GBP", "USD", "EUR"]
        self.menu_list = [
            {"viewclass": "OneLineListItem", "text": currency, "on_release": lambda x=currency: self.menu_callback(x)}
            for currency in currency_options
        ]
        print(button)
        # Create and open the dropdown menu
        self.menu = MDDropdownMenu(
            caller=button,
            items=self.menu_list,
            width_mult=4
        )
        self.menu.open()

    menu = None  # Add this line to declare the menu attribute
    options_button_icon_mapping = {
        "INR": "currency-inr",
        "GBP": "currency-gbp",
        "USD": "currency-usd",
        "EUR": "currency-eur"
    }

    def menu_callback(self, instance_menu_item):
        print(f"Selected currency: {instance_menu_item}")
        store = JsonStore('user_data.json')
        phone_no = store.get('user')['value']["phone"]
        total_balance = self.manager.get_total_balance(phone_no, instance_menu_item)
        # Convert the total balance to the selected currency

        self.ids.balance_lbl.text = f'balance: {total_balance} '
        print(total_balance)
        self.ids.options_button.icon = self.options_button_icon_mapping.get(instance_menu_item, "currency-inr")
        self.menu.dismiss()

    def currencyDropdown(self):
        try:
            # Manually set currencies
            currencies = ["INR", "USD", "EUR", "GBP", "JPY", "AUD"]

            # Create the menu list dynamically based on the fetched currencies
            self.menu_list = [
                {"viewclass": "OneLineListItem", "text": currency,
                 "on_release": lambda x=currency: self.selected_currency(x)}
                for currency in currencies
            ]

            # Create and open the dropdown menu
            self.menu = MDDropdownMenu(
                caller=self.ids.currency_dropdown,
                items=self.menu_list,
                width_mult=4
            )
            self.menu.open()
        except Exception as e:
            print(f"Error fetching currencies: {e}")

    def selected_currency(self, currency):
        wallet_scr = self.manager.get_screen('Wallet')
        wallet_scr.ids.currency_dropdown.text = currency
        self.menu.dismiss()
        print(currency)


class WalletApp(MDApp):
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(AddMoneyScreen(name='Wallet'))
        return screen_manager


if __name__ == '__main__':
    WalletApp().run()
