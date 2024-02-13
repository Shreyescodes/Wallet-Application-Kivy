from datetime import datetime
import requests
from anvil.tables import app_tables
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivymd.toast import toast
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import Screen
from kivy.base import EventLoop
from kivy.core.window import Window
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
    def __init__(self, **kwargs):
        super(WithdrawScreen, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)
    def go_back(self):
        self.manager.current = 'dashboard'

    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key in [27,9]:
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

    def select_currency(self, currency):
        wdrw_scr = self.manager.get_screen('withdraw')
        wdrw_scr.ids.currency_spinner.text = currency

    def withdraw(self):
        wdrw_scr = self.manager.get_screen('withdraw')
        # Get the entered mobile number, amount, and selected currency from your UI components
        amount = wdrw_scr.ids.amount_textfield.text
        currency = wdrw_scr.ids.currency_spinner.text
        date = datetime.now()
        phone = JsonStore('user_data.json').get('user')['value']["phone"]
        balance_table = app_tables.wallet_users_balance.get(phone=phone, currency_type=currency)
        selected_bank = wdrw_scr.ids.bank_dropdown.text
        # Validate inputs
        if not selected_bank or not amount or not currency:
            self.show_error_popup("Please fill in all fields.")
            return

        try:
            amount = float(amount)
        except ValueError:
            self.show_error_popup("Invalid amount. Please enter a valid number.")
            return

        try:
            if balance_table is not None:
                old_balance = balance_table['balance']
                if amount <= old_balance:
                    new_balance = old_balance - amount
                    balance_table['balance'] = new_balance
                    balance_table.update()
                else:
                    toast("balance is less than entered amount")
            else:
                toast("you dont have a balance in this currency type")
            app_tables.wallet_users_transaction.add_row(
                receiver_phone=float(self.account_number),
                phone=phone,
                fund=amount,
                date=date,
                transaction_type="debit"
            )

            success_message = f"Withdrawal successful."
            self.manager.show_success_popup(success_message)
            self.manager.show_balance()
        except Exception as e:
            print(f"Error withdrawing money: {e}")
            self.manager.show_error_popup("An error occurred. Please try again.")
