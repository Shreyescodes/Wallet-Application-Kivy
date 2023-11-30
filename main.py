from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem
from login import LoginScreen
from signin import SignInScreen
from signup import SignUpScreen
from edituser import EditUser
from dashboard import DashBoardScreen
from user import Profile
from transaction import Transaction
from addAccount import AddAccountScreen
from kivymd.uix.snackbar import Snackbar
import sqlite3
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

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
    """
)


class ScreenManagement(ScreenManager):
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
            sql = ('INSERT INTO login(gmail,username,password,phone,adhaar,pan,address) VALUES (?,?,?,?,?,?,?);')
            mydata = (gmail, username, password, phone_no, aadhar_card, pan_card, address)
            cursor.execute(sql, mydata)
            # cheking for duplicate values
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

                self.fetch_and_update_dashboard(row)
                # Show popup for successful login
                self.show_popup("Login Successful")
                self.current = 'dashboard'
            store = JsonStore('user_data.json')
            store.put('user', value=row)
            conn.commit()
            conn.close()

    def fetch_and_update_dashboard(self, user_data):
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

    def go_to_transaction(self):
        self.on_start()
        self.current = 'transaction'

    def on_start(self):
        self.get_transaction_history()

    def get_transaction_history(self):
        # Connect to the database
        conn = sqlite3.connect('wallet_app.db')
        cursor = conn.cursor()

        # Execute the query
        cursor.execute('SELECT * FROM transactions')

        # Fetch all the results
        transaction_history = cursor.fetchall()

        # Close the connection
        conn.close()
        trans_screen = self.get_screen('transaction')
        # Clear existing widgets in the MDList
        trans_screen.ids.transaction_list.clear_widgets()
        # Display the transaction history
        for trans in transaction_history:
            transaction_item = f"paid     {trans[2]}₹\n          " \
                               f" {trans[3]}\n" \

            trans_screen.ids.transaction_list.add_widget(OneLineListItem(text=transaction_item))

    def add_account(self):
        acc_scr = self.get_screen('addaccount')
        self.current = 'addaccount'
        # Retrieve data from text fields
        account_holder_name = acc_scr.ids.account_holder_name.text
        account_number = acc_scr.ids.account_number.text
        confirm_account_number = acc_scr.ids.confirm_account_number.text
        bank_name = acc_scr.ids.bank_name.text
        branch_name = acc_scr.ids.branch_name.text
        ifsc_code = acc_scr.ids.ifsc_code.text
        account_type = acc_scr.ids.account_type.text

        # Process the data (you can store it or perform further actions)


class WalletApp(MDApp):
    def build(self):
        self.scr_mgr = ScreenManagement()
        self.scr_mgr.check_login_status()
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
