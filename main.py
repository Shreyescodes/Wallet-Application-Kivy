from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from login import LoginScreen
from signin import SignInScreen
from signup import SignUpScreen
from edituser import EditUser
from dashboard import DashBoardScreen
from user import Profile
from kivymd.uix.snackbar import Snackbar
import re
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
    """
)


class ScreenManagement(ScreenManager):
    current_user_data = None  # Class attribute to store the current user data

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

            conn.commit()
            conn.close()

    def fetch_and_update_dashboard(self, user_data):
        # Assuming user_data is a tuple containing user information (username, email, balance, etc.)
        gmail, username, password, phone, adhaar, pan, address, _, _ = user_data

        # Update class attribute with current user data
        ScreenManagement.current_user_data = user_data

        # Update labels in DashBoardScreen
        dashboard_screen = self.get_screen('dashboard')
        dashboard_screen.ids.username_label.text = username
        dashboard_screen.ids.email_label.text = gmail

    def profile_view(self):
        # Check if the user is logged in
        if ScreenManagement.current_user_data:
            # Retrieve the current user data
            current_user_data = ScreenManagement.current_user_data

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
        else:
            # Show a message indicating that the user is not logged in
            self.show_popup("Please log in to view the profile.")

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


class WalletApp(MDApp):
    def build(self):
        self.scr_mgr = ScreenManagement()
        return self.scr_mgr

    # edit profile========================
    def edit_profile(self):
        edit_screen = self.scr_mgr.get_screen('edituser')
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
        self.scr_mgr.profile_view()
        # self.scr_mgr.current = 'profile'


if __name__ == '__main__':
    WalletApp().run()
