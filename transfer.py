from datetime import datetime
import requests
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivymd.toast import toast
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import Screen

kv_string = '''
<TransferScreen>
    MDScreen:
        MDTopAppBar:
            title: 'Money Transfer'
            elevation: 3
            left_action_items: [['arrow-left', lambda x: root.go_back()]]
            md_bg_color: "#1e75b9"
            specific_text_color: "#ffffff"
            pos_hint:{'top':1} 

        BoxLayout:
            orientation: 'vertical'
            padding: dp(10)
            spacing: dp(20)
            size_hint_y: None
            height: self.minimum_height
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}

            Image:
                source: 'images/trans.jpg'  # Update with your image file path
                size_hint_y: None
                height: dp(170)  # Adjust the height as needed
                pos_hint: {'center_x': 0.5}    


            MDTextField:
                id:amount_field
                mode:'rectangle'
                hint_text: "Amount"
                helper_text: "Enter the amount to transfer"
                helper_text_mode: "on_focus"
                input_type: "number"
                spacing: dp(10)
                #pos_hint: {"center_x": 0.5, "center_y": 0.8}
                #width:300

            MDTextField:
                id:mobile_no_field
                hint_text: "Mobile no"
                helper_text: "Enter Receiver's mobile number"
                helper_text_mode: "on_focus"
                input_type: "number"
                # pos_hint: {"center_x": 0.5, "center_y": 0.7}
                # size_hint_x:None
                # width:300


            Spinner:
                id: currency_spinner
                text: 'Currency'
                values: ['INR', 'USD', 'EUROS', 'POUND']
                size_hint: None, None
                pos_hint: {'center_x': 0.5, 'center_y': 0.35}
                size: "150dp", "50dp"
                # on_text: app.select_currency(self.text)
                md_bg_color: 52/255.0, 171/255.0, 235/255.0,0  
                canvas.before:
                    Color:
                        rgba: 52/255.0, 171/255.0, 235/255.0,0  # Set the background color (in this case, a dark gray)
                    Rectangle:
                        pos: self.pos
                        size: self.size   

            MDRaisedButton:
                text: "Transfer Money"
                on_release: root.transfer_money()
                pos_hint: {"center_x": 0.5, "center_y": 0.27}

'''
Builder.load_string(kv_string)


class TransferScreen(Screen):
    def go_back(self):
        self.manager.current = 'dashboard'

    import requests
    from kivymd.toast import toast
    from kivymd.uix.dialog import MDDialog
    from kivymd.uix.button import MDFlatButton
    from datetime import datetime

    def transfer_money(self):
        # Get data from the text fields and spinner
        amount = float(self.ids.amount_field.text)
        receiver_phone = self.ids.mobile_no_field.text
        currency = self.ids.currency_spinner.text

        store = JsonStore('user_data.json')
        sender_phone = store.get('user')['value']["phone"]
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Replace "your-project-id" with your actual Firebase project ID
        database_url = "https://e-wallet-realtime-database-default-rtdb.asia-southeast1.firebasedatabase.app/"

        # Reference to the 'add_money' collection
        add_money_endpoint = f"{database_url}/add_money/{sender_phone}.json"

        try:
            # Make a GET request to check if the sender's account exists
            response = requests.get(add_money_endpoint)
            sender_record = response.json()

            # Check if the sender's account exists (status code 200)
            if response.status_code == 200 and sender_record:
                # Check if 'e_money' is present in the sender's record
                current_e_money_sender = sender_record.get('e_money', 0)

                # Check if the sender has sufficient balance
                if current_e_money_sender < amount:
                    toast("Insufficient balance")
                    return

                # Calculate the new balance for the sender
                new_e_money_sender = current_e_money_sender - amount


                # Reference to the receiver's document
                receiver_add_money_endpoint = f"{database_url}/add_money/{receiver_phone}.json"
                receiver_login_endpoint = f"{database_url}/login/{receiver_phone}.json"
                # Make a GET request to check if the receiver's account exists
                response = requests.get(receiver_add_money_endpoint)
                receiver_record = response.json()
                response2=requests.get(receiver_login_endpoint)
                receivers_login_record=response2.json()

                # Check if the receiver's account exists (status code 200)
                if response.status_code == 200 and receiver_record:
                    # Check if 'e_money' is present in the receiver's record
                    current_e_money_receiver = receiver_record.get('e_money', 0)

                    # Calculate the new balance for the receiver
                    new_e_money_receiver = current_e_money_receiver + amount

                    # Update the receiver's record with the new balance
                    response = requests.put(receiver_add_money_endpoint, json={
                        'currency_type': 'INR',
                        'e_money': new_e_money_receiver,
                        'phone': receiver_phone
                    })
                    response = requests.put(add_money_endpoint, json={
                        'currency_type': 'INR',
                        'e_money': new_e_money_sender,
                        'phone': sender_phone
                    })
                    # Reference to the 'transactions' collection for sender
                    sender_transactions_endpoint = f"{database_url}/transactions/{sender_phone}/user_transactions.json"

                    # Make a POST request to add a new transaction record for sender
                    response = requests.post(sender_transactions_endpoint, json={
                        'description': f'send to {receiver_phone}',
                        'amount': amount,
                        'date': current_datetime,
                        'phone': sender_phone,
                        'account_number': receiver_phone,
                        'type': 'Debit'
                    })

                    # Reference to the 'transactions' collection for receiver
                    receiver_transactions_endpoint = f"{database_url}/transactions/{receiver_phone}/user_transactions.json"

                    # Make a POST request to add a new transaction record for receiver
                    response = requests.post(receiver_transactions_endpoint, json={
                        'description': f'received from {sender_phone}',
                        'amount': amount,
                        'date': current_datetime,
                        'phone': receiver_phone,
                        'account_number': sender_phone,
                        'type': 'Credit'
                    })

                    # Show success message
                    toast("Money sent successfully")
                    self.manager.get_total_balance(sender_phone)
                    self.manager.show_balance()
                    self.manager.current = 'dashboard'
                elif response2.status_code == 200 and receivers_login_record:
                    response2 = requests.put(receiver_add_money_endpoint, json={
                        'currency_type': 'INR',
                        'e_money': amount,
                        'phone': receiver_phone
                    })
                    new_e_money_sender = current_e_money_sender - amount

                    # Update the sender's record with the new balance
                    response2 = requests.put(add_money_endpoint, json={
                        'currency_type': 'INR',
                        'e_money': new_e_money_sender,
                        'phone': sender_phone
                    })
                    sender_transactions_endpoint = f"{database_url}/transactions/{sender_phone}/user_transactions.json"

                    # Make a POST request to add a new transaction record for sender
                    response2 = requests.post(sender_transactions_endpoint, json={
                        'description': f'send to {receiver_phone}',
                        'amount': amount,
                        'date': current_datetime,
                        'phone': sender_phone,
                        'account_number': receiver_phone,
                        'type': 'Debit'
                        
                    })

                    # Reference to the 'transactions' collection for receiver
                    receiver_transactions_endpoint = f"{database_url}/transactions/{receiver_phone}/user_transactions.json"

                    # Make a POST request to add a new transaction record for receiver
                    response2 = requests.post(receiver_transactions_endpoint, json={
                        'description': f'received from {sender_phone}',
                        'amount': amount,
                        'date': current_datetime,
                        'phone': receiver_phone,
                        'account_number': sender_phone,
                        'type': 'Credit'
                    })
                    toast("Money sent successfully")
                    self.manager.get_total_balance(sender_phone)
                    self.manager.show_balance()
                    self.manager.current = 'dashboard'
                else:
                    # Receiver's phone number is not registered, show a dialogue box indicating the same
                    self.show_not_registered_dialog()

            else:
                # Sender's phone number is not registered, show a dialogue box indicating the same
                self.show_not_registered_dialog()

        except ValueError:
            toast("Invalid amount")

        except Exception as e:
            print(f"Error transferring money: {e}")

        finally:
            # No need to close a connection in Firestore, as it's managed automatically
            pass

    def show_not_registered_dialog(self):
        # Show a dialog indicating that the receiver's phone number is not registered
        dialog = MDDialog(
            title="Receiver Not Registered",
            text="The provided phone number is not registered. Consider inviting the user to join.",
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda *args: dialog.dismiss()
                )
            ]
        )
        dialog.open()


