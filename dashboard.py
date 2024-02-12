import base64
import io
from kivy.uix.image import Image
import qrcode
import requests
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import Screen
from kivy.uix.image import AsyncImage
from kivymd.uix.button import MDIconButton
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from anvil.tables import app_tables

navigation_helper = """
<DashBoardScreen>:
    Screen:
        MDNavigationLayout:
            MDScreenManager:
                MDScreen:
                    MDTopAppBar:
                        title: ""
                        elevation: 1
                        pos_hint: {"top": 1}
                        md_bg_color: "#ffffff"
                        specific_text_color: "#000000"

                        # Adding a logo to the left of the text
                        BoxLayout:
                            spacing: dp(10)
                            MDIconButton:
                                icon: 'menu'
                                on_release: root.nav_navbar()
                                pos_hint: {'center_y': 0.5}

                            Image:
                                source: 'images/2.png'  # Replace with the actual path to your logo
                                size_hint: None, None
                                size: dp(30), dp(28)
                                pos_hint: {'center_y': 0.5}

                            MDLabel:
                                text: "Welcome to G-wallet"
                                #{}".format(root.get_username()) 
                                font_size: '20sp'
                                bold: True
                                pos_hint: {'center_y': 0.5, 'center_x': 0.5}




                    #Main page

                    BoxLayout:
                        orientation: 'vertical'
                        spacing:dp(20)
                        padding: dp(10)
                        pos_hint:{'center_y':.37}

                        Image:
                            source: 'images/signin.jpg'  # Replace with the actual path to your image
                            allow_stretch: True
                            keep_ratio: False
                            size_hint_y: None
                            height: dp(200)


                        GridLayout:
                            #spacing:dp(100)
                            #padding:dp(5)
                            cols: 4
                            spacing:dp(20)
                            rows:4



                            # Icon and label for qrcode-scan
                            BoxLayout:

                                spacing: dp(10)
                                orientation: 'vertical'
                                size_hint_y: None
                                height: self.minimum_height
                                width:20

                                MDIconButton:
                                    icon: 'qrcode-scan'
                                    on_release: root.generate_qr_code()# Replace with your actual function
                                    pos_hint: {'center_x': 0.5}
                                    theme_text_color: 'Custom'
                                    text_color: 0.117, 0.459, 0.725, 1 

                                MDLabel:
                                    text: 'Scan Any QR code'
                                    bold: True
                                    halign: 'center'
                                    font_size: '12sp'

                            BoxLayout:
                                spacing: dp(10)
                                orientation: 'vertical'
                                size_hint_y: None
                                height: self.minimum_height
                                width:20


                                MDIconButton:
                                    icon: 'bank-transfer-in' 
                                    on_release: root.nav_transfer()
                                    pos_hint: {'center_x': 0.5}
                                    theme_text_color: 'Custom'
                                    text_color: 0.117, 0.459, 0.725, 1 

                                MDLabel:
                                    text: 'Transfer'
                                    bold: True
                                    halign: 'center'
                                    font_size: '12sp'

                            BoxLayout:
                                spacing: dp(10)
                                orientation: 'vertical'
                                size_hint_y: None
                                height: self.minimum_height
                                width:20

                                MDIconButton:
                                    icon: 'bank-transfer-out'
                                    on_release: root.nav_withdraw()
                                    pos_hint: {'center_x': 0.5}
                                    theme_text_color: 'Custom'
                                    text_color: 0.117, 0.459, 0.725, 1 

                                MDLabel:
                                    text: 'Withdraw'
                                    bold: True
                                    halign: 'center'
                                    font_size: '12sp'

                            # Icon and label for Transfer


                            # Icon and label for Add Money
                            BoxLayout:
                                spacing: dp(10)
                                orientation: 'vertical'
                                size_hint_y: None
                                height: self.minimum_height
                                width:20

                                MDIconButton:
                                    icon: 'phone'
                                    on_release: root.nav_addPhone()
                                    pos_hint: {'center_x': 0.5}
                                    theme_text_color: 'Custom'
                                    text_color: 0.117, 0.459, 0.725, 1 

                                MDLabel:
                                    text: 'Pay Phone Number'
                                    bold: True
                                    halign: 'center'
                                    font_size: '12sp'   

                            # Icon and label for add contacts        
                            BoxLayout:

                                spacing: dp(10)
                                orientation: 'vertical'
                                size_hint_y: None
                                height: self.minimum_height

                                MDIconButton:
                                    icon: 'contacts'
                                    pos_hint: {'center_x': 0.5}
                                    on_release: root.nav_addContact()
                                    padding: dp(20)
                                    theme_text_color: 'Custom'
                                    text_color: 0.117, 0.459, 0.725, 1 

                                MDLabel:
                                    text: 'Pay Contacts'
                                    bold: True
                                    halign: 'center'
                                    font_size: '12sp'

                            # Icon and label for add phone number
                            BoxLayout:
                                spacing: dp(10)
                                orientation: 'vertical'
                                size_hint_y: None
                                height: self.minimum_height
                                width: 20

                                MDIconButton:
                                    icon: 'wallet'
                                    on_release: root.Add_Money()
                                    pos_hint: {'center_x': 0.5}
                                    theme_text_color: 'Custom'
                                    text_color: 0.117, 0.459, 0.725, 1 

                                MDLabel:
                                    id: balance_lbl
                                    text: 'Wallet Balance'
                                    bold: True
                                    halign: 'center'
                                    font_size: '12sp'        

                            # Icon and label for transaction history        
                            BoxLayout:

                                spacing: dp(10)
                                orientation: 'vertical'
                                size_hint_y: None
                                height: self.minimum_height

                                MDIconButton:
                                    icon: 'history'
                                    pos_hint: {'center_x': 0.5}
                                    on_release:root.go_to_transaction()
                                    padding: dp(20)
                                    theme_text_color: 'Custom'
                                    text_color: 0.117, 0.459, 0.725, 1 

                                MDLabel:
                                    text: 'Transaction History'
                                    bold: True
                                    halign: 'center'
                                    font_size: '12sp'

                            # Icon and label for check balance
                            BoxLayout:

                                spacing: dp(10)
                                orientation: 'vertical'
                                size_hint_y: None
                                height: self.minimum_height

                                BoxLayout:
                                    orientation: "vertical"
                                    padding: 5
                                    pos_hint:{'center_x':0.44}

                                MDCard:
                                    radius: [1, 1, 1, 1]
                                    orientation: 'vertical'
                                    size_hint: 1, 0.4
                                    height: self.minimum_height
                                    md_bg_color: 0.9, 0.9, 0.9, 1

                                    BoxLayout:
                                        padding: "20dp"
                                        orientation: 'horizontal'
                                        spacing: "5dp"



                                    MDIconButton:
                                        id: options_button
                                        icon: 'currency-inr'
                                        pos_hint: {'center_x': 0.5}
                                        on_release: root.show_currency_options(self)
                                        padding: dp(20)
                                        theme_text_color: 'Custom'
                                        text_color: 0.117, 0.459, 0.725, 1 


                                        #md_bg_color: 0.7, 0.7, 0.7, 1  # Blue background color
                                        #text_color: 0, 0, 0, 1  # White text color    

                                MDLabel:
                                    id: balance_lbl
                                    text: 'Check Balance'
                                    bold: True
                                    halign: 'center'
                                    font_size: '12sp'   #        

            MDNavigationDrawer:
                id: nav_drawer
                radius: (0, 10, 10, 0)

                ContentNavigationDrawer:


                    BoxLayout:
                        size: root.width, root.height
                        spacing: '12dp'
                        padding: '8dp'
                        orientation: "vertical"
                        pos_hint:{'top':1}

                        MDLabel:
                            id: username_label
                            text:''
                            font_style:"Subtitle1"
                            size_hint_y:None
                            height: self.texture_size[1]


                        MDLabel:
                            id: email_label
                            text:''
                            font_style:"Caption" 
                            size_hint_y:None
                            height: self.texture_size[1]

                        MDLabel:
                            id: contact_label  
                            text: ''
                            font_style: "Caption" 
                            size_hint_y: None
                            height: self.texture_size[1]    


                        BoxLayout: 
                            size_hint_y: None
                            height: dp(500)
                            pos_hint: {'center_x': 0.45, 'y': 230}        

                            BoxLayout:
                                orientation: "vertical"
                                size_hint_y: None
                                height: self.minimum_height
                                spacing: '4dp'

                                OneLineIconListItem:
                                    text: "Your QR Code"
                                    on_release: root.generate_qr_code()
                                    IconLeftWidget:
                                        icon: "qrcode-scan"
                                        theme_text_color: 'Custom'
                                        text_color: get_color_from_hex("#3489eb")  
                                OneLineIconListItem:
                                    text: "Auto Topup"
                                    IconLeftWidget:
                                        icon: "autorenew" 
                                        theme_text_color: 'Custom'
                                        text_color: get_color_from_hex("#3489eb") 
                                OneLineIconListItem:
                                    text: "Settings"
                                    IconLeftWidget:
                                        icon: "cog-outline"
                                        theme_text_color: 'Custom'
                                        text_color: get_color_from_hex("#3489eb")                      
                                OneLineIconListItem:
                                    text: "Profile"
                                    on_release: root.profile_view()
                                    IconLeftWidget:
                                        icon: "face-man-profile" 
                                        theme_text_color: 'Custom'
                                        text_color: get_color_from_hex("#3489eb")
                                OneLineIconListItem:
                                    text: "Add Bank Account"
                                    on_release: root.manager.nav_account()
                                    IconLeftWidget:
                                        icon: "bank"
                                        theme_text_color: 'Custom'
                                        text_color: get_color_from_hex("#3489eb")
                                OneLineIconListItem:
                                    text: "Get Help"
                                    IconLeftWidget:
                                        icon: "help-circle"
                                        theme_text_color: 'Custom'
                                        text_color: get_color_from_hex("#3489eb")
                                OneLineIconListItem:
                                    text: "Raise a Complaint"
                                    IconLeftWidget:
                                        icon: "alert"  
                                        theme_text_color: 'Custom'
                                        text_color: get_color_from_hex("#3489eb")        
                                OneLineIconListItem:
                                    text: "Log-out"
                                    on_release: root.manager.logout()
                                    IconLeftWidget:
                                        icon: "logout"  
                                        theme_text_color: 'Custom'
                                        text_color: get_color_from_hex("#3489eb")     

"""
Builder.load_string(navigation_helper)


class BottomAppBar(FloatLayout):
    pass


class ContentNavigationDrawer(MDBoxLayout):
    pass


class DashBoardScreen(Screen):
    def get_username(self):
        store = JsonStore('user_data.json').get('user')['value']
        return store["username"]

    def nav_addPhone(self):
        self.manager.current = 'addphone'

    def profile_view(self):
        store = JsonStore('user_data.json').get('user')['value']
        username = store["username"]
        gmail = store["gmail"]
        phone = store["phone"]
        aadhaar = store["Aadhaar"]
        address = store["address"]
        pan = store["pan"]
        profile_screen = self.manager.get_screen('profile')
        profile_screen.ids.username_label.text = f"Username:{username}"  # Assuming username is at index 1
        profile_screen.ids.email_label.text = f"Email:{gmail}"  # Assuming email is at index 0
        profile_screen.ids.contact_label.text = f"Mobile No:{phone}"
        profile_screen.ids.aadhaar_label.text = f"Aadhar:{aadhaar}"
        profile_screen.ids.pan_label.text = f"Pan no:{pan}"
        profile_screen.ids.address_label.text = f"Address:{address}"
        # Navigate to the 'Profile' screen
        self.manager.current = 'profile'

    def nav_topup(self):
        phone = JsonStore('user_data.json').get('user')['value']["phone"]
        account_details = self.account_details_exist(phone)
        if account_details:
            self.manager.current = 'topup'

        else:
            self.show_add_account_dialog()

    def account_details_exist(self, phone):
        try:
            return app_tables.wallet_users_account.search(phone=phone)  # Returns a list of accounts
        except Exception as e:
            print(f"Error fetching accounts: {e}")
            return False

    def nav_withdraw(self):
        phone = JsonStore('user_data.json').get('user')['value']["phone"]
        account_details = self.account_details_exist(phone)
        if account_details:
            self.manager.current = 'withdraw'

        else:
            self.show_add_account_dialog()

    def nav_transfer(self):
        phone = JsonStore('user_data.json').get('user')['value']["phone"]
        account_details = self.account_details_exist(phone)
        if account_details:
            self.manager.current = 'transfer'

        else:
            self.show_add_account_dialog()

    def show_add_account_dialog(self):
        dialog = MDDialog(
            title="Bank Account Not Found",
            text="You don't have a bank account associated with your phone number. "
                 "Would you like to add a bank account?",
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    on_release=lambda *args: (dialog.dismiss(), setattr(self.manager, 'current', 'dashboard'))),
                MDFlatButton(
                    text="OK",
                    on_release=lambda *args:
                    (dialog.dismiss(), setattr(self.manager, 'current', 'addaccount'))),
            ],
        )
        dialog.open()

    def go_to_transaction(self):
        self.on_start()
        self.manager.current = 'transaction'

    def on_start(self):
        self.get_transaction_history()

    def get_transaction_history(self):
        try:
            # Get the phone number from the JSON file
            phone = JsonStore('user_data.json').get('user')['value']['phone']

            # Query the 'transactions' table to fetch the transaction history
            transactions = app_tables.wallet_users_transaction.search(phone=phone)
            trans_screen = self.manager.get_screen('transaction')
            # Clear existing widgets in the MDList
            trans_screen.ids.transaction_list.clear_widgets()

            # Display the transaction history in LIFO order
            for transaction in sorted(transactions, key=lambda x: x['date'], reverse=True):
                transaction_item = f"{transaction['money']}₹\n" \
                                   f"{transaction['transaction_type']}\n"

                trans_screen.ids.transaction_list.add_widget(OneLineListItem(text=transaction_item))

        except Exception as e:
            print(f"Error getting transaction history: {e}")

    menu = None  # Add this line to declare the menu attribute
    options_button_icon_mapping = {
        "INR": "currency-inr",
        "GBP": "currency-gbp",
        "USD": "currency-usd",
        "EUR": "currency-eur"
    }

    def show_currency_options(self, button):
        currency_options = ["INR", "GBP", "USD", "EUR"]
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
        total_balance = self.manager.get_total_balance(phone_no, instance_menu_item)
        # Convert the total balance to the selected currency

        self.ids.balance_lbl.text = f'balance: {total_balance} '
        print(total_balance)
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

    def generate_qr_code(self):
        phone = JsonStore('user_data.json').get('user')['value']["phone"]
        qr_code = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr_code.add_data(phone)
        qr_code.make(fit=True)

        img = qr_code.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        png_data = buffer.getvalue()
        self.show_qr(png_data)

    def show_qr(self, png_data):
        qr_code_popup = Popup(title='Your QR Code', size_hint=(0.8, 0.8))
        qr_code_image = Image()
        qr_code_image.source = 'data:image/png;base64,' + base64.b64encode(png_data).decode('utf-8')
        qr_code_popup.add_widget(qr_code_image)
        qr_code_popup.open()

    def nav_addContact(self):
        self.manager.current = 'addcontact'

    def nav_navbar(self):
        self.manager.current = 'navbar'

    def Add_Money(self):
        self.manager.current = 'Wallet'
