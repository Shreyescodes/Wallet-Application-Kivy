import self
from datetime import datetime
from kivy.metrics import dp
from kivy.properties import StringProperty, NumericProperty
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.card import MDCard
from kivymd.uix.list import MDList, OneLineListItem
from kivy.uix.boxlayout import BoxLayout
from anvil.tables import app_tables
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineListItem
from kivymd.uix.textfield import MDTextField
from kivymd.uix.toolbar import MDTopAppBar
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from win32pdhquery import Query

KV = '''
<AddPhoneScreen>:
    Screen:
        BoxLayout:
            orientation: 'vertical'

            MDTopAppBar:
                title: root.top_app_bar_title
                elevation: 3
                left_action_items: [['arrow-left', lambda x: root.go_back()]]
                md_bg_color: "#148EFE"
                specific_text_color: "#ffffff"
                pos_hint: {'top': 1}

            ScrollView:
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: dp(120)  # Adjust the height as needed
    
                    MDBoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: dp(80)
    
                        MDIconButton:
                            icon: 'magnify'
                            theme_text_color: 'Custom'
                            text_color: [0, 0, 0, 1]
    
                        MDTextField:
                            id: search_text_card
                            hint_text: 'Enter a Phone number to Pay any person on Gwallet'
                            multiline: False
                            size_hint_x: 0.7
                            radius: [20, 20, 0, 0]
                            padding: dp(0)
                            background_color: 1, 1, 1, 0
                            on_text_validate: root.on_search_text_entered()
                            pos_hint: {"center_y": 0.4}  # Adjust the value to move it down
    
                    Widget:  # Spacer
                        size_hint_y: None
                        height: dp(10)  # Adjust the height as needed
    
                    OneLineListItem:
                        id: search_result_item
                        text: "No result"
                        on_release: root.on_number_click(float(root.ids.search_text_card.text))
                    
                    MDLabel:
                        id: contact_label
                        text:''
                        font_style:"H6"
                        size_hint_y:None
                        height: self.texture_size[1]
                # MDBottomNavigation:
                #     spacing: dp(5)
                # #     text_color_active: get_color_from_hex("F5F5F5")
                #     md_bg_color: (1,1,1,1)
<UserDetailsScreen>:
    BoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: f'Paying to +91 {root.phone_number}'
            elevation: 3
            left_action_items: [['arrow-left', lambda x: root.go_back()]]
            right_action_items: [['phone', lambda x: root.phone_action()], ['dots-vertical', lambda x: root.more_action()]]
            md_bg_color: "#148EFE"
            specific_text_color: "#ffffff"

        ScrollView:
            MDList:
                id: transaction_list_mdlist
                
                        

        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: dp(50)
            
            MDTextField:
                id: another_textfield
                hint_text: "Pay amount"
                mode:'round'
                size_hint: None, None
                size: dp(200), dp(60)
                pos_hint: {'center_x': 0.5}  # Position on top
                opacity: 0  # Initially invisible   
            
                
            BoxLayout:
                orientation: 'horizontal'
                size_hint_y: None
                height: dp(400)
                spacing: dp(10)
                pos_hint: {'center_x': 0.5}
                padding: 10
    
                MDRectangleFlatButton:
                    text: 'Pay'
                    #on_release: root.manager.current = 'pay'
                    size_hint_x: None
                    width: "50dp"
                    height: "300dp"
                    pos_hint: {'center_x': 0.5}   
                    text_color: 1, 1, 1, 1
                    md_bg_color: 0, 193/255, 245/255, 1
    
                MDRectangleFlatButton:
                    text: 'Request'
                    #on_press: root.manager.current = 'request'
                    size_hint_x: None
                    width: "150dp"
                    height: "300dp"
                    size_hint_y: None
                    height: "300dp"
                    pos_hint: {'center_x': 0.5}   
                    text_color: 1, 1, 1, 1
                    md_bg_color: 0, 193/255, 245/255, 1
                    radius: [15]
                    
                    
                MDTextField:
                    hint_text: "Messages..."
                    icon_right: "send"
                    size_hint_y: None
                    height: dp(1)  # Adjust height as needed
                    mode: "fill"
                    fill_mode: True
                    radius: [15, 15, 15, 15]  # Rounded edges
                    padding: dp(5), dp(5)
                    theme_text_color: "Custom"
                    text_color: 0, 0, 0, 1  # Black text color    
                    on_text: root.add_another_textfield(self.text)
                    on_text_validate: root.deduct_and_transfer(self.text)
                    
                 
                    
                    
               
'''

Builder.load_string(KV)

class AddPhoneScreen(Screen):
    top_app_bar_title = "Phone Transfer"

    def go_back(self):
        self.manager.current = 'dashboard'

    def fetch_and_update_addPhone(self):
        store = JsonStore('user_data.json').get('user')['value']
        # Update labels in ComplaintScreen
        addPhone_screen = self.get_screen('addphone')
        addPhone_screen.ids.contact_label.text = store["phone"]
        addPhone_screen.current_user_phone = str(store["phone"])

    def on_top_app_bar_title(self, instance, value):
        app = MDApp.get_running_app()
        try:
            self.top_app_bar.title = value
        except AttributeError:
            print("Error: 'top_app_bar' not found")

    def on_search_text_entered(self):
        number = int(self.ids.search_text_card.text)
        print(number)
        try:
            userdata = app_tables.wallet_users.get(phone=number)
            username = userdata['username']
            print(f'username in SearchField:{username}')
            self.ids.search_result_item.text = username
            return username

        except Exception as e:
            print("no connection")
            print(e)
            return {}

    def on_number_click(self, number):
        phone_number = self.ids.search_text_card.text
        if phone_number:
            username = self.ids.search_result_item.text
            self.manager.current = 'userdetails'
            user_details_screen = self.manager.get_screen('userdetails')
            user_details_screen.username = username
            user_details_screen.phone_number = phone_number
            user_details_screen.current_user_phone = self.current_user_phone
            print(self.current_user_phone)

            # Fetch the user details from the database
            user_data = app_tables.wallet_users.get(phone=number)

            if user_data:
                user_details_screen.current_user_phone = self.current_user_phone
                print(self.current_user_phone)
                user_details_screen.searched_user_phone = str(user_data['phone'])  # Adjust this based on your data structure
                print(f"{user_data['phone']}")
            else:
                print(f"User with phone number {number} not found in the database")

            # # Pass the current user's phone number and the searched user's phone number to the UserDetailsScreen
            # user_details_screen.current_user_phone = str(app_tables.wallet_users.get(phone=number))
            # user_details_screen.searched_user_phone = self.on_search_text_entered()

class UserDetailsScreen(Screen):
    username = ""
    phone_number = StringProperty('')
    current_user_phone = ""
    searched_user_phone = ""
    transaction_list_mdlist = None

    def on_enter(self, sender=None):
        # Convert phone numbers to integers
        global message, color, align
        current_user_phone = int(self.current_user_phone)
        print(f'current_user_phone:{self.current_user_phone}')
        searched_user_phone = int(self.searched_user_phone)
        print(f'searched_user_phone:{self.searched_user_phone}')

        # Get the transaction data between current and searched users
        user_data_1 = app_tables.wallet_users_transaction.search(
            phone=searched_user_phone,
            receiver_phone=current_user_phone,
            transaction_type='debit'
        )
        user_data_2 = app_tables.wallet_users_transaction.search(
            phone=current_user_phone,
            receiver_phone=searched_user_phone,
            transaction_type='debit'

        )
        print(user_data_2)
        print(user_data_1)
        # Convert LiveObjectProxy results to lists
        user_data_1_list = list(user_data_1)
        user_data_2_list = list(user_data_2)

        # Combine the lists
        user_data = user_data_1_list + user_data_2_list
        print(user_data)

        self.ids.transaction_list_mdlist.clear_widgets()

        # Iterate over the transaction data and display as chat-like messages
        for transaction in user_data:
            sender = transaction['phone']
            receiver = transaction['receiver_phone']
            fund = transaction['fund']
            date = transaction['date']

            # Extract only the date part from the datetime object
            date_str = date.strftime('%Y-%m-%d')  # Format the date as desired

            # Retrieve the username associated with the searched user phone
            searched_user_data = app_tables.wallet_users.get(phone=searched_user_phone)
            searched_username = searched_user_data['username'] if searched_user_data else 'Unknown User'

            date_label = Label(
                text=date_str,
                font_size=18,
                color=(0.5, 0.5, 0.5, 1),  # Black color for date
                size_hint_y=None,
                height=dp(40),
                halign='center'  # Center align the date label
            )
            self.ids.transaction_list_mdlist.add_widget(date_label)

            # Initialize message and color variables
            message = ""
            color = (0, 0, 0, 1)  # Default color


            # Determine the direction of the message based on sender and receiver
            if sender == current_user_phone:
                message = f"Payment to {searched_username}\n" \
                          f"₹{fund}"
                color = (0, 0, 0, 1)  # Blue for outgoing messages
                align = 'right'
            elif sender == searched_user_phone:
                message = f"Payment to you\n" \
                          f"₹{fund}"
                color = (0, 0, 0, 1)  # Green for incoming messages
                align = 'left'


            # Create label for transaction message
            message_label = Label(
                text=message,
                font_size=24,
                color=color,
                size_hint_y=None,
                height=dp(60),
                halign=align
            )
            self.ids.transaction_list_mdlist.add_widget(message_label)

    def add_another_textfield(self, text):
        if text:
            self.ids.another_textfield.text = text
            self.ids.another_textfield.opacity = 1
        else:
            self.ids.another_textfield.opacity = 0


    def deduct_and_transfer(self, amount):
        # Convert amount to integer or float
        amount = int(amount)

        # Fetch current user's data from wallet_users_balance
        current_user_data = app_tables.wallet_users_balance.search(
            phone=int(self.current_user_phone),
            currency_type='INR'  # Add currency_type condition
        )
        if len(current_user_data) == 1:
            current_user_data = current_user_data[0]
            # Deduct amount from current user's balance
            current_user_data['balance'] -= amount
            current_user_data.update()
        else:
            print("Error: More than one row matched for current user")

        app_tables.wallet_users_transaction.add_row(
            reciever_phone=int(self.searched_user_phone),
            phone=int(self.current_user_phone),
            fund=amount,
            #date=date,
            transaction_type="Debit"
        )

        # Fetch searched user's data from wallet_users_balance
        searched_user_data = app_tables.wallet_users_balance.search(
            phone=int(self.searched_user_phone),
            currency_type='INR'  # Add currency_type condition
        )
        if len(searched_user_data) == 1:
            searched_user_data = searched_user_data[0]
            # Add amount to searched user's balance
            searched_user_data['balance'] += amount
            searched_user_data.update()
        else:
            print("Error: More than one row matched for searched user")

        app_tables.wallet_users_transaction.add_row(
            reciever_phone=int(self.current_user_phone),
            phone=int(self.searched_user_phone),
            fund=amount,
            #date=date,
            transaction_type="Credit"
        )


    def go_back(self):
        self.manager.current = 'addphone'

    def fetch_and_display_transaction_history(self):

        # Get the phone number from the JSON file
        phone = JsonStore('user_data.json').get('user')['value']['phone']

        # Query the 'transactions' table to fetch the transaction history
        transactions1 = app_tables.wallet_users_transaction.search(phone=self.current_user_phone)
        transactions2 = app_tables.wallet_users_transaction.search(receiver_phone=self.searched_user_phone)

        transactions = [
            {"sender": "searched_user_phone", "fund": "transactions2['fund']"},
            {"sender": "current_user_phone", "fund": "transactions1['fund']"},
            # Add more transactions here
        ]

        # Clear existing transaction history
        self.ids.transaction_list_mdlist.clear_widgets()

        if not transactions:
            # If no transactions found, display a message
            item = MDLabel(text="No transactions found", font_size=20, size_hint_y=None, height=dp(50))
            self.ids.transaction_list_mdlist.add_widget(item)
        else:
            for transaction in transactions:
                # Create a label to display transaction details
                transaction_label = MDLabel(
                    text=transaction["fund"],
                    font_size=16,
                    size_hint_y=None,
                    height=dp(150)
                )

                # Determine the side of the screen to place the transaction label
                if transaction["sender"] == "searched_user_phone":
                    layout = MDBoxLayout(orientation='horizontal', padding=10, spacing=10, size_hint=(1, None))
                    layout.add_widget(MDLabel(text=transaction["fund"], theme_text_color="Secondary"))
                    layout.add_widget(Widget())  # Spacer
                    self.ids.transaction_list_mdlist.add_widget(layout)
                elif transaction["sender"] == "current_user_phone":
                    layout = MDBoxLayout(orientation='horizontal', padding=10, spacing=10, size_hint=(1, None),
                                         pos_hint={'right': 1})
                    layout.add_widget(Widget())  # Spacer
                    layout.add_widget(MDLabel(text=transaction["fund"]))
                    self.ids.transaction_list_mdlist.add_widget(layout)
    def build(self):
        # Initialize screen manager
        screen_manager = ScreenManager()

        # Add screens to the screen manager
        screen_manager.add_widget(AddPhoneScreen(name='add_phone'))
        screen_manager.add_widget(UserDetailsScreen(name='user_details'))
        return screen_manager

# if __name__ == '__main__':
#     WalletApp().run()








