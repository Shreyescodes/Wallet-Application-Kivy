import sqlite3
import anvil
import requests
from anvil.tables import app_tables
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.label import MDLabel
from landing import LandingScreen
from signup import SignUpScreen
from signin import SignInScreen
from dashboard import DashBoardScreen
from viewprofile import Profile
from editprofile import EditUser
from topup import Topup
from withdraw import WithdrawScreen
from transfer import TransferScreen
from addAccount import AddAccountScreen
from transaction import Transaction
from addContact import AddContactScreen
from paysetting import PaysettingScreen
from navbar import NavbarScreen
from accmanage import AccmanageScreen
from settings import SettingsScreen
from help import HelpScreen
from contactus import ContactUsScreen
from complaint import ComplaintScreen
from addPhone import AddPhoneScreen
from Wallet import AddMoneyScreen
from addPhone import UserDetailsScreen
Builder.load_string(
    """
<ScreenManagement>:
    LandingScreen:
        name: 'landing'
        manager: root
        
    SignUpScreen:
        name: 'signup'
        manager: root  
        
    SignInScreen:
        name: 'signin'
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

    SettingsScreen:
        name: 'settings'
        manager: root   

    AccmanageScreen:
        name: 'accmanage'
        manager: root    

    ContactUsScreen:
        name: 'contactus'
        manager: root    
    
    AddAccountScreen:
        name:'addaccount'
        manager: root

    AddContactScreen:
        name:'addcontact'
        manager: root   

    ComplaintScreen:
        name:'complaint'
        manager: root    

    AddPhoneScreen:
        name:'addphone'
        manager: root   

    PaysettingScreen:
        name:'paysetting'
        manager: root         
        
    NavbarScreen:
        name:'navbar'
        manager: root   
        
    HelpScreen:
        name:'help'
        manager: root      
    
    Transaction:
        name: 'transaction'
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
    
    AddMoneyScreen:
        name:'Wallet'
        manager: root
         
    UserDetailsScreen:
        name:"user_details" 
        manager:root                   
"""
)


class ScreenManagement(ScreenManager):
    current_user_data = None  # Class attribute to store the current user data

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect_to_server()

    def connect_to_server(self):
        if self.is_internet_connected():
            # If internet is connected, connect to the Anvil server
            self.anvil_server_connected = True
            self.client = anvil.server.connect("server_QVP7TBTIZPTLZZTXO5LN7GBD-2QQVRBJQQ5M7D6YM")
        else:
            # If no internet, use local database or show a popup
            self.anvil_server_connected = False
            toast("no internet connection", duration=3)
            # self.show_no_internet_popup()
            # Connect to local database (replace this with your local database code)

    def is_internet_connected(self):
        try:
            # Try to make a simple HTTP request to a known server (e.g., Anvil's server)
            response = requests.get("https://anvil.works")
            return response.status_code == 200
        except requests.ConnectionError:
            return False

    # checking users login status
    def check_login_status(self):
        store = JsonStore('user_data.json')
        if 'user' in store:
            ScreenManagement.current_user_data = store.get('user')['value']
            self.current = 'dashboard'
            self.get_username()
            self.fetch_and_update_navbar()
            self.fetch_and_update_complaint()
            self.show_balance()
        else:
            self.current = 'landing'

    def logout(self):
        # Remove the stored user data when logging out
        store = JsonStore('user_data.json')
        if 'user' in store:
            del store['user']

        try:
            store.clear()
        except Exception as e:
            print(f"Error deleting JSON file: {e}")

        self.current = 'signin'

    def get_username(self):
        store = JsonStore('user_data.json')
        return store.get('user')['value']["username"]

    def nav_navbar(self):
        self.current = 'navbar'

    def fetch_and_update_navbar(self):
        store = JsonStore('user_data.json').get('user')['value']
        # Update labels in NavbarScreen
        navbar_screen = self.get_screen('navbar')
        navbar_screen.ids.username_label.text = store["username"]
        navbar_screen.ids.email_label.text = store["email"]
        navbar_screen.ids.contact_label.text = str(store["phone"])

    def nav_complaint(self):
        self.current = 'complaint'

    def fetch_and_update_complaint(self):
        store = JsonStore('user_data.json').get('user')['value']
        # Update labels in ComplaintScreen
        complaint_screen = self.get_screen('complaint')
        complaint_screen.ids.email_label.text = store["email"]

    def nav_account(self):
        self.current = 'addaccount'

    def show_balance(self):
        balance_scr = self.get_screen('dashboard')
        # Load user data from the JSON file
        store = JsonStore('user_data.json')

        if 'user' in store:
            # 'user' key found, proceed with retrieving data
            phone = store.get('user')['value']["phone"]
            currency = "INR"
            balance_scr.ids.balance_lbl.text = f"{self.get_total_balance(phone, currency)} INR"
        else:
            # 'user' key not found, show an appropriate message
            balance_scr.ids.balance_lbl.text = "User data not found. Please log in."

    def get_total_balance(self, phone, currency_type):
        try:
            acc_row = app_tables.wallet_users_balance.get(phone=phone, currency_type=currency_type)
            if acc_row:
                return acc_row['balance']
            else:
                return 0
        except Exception as e:
            print(f"Error fetching data from anvil Database: {e}")
            return 0

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

    def nav_settings(self):
        self.current = 'settings'

    def nav_help(self):
        self.current = 'help'

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
        self.current = 'dashboard'

    def nav_contactus(self):
        self.current = 'contactus'

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

    def nav_paysetting(self):
        self.current = 'paysetting'

    def nav_accmanage(self):
        self.current = 'accmanage'

    def Add_Money(self):
        self.current = 'Wallet'


class WalletApp(MDApp):
    def build(self):
        self.scr_mgr = ScreenManagement()
        self.scr_mgr.check_login_status()
        self.createTables()
        return self.scr_mgr

    def createTables(self):
        # Connect to SQLite database (or create it if it doesn't exist)
        conn = sqlite3.connect('wallet_database.db')
        cursor = conn.cursor()

        # Create the wallet_users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS wallet_users (
                phone INTEGER PRIMARY KEY,
                username TEXT,
                email TEXT,
                password TEXT,
                confirm_email BOOLEAN,
                aadhar_number INTEGER,
                pan TEXT,
                address TEXT,
                usertype TEXT,
                banned BOOLEAN,
                balance_limit INTEGER,
                daily_limit INTEGER,
                last_login DATE
            )
        ''')

        # Create the wallet_users_account table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS wallet_users_account (
                phone INTEGER,
                account_number INTEGER,
                account_holder_name TEXT,
                bank_name TEXT,
                branch_name TEXT,
                ifsc_code TEXT,
                account_type TEXT,
                FOREIGN KEY (phone) REFERENCES wallet_users(phone)
            )
        ''')

        # Create the wallet_users_balance table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS wallet_users_balance (
                phone INTEGER,
                currency_type TEXT,
                balance INTEGER,
                PRIMARY KEY (phone, currency_type),
                FOREIGN KEY (phone) REFERENCES wallet_users(phone)
            )
        ''')

        # Create the wallet_users_transaction table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS wallet_users_transaction (
                phone INTEGER,
                date DATETIME,
                fund INTEGER,
                transaction_type TEXT,
                transaction_status TEXT,
                FOREIGN KEY (phone) REFERENCES wallet_users(phone)
            )
        ''')

        # Commit the changes and close the connection
        conn.commit()
        conn.close()


if __name__ == '__main__':
    WalletApp().run()
