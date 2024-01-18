from datetime import datetime
import requests
from kivymd.toast import toast
from kivymd.uix.screen import Screen
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.menu import MDDropdownMenu

KV = """
<Topup>
    Screen:
        MDTopAppBar:
            left_action_items: [["arrow-left", lambda x: root.go_back()]]
            right_action_items: [["bank", lambda x: root.manager.nav_account()]]
            title: "Top Up"
            md_bg_color: "#1e75b9"
            specific_text_color: "#ffffff"
            pos_hint: {'top': 1}

        BoxLayout:
            orientation: 'vertical'
            padding: dp(10)
            spacing: dp(10)
            size_hint_y: None
            height: dp(400)
            pos_hint: {'center_x': 0.5, 'center_y': 0.4}

            Image:
                source: 'images/addmoney.png'  # Update with your image file path
                size_hint_y: None
                height: dp(300)  # Adjust the height as needed
                pos_hint: {'center_x': 0.5}    

            RelativeLayout:

            MDTextField:
                id: amount_field
                hint_text: "Enter Amount"
                mode: "rectangle"
                keyboardType: "numeric"
                required: True
                size_hint: None, None
                size: dp(320), dp(48)  # Adjust the size as needed
                pos_hint: {'center_x': 0.5, 'center_y': 0.65}

            MDRectangleFlatButton:
                id: bank_dropdown
                text: "change bank account"
                theme_text_color: "Custom"
                text_color: 0, 0, 0, 1  # White text color
                line_color: 0, 0, 0, 1  # Black border color
                size_hint: None, None
                on_release: root.dropdown()
                size: dp(100), dp(48)
                pos_hint: {'center_x': 0.5, 'center_y': 0.45}

            MDRaisedButton:
                text: "Add Money"
                on_press: root.add_money()
                size_hint: None, None
                size: dp(200), dp(48)
                pos_hint: {'center_x': 0.5, 'center_y': 0.3}

"""
Builder.load_string(KV)

class Topup(Screen):
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

    def add_money(self):
        topup_scr = self.manager.get_screen('topup')
        amount = float(topup_scr.ids.amount_field.text)
        bank_name = topup_scr.ids.bank_dropdown.text
        store = JsonStore('user_data.json')
        phone = store.get('user')['value']["phone"]

        # Check if the amount is within the specified range
        if 500 <= amount <= 100000:
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
                    'description': 'topup',
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