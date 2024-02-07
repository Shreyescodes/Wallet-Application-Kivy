from datetime import datetime
import requests
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivymd.toast import toast
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import Screen

KV = '''
<WithdrawScreen>
    MDTopAppBar:
        left_action_items: [["arrow-left", lambda x: root.go_back()]]
        title: "Withdraw"
        md_bg_color: "#1e75b9"
        specific_text_color: "#ffffff"
        pos_hint: {'top': 1}
    BoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(10)
        size_hint_y: None
        height: self.minimum_height
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
    
        Image:
            source: 'images/withdraw.jpg'  # Update with your image file path
            size_hint_y: None
            height: dp(180)  # Adjust the height as needed
            pos_hint: {'center_x': 0.5} 

        BoxLayout:
            orientation: "vertical"
            padding: 5
            pos_hint:{'center_x':0.44}

        MDCard:
            radius: [1, 1, 1, 1]
            orientation: 'vertical'
            size_hint: 1, 0.4
            height: self.minimum_height
            #md_bg_color: 0.9, 0.9, 0.9, 1
            md_bg_color: "#e1eaea"

            BoxLayout:
                padding: "5dp"
                orientation: 'horizontal'
                spacing: "20dp"

                MDLabel:
                    id: balance_lbl
                    text: "Wallet Balance:"  # Replace this with the actual wallet amount
                    size_hint: 1, None
                    font_size:"18sp"
                    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                    bold: True
                    height:"18dp"
                    halign: "center"
                    valign: "center"

                MDIconButton:
                    id: options_button
                    icon: 'currency-inr'
                    pos_hint: {'center_x': 0.5}
                    on_release: root.show_currency_options(self)
                    padding: dp(20)
                    theme_text_color: 'Custom'
                    text_color: 0.117, 0.459, 0.725, 1 
                    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                    
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
                on_text: root.select_currency(self.text)
        
        MDRectangleFlatButton:
            id: bank_dropdown
            text: "select bank account"
            theme_text_color: "Custom"
            text_color: 0, 0, 0, 1  # White text color
            line_color: 0, 0, 0, 1  # Black border color
            size_hint: None, None
            on_release: root.dropdown()
            size: dp(200), dp(48)
            pos_hint: {'center_x': 0.5, 'center_y': 0.45}

        MDTextField:
            id: amount_textfield
            hint_text: "Amount"
            helper_text: "Enter withdrawal amount"
            helper_text_mode: "on_focus"
            input_filter: "float"
            hint_text_mode: "on_focus"
            
        MDRaisedButton:
            text: "Proceed"
            on_release: root.withdraw()
            pos_hint:{'center_x': 0.5}

'''
Builder.load_string(KV)


class WithdrawScreen(Screen):
    def go_back(self):
        self.manager.current = 'dashboard'

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

    def select_currency(self, currency):
        wdrw_scr = self.manager.get_screen('withdraw')
        wdrw_scr.ids.currency_spinner.text = currency

    def withdraw(self):
        wdrw_scr = self.manager.get_screen('withdraw')
        database_url = "https://e-wallet-realtime-database-default-rtdb.asia-southeast1.firebasedatabase.app/"

        # Get the entered mobile number, amount, and selected currency from your UI components
        amount = wdrw_scr.ids.amount_textfield.text
        selected_currency = wdrw_scr.ids.currency_spinner.text
        entered_mobile = JsonStore('user_data.json').get('user')['value']["phone"]
        selected_bank = wdrw_scr.ids.bank_dropdown.text

        # Validate inputs
        if not selected_bank or not amount or not selected_currency:
            self.show_error_popup("Please fill in all fields.")
            return

        try:
            amount = float(amount)
        except ValueError:
            self.show_error_popup("Invalid amount. Please enter a valid number.")
            return

        # Reference to the 'add_money' collection
        add_money_endpoint = f"{database_url}/add_money/{entered_mobile}.json"

        try:
            # Make a GET request to check if the user's account exists
            response = requests.get(add_money_endpoint)
            existing_record = response.json()

            # Check if the user's account exists (status code 200)
            if response.status_code == 200 and existing_record:
                # Check if 'e_money' is present in the existing record
                current_e_money = existing_record.get('e_money', 0)

                # Check if the wallet has sufficient funds
                if amount > current_e_money:
                    self.show_error_popup("Insufficient funds.")
                    return

                # Withdraw money (subtract the withdrawal amount from e_money)
                new_e_money_value = current_e_money - amount
                existing_record.update({'e_money': new_e_money_value})

                # Update the 'add_money' record with the new values
                response = requests.put(add_money_endpoint, json={
                    'currency_type': 'INR',
                    'e_money': new_e_money_value,
                    'phone': entered_mobile
                })

                # Convert the withdrawn amount to the selected currency
                converted_amount = self.manager.convert_to_currency(amount, selected_currency)

                # Reference to the 'transactions' collection
                transactions_endpoint = f"{database_url}/transactions/{entered_mobile}/user_transactions.json"
                transactions_collection = requests.post(
                    transactions_endpoint,
                    json={
                        'description': f'Withdrawal to A/c No. {self.account_number}',
                        'amount': amount,
                        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'phone': entered_mobile,
                        'account_number': self.account_number,
                        'type': 'Debit'
                    }
                )
 
                # wallet_label = wdrw_scr.ids.wallet_label
                # wallet_label.text = f"Wallet Money: ${new_e_money_value}"
                wallet_label = wdrw_scr.ids.balance_lbl
                wallet_label.text = f"Wallet Balance: ₹{new_e_money_value}"
           

                # Show success message with the withdrawn amount in the selected currency
                success_message = f"Withdrawal successful."
                self.manager.show_success_popup(success_message)
                self.manager.show_balance()

            else:
                self.manager.show_error_popup("User not found.")

        except Exception as e:
            print(f"Error withdrawing money: {e}")
            self.show_error_popup("An error occurred. Please try again.")

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