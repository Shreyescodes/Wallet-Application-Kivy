import requests
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import Screen
from kivymd.uix.snackbar import Snackbar

KV_STRING = '''
<AddAccountScreen>
    name: 'addaccount'
    BoxLayout:
        orientation: 'vertical'
        spacing: dp(10)
        # padding: dp(10)
        pos_hint: {'top': 1}

        MDTopAppBar:
            title: 'Add Account'
            elevation: 3
            left_action_items: [['arrow-left', lambda x: root.go_back()]]
            md_bg_color: "#1e75b9"
            specific_text_color: "#ffffff"
            size_hint_y: None  # Disable automatic height adjustment
            height: dp(56)  # Set the desired height of the MDTopAppBar

        ScrollView:
            BoxLayout:
                orientation: 'vertical'
                spacing: dp(5)
                padding: dp(20)

                # Profile Details
                MDTextField:
                    id: account_holder_name
                    hint_text: "Account Holder's Name"
                    mode: "rectangle"
                    multiline: False

                MDTextField:
                    id: account_number
                    hint_text: "Account Number"
                    mode: "rectangle"
                    multiline: False

                MDTextField:
                    id: confirm_account_number
                    hint_text: "Confirm Account Number"
                    mode: "rectangle"
                    multiline: False

                MDTextField:
                    id: bank_name
                    hint_text: "Bank Name"
                    mode: "rectangle"
                    multiline: False

                MDTextField:
                    id: branch_name
                    hint_text: "Branch Name"
                    mode: "rectangle"
                    multiline: False

                MDTextField:
                    id: ifsc_code
                    hint_text: "IFSC Code"
                    mode: "rectangle"
                    multiline: False

                MDTextField:
                    id: account_type
                    hint_text: "Account Type"
                    mode: "rectangle"
                    multiline: False

                Widget:
                    size_hint_y: None
                    height: '5dp'    

                MDRaisedButton:
                    #id: edit_save_button
                    text: "Submit"
                    size_hint: None, None
                    size: dp(150), dp(50)
                    pos_hint: {'center_x': 0.5}
                    on_release: root.add_account()
                      
'''
Builder.load_string(KV_STRING)


class AddAccountScreen(Screen):
    def go_back(self):
        self.manager.current = 'dashboard'

    def show_popup(self, text):
        dialog = MDDialog(
            title="Alert",
            text=text,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda *args: dialog.dismiss()
                    # pos_hint = {"center_x": 0.5, "center_y": 0.5}
                )
            ]
        )
        dialog.open()

    def add_account(self):
        acc_scr = self.manager.get_screen('addaccount')
        # Retrieve data from text fields
        account_holder_name = acc_scr.ids.account_holder_name.text
        account_number = acc_scr.ids.account_number.text
        confirm_account_number = acc_scr.ids.confirm_account_number.text
        bank_name = acc_scr.ids.bank_name.text
        branch_name = acc_scr.ids.branch_name.text
        ifsc_code = acc_scr.ids.ifsc_code.text
        account_type = acc_scr.ids.account_type.text

        # Check if the account numbers match
        if account_number != confirm_account_number:
            print("Error: Account numbers do not match.")
            Snackbar(
                text="Error: Account number didn't match.").open()
            # You might want to handle this case in your UI, e.g., show an error message.
            return

        # Retrieve phone number from user_data.json
        phone = JsonStore('user_data.json').get('user')['value']["phone"]

        try:
            # Replace "your-project-id" with your actual Firebase project ID
            database_url = "https://e-wallet-realtime-database-default-rtdb.asia-southeast1.firebasedatabase.app"

            # Reference to the 'accounts' subcollection under the user's document
            accounts_endpoint = f"{database_url}/account_details/{phone}/accounts.json"

            # Make a POST request to add a new document to the 'accounts' subcollection
            response = requests.post(accounts_endpoint, json={
                'account_holder_name': account_holder_name,
                'account_number': account_number,
                'bank_name': bank_name,
                'branch_name': branch_name,
                'ifsc_code': ifsc_code,
                'account_type': account_type
            })

            # Check if the new document was added successfully (status code 200)
            if response.status_code == 200:
                print("Account details added successfully.")
                self.show_popup("Account added successfully.")
                self.manager.current = 'dashboard'
            else:
                print(f"Failed to add account details. Status code: {response.status_code}")
                Snackbar(
                    text=f"Failed to add account details. Status code: {response.status_code}").open()

        except Exception as e:
            print(f"Error adding account details: {e}")
            Snackbar(
                text=f"Error adding account details: {e}").open()