from kivy.lang import Builder
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import Screen
from kivymd.uix.snackbar import Snackbar
import requests

KV = '''
<SignUpScreen>:
    BoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            left_action_items: [["arrow-left", lambda x: root.go_back()]]
            title: 'Sign Up'
            elevation: 5

        ScrollView:


            MDGridLayout:
                cols: 1
                adaptive_height: True
                padding: dp(16)
                required: True

                MDTextField:
                    id: gmail
                    hint_text: "Gmail"
                    required: True

                MDTextField:
                    id: username
                    hint_text: "Username"
                    required: True

                MDTextField:
                    id: password
                    hint_text: "Password"
                    password: True
                    required: True

                MDTextField:
                    id: phone_no
                    hint_text: "Phone Number"
                    required: True

                MDTextField:
                    id: aadhar_card
                    hint_text: "Aadhar Card Number"
                    required: True

                MDTextField:
                    id: pan_card
                    hint_text: "PAN Card Number"
                    required: True

                MDTextField:
                    id: address
                    hint_text: "Address"
                    required: True

                MDRectangleFlatButton:
                    text: "Sign Up"
                    pos_hint: {'center_x': 0.5}
                    on_release: root.signup()
          
'''
Builder.load_string(KV)


class SignUpScreen(Screen):
    def go_back(self):
        self.manager.current = 'landing'

    def signup(self):
        database_url = "https://e-wallet-realtime-database-default-rtdb.asia-southeast1.firebasedatabase.app/"
        current_screen = self.manager.get_screen('signup')
        gmail = current_screen.ids.gmail.text
        username = current_screen.ids.username.text
        password = current_screen.ids.password.text
        phone_no = current_screen.ids.phone_no.text
        aadhar_card = current_screen.ids.aadhar_card.text
        pan_card = current_screen.ids.pan_card.text
        address = current_screen.ids.address.text
        login_endpoint = f"{database_url}/login/{phone_no}.json"
        self.account_details(phone_no)
        self.add_money(phone_no)
        self.transactions(phone_no)
        try:
            # Check for duplicate phone numbers in Firebase
            if self.is_phone_number_registered(phone_no):
                Snackbar(text="Phone number already exists. Choose another.").open()
                return

            # Add user data to the 'login' collection in Firebase
            user_data = {
                'gmail': gmail,
                'username': username,
                'password': password,
                'phone': phone_no,
                'Aadhaar': aadhar_card,
                'pan': pan_card,
                'address': address
            }
            response = requests.put(login_endpoint, json=user_data)
            if response.status_code == 200:
                # Show a popup with a success message
                dialog = MDDialog(
                    title="Alert",
                    text="Successfully signed up.",
                    buttons=[
                        MDFlatButton(
                            text="OK",
                            on_release=lambda *args: (dialog.dismiss(), self.dismiss_and_navigate())
                        )
                    ]
                )
                dialog.open()
            else:
                print("Error adding user data:", response.text)
        except Exception as e:
            print(e)

    def is_phone_number_registered(self, phone_number):
        database_url = "https://e-wallet-realtime-database-default-rtdb.asia-southeast1.firebasedatabase.app/"
        response = requests.get(f"{database_url}/login.json",
                                params={'orderBy': '"phone"', 'equalTo': f'"{phone_number}"'})
        data = response.json()
        print(data)
        return data

    def dismiss_and_navigate(self):

        self.manager.current = 'signin'

    # Function to add data to the 'account_details' collection
    def account_details(self, phone):
        database_url = "https://e-wallet-realtime-database-default-rtdb.asia-southeast1.firebasedatabase.app/"
        account_details_endpoint = f"{database_url}/account_details/{phone}/accounts.json"
        account_details_data = {
            'account_holder_name': None,
            'account_number': None,
            'bank_name': None,
            'branch_name': None,
            'ifsc_code': None,
            'account_type': None,
            'phone': None
        }
        requests.post(account_details_endpoint, json=account_details_data)

    # Function to add data to the 'transactions' collection
    def transactions(self, phone):
        database_url = "https://e-wallet-realtime-database-default-rtdb.asia-southeast1.firebasedatabase.app/"
        transactions_endpoint = f"{database_url}/transactions/{phone}/transaction.json"
        transactions_data = {
            'amount': None,
            'description': None,
            'date': None,
            'phone': phone
        }
        requests.post(transactions_endpoint, json=transactions_data)

    def add_money(self, phone):
        database_url = "https://e-wallet-realtime-database-default-rtdb.asia-southeast1.firebasedatabase.app/"
        add_money_endpoint = f"{database_url}/add_money/{phone}.json"
        add_money_data = {
            'currency_type': None,
            'e_money': None,
            'phone': phone,
            'account_number': None
        }
        requests.post(add_money_endpoint, json=add_money_data)
