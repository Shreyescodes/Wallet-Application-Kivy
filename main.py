import json
import threading
from datetime import datetime
from io import BytesIO

import qrcode
from kivy.clock import Clock

from qr_viwer import QRScreen
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineListItem
from login import LoginScreen
from signin import SignInScreen
from signup import SignUpScreen
from edituser import EditUser
from dashboard import DashBoardScreen
from user import Profile
from transaction import Transaction
from addAccount import AddAccountScreen
from topup import Topup
from w2 import WithdrawScreen
from kivymd.uix.snackbar import Snackbar
import sqlite3
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from Transfer_Page import TransferScreen

Builder.load_string(
    """
<ScreenManagement>:
    LoginScreen:
        name: 'login'
        manager: root
    SignInScreen:
        name: 'signin'
        manager: root
    SignUpScreen:
        name: 'signup'
        manager: root
    DashBoardScreen:
        name: 'dashboard'
        manager: root    
    Profile:
        name:'profile'
        manager: root      
    EditUser:
        name: 'edituser'
        manager: root    
    Transaction:
        name: 'transaction'
        manager: root  

    AddAccountScreen:
        name:'addaccount'
        manager: root 
        
    Topup:
        name:'topup'
        manager: root 
     
    WithdrawScreen:
        name: 'withdraw'
        manager: root  
        
    TransferScreen:
        name:'transfer'
        manager:root          
        
    QRScreen:
        name:'qr_screen'
        manager: root                    
    """
)


class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)
        self.transition = SlideTransition(duration=0.7)

    current_user_data = None  # Class attribute to store the current user data

    # checking users login status
    def check_login_status(self):
        # Check for stored user data when the app starts
        store = JsonStore('user_data.json')
        if 'user' in store:
            ScreenManagement.current_user_data = store.get('user')['value']
            self.current = 'dashboard'
        else:
            self.current = 'login'

    def dismiss_and_navigate(self):

        self.current = 'signin'  # Navigate to the desired screen

    # signup codes ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def signup(self):
        current_screen = self.current_screen
        gmail = current_screen.ids.gmail.text
        username = current_screen.ids.username.text
        password = current_screen.ids.password.text
        phone_no = current_screen.ids.phone_no.text
        aadhar_card = current_screen.ids.aadhar_card.text
        pan_card = current_screen.ids.pan_card.text
        address = current_screen.ids.address.text

        try:
            # Database Connection
            conn = sqlite3.connect('wallet_app.db')
            cursor = conn.cursor()
            # Inserting data into DataSbase
            sql = 'INSERT INTO login(gmail,username,password,phone,adhaar,pan,address) VALUES (?,?,?,?,?,?,?);'
            mydata = (gmail, username, password, phone_no, aadhar_card, pan_card, address)
            cursor.execute(sql, mydata)
            # checking for duplicate values
            # Check for duplicate usernames and phones
            cursor.execute('''
                SELECT gmail, username, COUNT(*)
                FROM login
                GROUP BY gmail,username
                HAVING COUNT(*) > 1
            ''')

            duplicate_records = cursor.fetchall()
            # navigating to the sign in screen if all requirements are correct=========================================
            if duplicate_records:
                Snackbar(text="Username/Gmail Already exists").open()
                for gmail, username, count in duplicate_records:
                    print(f"Username: {username}, gmail: {gmail} - Count: {count}")
            else:
                print("No duplicate records found.")
                # Show a popup with a message
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
        except Exception as e:
            print(e)
        conn.commit()
        conn.close()

        if (not gmail or not username
                or not password or not phone_no
                or not aadhar_card or not pan_card or not address):
            Snackbar(text="All fields are mandatory. Please fill in all the required fields.").open()
            return

        if not self.is_valid_aadhar(aadhar_card):
            Snackbar(
                text="Invalid Aadhar card number. Aadhar card should be 12 digits long and contain only numeric characters.").open()
            return

        if not self.is_valid_phone(phone_no):
            Snackbar(
                text="Invalid phone number. Phone number should be 10 digits long and start with 6, 7, 8, or 9.").open()
            return

        if not self.is_valid_pan(pan_card):
            Snackbar(
                text="Invalid PAN card number. PAN card should start with 5 characters (A-Z), followed by 4 numbers, and ending with 1 character (A-Z).").open()
            return

        # Add your sign-up logic here
        print("Signing up...")
        print(f"Gmail: {gmail}, Username: {username}, Password: {password}, "
              f"Phone Number: {phone_no}, Aadhar Card: {aadhar_card}, PAN Card: {pan_card}, "
              f"Address: {address}")

    def is_valid_phone(self, phone):
        if len(phone) == 10 and phone[0] in ['6', '7', '8', '9']:
            return True
        return False

    def is_valid_aadhar(self, aadhar):
        if len(aadhar) == 12 and aadhar.isdigit():
            return True
        return False

    def is_valid_pan(self, pan):
        if len(pan) == 10 or len(pan) == 11 and pan[:5].isalpha() and pan[5:9].isdigit() and pan[9:10].isdigit() or pan[
                                                                                                                    9:12].isalpha():
            return True
        return False

    # ...
    # signin++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def sign_in(self, input_text, password):
        # ... (rest of your code)

        if input_text == '' or password == '':
            # Show popup for required fields
            self.show_popup("All Fields are Required")
        else:
            try:
                conn = sqlite3.connect('wallet_app.db')
                cursor = conn.cursor()
            except:
                # Show popup for connection error
                self.show_popup("Something Went Wrong")
                return

            sql = "SELECT * FROM login WHERE (username=? or phone=? or gmail=?) AND password=?"
            data = (input_text, input_text, input_text, password)
            cursor.execute(sql, data)
            row = cursor.fetchone()

            if row is None:
                # Show popup for invalid user
                self.show_popup("Invalid User")
            else:

                # self.fetch_and_update_dashboard(row)
                # Show popup for successful login
                self.show_popup("Login Successful")

                self.current = 'dashboard'
            store = JsonStore('user_data.json')
            store.put('user', value=row)
            phone_number = store.get('user')['value'][3]
            self.show_balance()
            Clock.schedule_once(lambda dt: self.generate_qr(phone_number), 0)
            conn.commit()
            conn.close()

    def fetch_and_update_dashboard(self):
        if ScreenManagement.current_user_data:
            # Retrieve the current user data
            current_user_data = ScreenManagement.current_user_data
        else:
            # If current_user_data is empty, try to load it from the JSON file
            store = JsonStore('user_data.json')
            if 'user' in store:
                current_user_data = store.get('user')['value']
            else:
                # If the JSON file doesn't have user data, show a message or handle it as needed
                Snackbar(text="User data not found. Please log in.").open()
                return

        # Update labels in DashBoardScreen
        dashboard_screen = self.get_screen('dashboard')
        dashboard_screen.ids.username_label.text = current_user_data[1]
        dashboard_screen.ids.email_label.text = current_user_data[0]

    def profile_view(self):
        # Check if the user is logged in
        if ScreenManagement.current_user_data:
            # Retrieve the current user data
            current_user_data = ScreenManagement.current_user_data
        else:
            # If current_user_data is empty, try to load it from the JSON file
            store = JsonStore('user_data.json')
            if 'user' in store:
                current_user_data = store.get('user')['value']
            else:
                # If the JSON file doesn't have user data, show a message or handle it as needed
                Snackbar(text="User data not found. Please log in.").open()
                return

        # Create a new ProfileScreen instance
        profile_screen = self.get_screen('profile')
        print(current_user_data)

        # Update the profile view with the user data
        profile_screen.ids.username_label.text = f"Username: {current_user_data[1]}"  # Assuming username is at index 1
        profile_screen.ids.email_label.text = f"Email: {current_user_data[0]}"  # Assuming email is at index 0
        profile_screen.ids.contact_label.text = f"Mobile No: {current_user_data[3]}"
        profile_screen.ids.aadhaar_label.text = f"Aadhar: {current_user_data[4]}"
        profile_screen.ids.pan_label.text = f"Pan no: {current_user_data[5]}"
        profile_screen.ids.address_label.text = f"Address: {current_user_data[6]}"
        # Navigate to the 'Profile' screen
        self.current = 'profile'

    def logout(self):
        # Remove the stored user data when logging out
        store = JsonStore('user_data.json')
        if 'user' in store:
            del store['user']

        try:
            import os
            os.remove('user_data.json')
        except Exception as e:
            print(f"Error deleting JSON file: {e}")

        self.current = 'signin'

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

    # transcation screen part
    def go_to_transaction(self):
        self.on_start()
        self.current = 'transaction'

    def on_start(self):
        self.get_transaction_history()

    def get_transaction_history(self):
        # Connect to the database
        conn = sqlite3.connect('wallet_app.db')
        cursor = conn.cursor()
        store = JsonStore('user_data.json')
        phone = store.get('user')['value'][3]
        # Execute the query
        cursor.execute('SELECT * FROM transactions  WHERE phone = ?', (phone,))

        # Fetch all the results
        transaction_history = cursor.fetchall()

        # Close the connection
        conn.close()
        trans_screen = self.get_screen('transaction')
        # Clear existing widgets in the MDList
        trans_screen.ids.transaction_list.clear_widgets()
        # Display the transaction history
        for trans in reversed(transaction_history):
            transaction_item = f"paid     {trans[2]}₹\n          " \
                               f" {trans[3]}\n"

            trans_screen.ids.transaction_list.add_widget(OneLineListItem(text=transaction_item))

    # add Account part
    def nav_account(self):
        acc_scr = self.get_screen('addaccount')
        self.current = 'addaccount'

    def add_account(self):
        acc_scr = self.get_screen('addaccount')
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
        with open('user_data.json', 'r') as json_file:
            user_data = json.load(json_file)
            phone_number = user_data.get("user", {}).get("value", [])[3]

        # Connect to the SQLite database
        conn = sqlite3.connect("wallet_app.db")
        cursor = conn.cursor()

        try:
            # Insert into account_details table
            cursor.execute('''
                       INSERT INTO account_details 
                       (account_holder_name, account_number, bank_name, branch_name, ifsc_code, account_type, phone) 
                       VALUES (?, ?, ?, ?, ?, ?, ?)
                   ''', (
                account_holder_name, account_number, bank_name, branch_name, ifsc_code, account_type, phone_number))

            # Commit the changes
            conn.commit()
            print("Account details added successfully.")
            self.show_popup("Account added successfully.")
            self.current = 'dashboard'
        except sqlite3.IntegrityError:
            conn.rollback()
            print("Error: Account number already exists in the database.")
            Snackbar(
                text="Error: Account number already exists in the database.").open()

        # Close the connection
        conn.close()

    # navigation ton top up screen
    def nav_topup(self):
        self.current = 'topup'

    def add_money(self):
        topup_scr = self.get_screen('topup')
        amount = float(topup_scr.ids.amount_field.text)
        bank_name = topup_scr.ids.bank_dropdown.text
        store = JsonStore('user_data.json')
        phone = store.get('user')['value'][3]

        # Check if the amount is within the specified range
        if 500 <= amount <= 100000:
            # Connect to the SQLite database (replace 'wallet_app.db' with your actual database file)
            connection = sqlite3.connect('wallet_app.db')
            cursor = connection.cursor()

            # Get the current date and time
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # update add money table and update the balance
            cursor.execute('SELECT * FROM add_money WHERE bank_name = ?', (bank_name,))
            existing_record = cursor.fetchone()
            if existing_record:
                # Bank name exists, update the record
                # current_currency = existing_record['currency_type']
                currency = existing_record[1]
                current_e_money = existing_record[3]
                current_balance = existing_record[2]

                # Calculate the new values
                new_e_money = current_e_money + amount
                new_balance = current_balance - amount
                cursor.execute("""
                        UPDATE add_money
                        SET e_money = ?, balance = ?
                        WHERE bank_name = ? AND phone_no = ?  
                    """, (new_e_money, new_balance, bank_name, phone))
            else:
                # Bank name doesn't exist, insert a new record
                cursor.execute("""
                            INSERT INTO add_money (wallet_id, currency_type, balance, e_money, phone_no, bank_name)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (2, 'INR', 10000 - amount, amount, phone, bank_name))
            # Insert a new row into the transactions table
            cursor.execute("""
                       INSERT INTO transactions (wallet_id, description, money, date, phone)
                       VALUES (?, ?, ?, ?, ?)
                   """, (1, 'topup', amount, current_datetime, phone))

            # Commit the changes and close the connection
            connection.commit()
            connection.close()

            # Show a success toast
            toast("Money added successfully.")
            self.current = 'dashboard'
            self.show_balance()

            # You can also navigate to another screen or perform other actions if needed
        else:
            # Show an error toast
            toast("Invalid amount. Please enter an amount between 500 and 100000.")

    def nav_withdraw(self):
        self.current = 'withdraw'

    def select_currency(self, currency):
        wdrw_scr = self.get_screen('withdraw')
        wdrw_scr.ids.currency_spinner.text = currency

    def withdraw(self):
        wdrw_scr = self.get_screen('withdraw')
        # self.create_tables_if_not_exist()
        # Get the entered mobile number, amount, and selected currency from your UI components
        entered_mobile = wdrw_scr.ids.mobile_textfield.text
        amount = wdrw_scr.ids.amount_textfield.text
        selected_currency = wdrw_scr.ids.currency_spinner.text

        # Validate inputs
        if not entered_mobile or not amount or not selected_currency:
            self.show_error_popup("Please fill in all fields.")
            return
            # Load user data from the JSON file
        with open("../../Wallet-Mobile-Application/user_data.json", "r") as file:
            user_data = json.load(file)
        # Get the signed-in number from user_data
        # Assuming the mobile number is at index 3
        signed_in_number = user_data.get("user", {}).get("value", [])[3]
        # Check if the entered mobile number matches the signed-in number
        if entered_mobile != signed_in_number:
            self.show_error_popup("Invalid mobile number.")
            return
        # Check if the withdrawal amount is a valid number
        try:
            amount = float(amount)
        except ValueError:
            self.show_error_popup("Invalid amount. Please enter a valid number.")
            return

        # Check if the entered mobile number is present in the withdraw_transfer table
        conn = sqlite3.connect('wallet_app.db')
        cursor = conn.cursor()
        cursor.execute('SELECT wallet_id, e_money, balance FROM add_money WHERE phone_no = ?', (entered_mobile,))
        result = cursor.fetchone()

        if result:
            wallet_id, emoney_value, previous_amount = result

            # Check if the wallet has sufficient funds
            if amount > emoney_value:
                self.show_error_popup("Insufficient funds.")
                conn.close()
                return

            # Withdraw money (subtract the withdrawal amount from emoney)
            new_emoney_value = emoney_value - amount
            new_amount = previous_amount + amount  # Update the amount attribute

            cursor.execute('UPDATE add_money SET e_money = ?, balance = ? WHERE wallet_id = ?',
                           (new_emoney_value, new_amount, wallet_id))
            conn.commit()

            conn.close()

            # Convert the withdrawn amount to the selected currency
            converted_amount = self.convert_to_currency(amount, selected_currency)

            wallet_label = wdrw_scr.ids.wallet_label
            wallet_label.text = f"Wallet Money: ${new_emoney_value}"

            # Show success message with the withdrawn amount in the selected currency
            success_message = f"Withdrawal successful. New emoney value: {new_emoney_value}\nWithdrawn Amount: {converted_amount} {selected_currency}"
            self.show_success_popup(success_message)
            self.show_balance()
        else:
            self.show_error_popup("User not found.")
            conn.close()

        return

    # to update the balance chart
    def show_balance(self):
        balance_scr = self.get_screen('dashboard')

        # Load user data from the JSON file
        store = JsonStore('user_data.json')

        if 'user' in store:
            # 'user' key found, proceed with retrieving data
            phone_no = store.get('user')['value'][3]
            balance_scr.ids.balance_lbl.text = f"{self.get_total_balance(phone_no)} INR"
        else:
            # 'user' key not found, show an appropriate message
            balance_scr.ids.balance_lbl.text = "User data not found. Please log in."

    def get_total_balance(self, phone_no):
        # Connect to the SQLite database
        connection = sqlite3.connect('wallet_app.db')
        cursor = connection.cursor()

        try:
            # Fetch e_money for a specific phone_no and calculate total balance
            cursor.execute("SELECT e_money FROM add_money WHERE phone_no = ?", (phone_no,))
            result = cursor.fetchall()

            if result:
                total_balance = sum(e_money for e_money, in result)
                print(f"The total balance for {phone_no} is: {total_balance}")
                return total_balance
            else:
                print(f"No records found for phone number: {phone_no}")
                return 0  # or handle it as needed
        finally:
            # Close the connection in the finally block to ensure it is always closed
            connection.close()

    def convert_to_currency(self, amount, target_currency):
        # Replace this with your actual currency conversion logic or API call
        # This is a simplified example, assuming 1 USD = 75 INR for conversion
        exchange_rate_inr_to_usd = 0.013  # Replace with actual exchange rates
        exchange_rate_inr_to_pound = 0.0098  # Replace with actual exchange rates
        exchange_rate_inr_to_euros = 0.0111  # Replace with actual exchange rates

        if target_currency == 'USD':
            return amount * exchange_rate_inr_to_usd
        elif target_currency == 'GBP':
            return amount * exchange_rate_inr_to_pound
        elif target_currency == 'EUR':
            return amount * exchange_rate_inr_to_euros
        else:
            return amount  # Default to the original amount if the target currency is not supported

        # ... (other methods and class definitions)

    def show_error_popup(self, message):
        content = BoxLayout(orientation='vertical', spacing='10dp')
        content.add_widget(MDLabel(text=message, halign='center'))

        ok_button = Button(text='OK', size_hint=(None, None), size=('150dp', '50dp'))
        ok_button.bind(on_press=lambda *args: popup.dismiss())
        content.add_widget(ok_button)

        popup = Popup(
            title='Error',
            content=content,
            size_hint=(None, None),
            size=('300dp', '200dp'),
            auto_dismiss=True
        )
        popup.open()

    def show_success_popup(self, message):
        content = BoxLayout(orientation='vertical', spacing='10dp')
        content.add_widget(MDLabel(text=message, halign='center'))

        ok_button = Button(text='OK', size_hint=(None, None), size=('150dp', '50dp'))
        ok_button.bind(on_press=lambda *args: popup.dismiss())
        content.add_widget(ok_button)

        popup = Popup(
            title='Success',
            content=content,
            size_hint=(None, None),
            size=('300dp', '200dp'),
            auto_dismiss=True
        )
        popup.open()

    def nav_transfer(self):
        self.current = 'transfer'

    def generate_qr(self,phone_number):
        # Example stored phone number


        # threading.Thread(target=self.generate_qr, args=(phone_number,)).start()
        # Generate QR code
        qr = qrcode.QRCode(
            version=3,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=15,
            border=4,
        )
        qr.add_data(f"Phone Number: {phone_number}")
        qr.make(fit=True)

        qr_img = qr.make_image(fill_color="black", back_color="white")

        # Convert PIL Image to BytesIO
        # img_buffer = BytesIO()
        img_buffer = BytesIO()
        qr_img.save(img_buffer, format="PNG", quality=95)

        img_buffer.seek(0)
        with open("qr_code.png", "wb") as f:
            f.write(img_buffer.read())
class WalletApp(MDApp):
    def build(self):
        self.scr_mgr = ScreenManagement()
        self.scr_mgr.check_login_status()
        self.scr_mgr.fetch_and_update_dashboard()
        self.scr_mgr.show_balance()
        return self.scr_mgr

    # edit profile========================
    def edit_profile(self):
        edit_screen = self.scr_mgr.get_screen('edituser')

        if ScreenManagement.current_user_data is None:
            # Load user data from user_data.json
            store = JsonStore('user_data.json')
            if 'user' in store:
                ScreenManagement.current_user_data = store.get('user')['value']
            else:
                print("User data not found in user_data.json. Cannot edit profile.")
                return

        edit_screen.ids.username.text = ScreenManagement.current_user_data[1]
        edit_screen.ids.email.text = ScreenManagement.current_user_data[0]
        edit_screen.ids.phone.text = ScreenManagement.current_user_data[3]
        edit_screen.ids.password.text = ScreenManagement.current_user_data[2]
        edit_screen.ids.aadhaar.text = ScreenManagement.current_user_data[4]
        edit_screen.ids.pan.text = ScreenManagement.current_user_data[5]
        edit_screen.ids.address.text = ScreenManagement.current_user_data[6]
        self.scr_mgr.current = 'edituser'

        print(ScreenManagement.current_user_data)

    def save_edit(self):
        conn = sqlite3.connect('wallet_app.db')
        cursor = conn.cursor()

        edit_scr = self.scr_mgr.get_screen('edituser')
        phone = edit_scr.ids.phone.text
        username = edit_scr.ids.username.text
        gmail = edit_scr.ids.email.text
        password = edit_scr.ids.password.text
        adhaar = edit_scr.ids.aadhaar.text
        pan = edit_scr.ids.pan.text
        address = edit_scr.ids.address.text

        update_sql = ('''
                UPDATE login
                SET username = ?, gmail = ?, password = ?, adhaar = ?, pan = ?, address = ?
                WHERE phone = ?;
            ''')

        # Execute the SQL statement with the updated values
        cursor.execute(update_sql, (username, gmail, password, adhaar, pan, address, phone))

        # Commit the changes
        conn.commit()

        # Close the connection (assuming 'conn' is the connection object)
        conn.close()
        # self.scr_mgr.profile_view()
        # self.scr_mgr.sign_in(username,password)
        # self.scr_mgr.current = 'profile'
        # self.show_popup("updated successfully now login ")
        # self.scr_mgr.logout()
        self.show_update_success_popup()

    def show_update_success_popup(self):
        dialog = MDDialog(
            title="Update Success",
            text="Your profile has been updated successfully. Please log in again.",
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda *args: (dialog.dismiss(), self.scr_mgr.logout())
                )
            ]
        )
        dialog.open()


if __name__ == '__main__':
    WalletApp().run()
