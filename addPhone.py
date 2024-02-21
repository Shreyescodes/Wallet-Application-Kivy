import self
from datetime import datetime, date
from datetime import datetime
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import StringProperty, NumericProperty
from kivy.storage.jsonstore import JsonStore
from kivymd.toast import toast
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel
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
                spacing: dp(5)
                pos_hint: {'center_x': 0.5}
                padding: 10

                MDFillRoundFlatButton:
                    text: 'Pay'
                    #on_release: root.deduct_and_transfer(root.ids.my_text_field.text) 
                    size_hint_x: None
                    width: "150dp"
                    height: "300dp"
                    pos_hint: {'center_x': 0.5}   
                    text_color: "#ffffff"
                    md_bg_color: "#148EFE"

                MDFillRoundFlatButton:
                    text: 'Request'
                    size_hint_x: None
                    width: "150dp"
                    height: "300dp"
                    text_color: 1, 1, 1, 1
                    md_bg_color: "#148EFE"
                    radius: [15]

                # BoxLayout:
                #     orientation: 'horizontal'
                #     size_hint_y: None
                #     height: dp(66)
                #     padding: dp(3)
                #     spacing: dp(5)
                #     MDTextField:
                #         hint_text: "Message..."
                #         mode: "round"
                #         height: dp(1) 
                #         text_color: 0, 0, 0, 1   # Set text color to black
                #         line_color_normal: app.theme_cls.primary_color
                #         
                #             
                #         MDIconButton:
                #             icon: "send"
                #             pos_hint: {'center_y': 0.5}
                #             on_release: root.deduct_and_transfer(self.text)

                CustomMDTextField:
                    id: my_text_field
                    hint_text: "Message..."
                    mode: "round"
                    width: "200dp"
                    height: dp(1)
                    icon_right: "send"
                    padding: dp(5), dp(5)
                    #icon_right_color: app.theme_cls.primary_color
                    line_color_normal: app.theme_cls.primary_color
                    on_text: root.add_another_textfield(self.text)
                    on_text_validate: root.deduct_and_transfer(self.text)


                # MDTextField:
                #     hint_text: "Message..."
                #     icon_right: "send"
                #         on_release: root.deduct_and_transfer(self.text)
                #     height: dp(1)  # Adjust height as needed
                #     mode: "round"
                #     padding: dp(5), dp(5)
                #     text_color: 0, 0, 0, 1  # Black text color    
                #     line_color_normal: app.theme_cls.primary_color
                #     on_text: root.add_another_textfield(self.text)
                #     #on_text_validate: root.deduct_and_transfer(self.text)





'''

Builder.load_string(KV)


class AddPhoneScreen(Screen):
    top_app_bar_title = "Phone Transfer"

    def go_back(self):
        self.manager.current = 'dashboard'
        self.ids.search_text_card.text = ''

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
        number = float(self.ids.search_text_card.text)
        try:
            userdata = app_tables.wallet_users.get(phone=number)
            username = userdata['username']
            print(f'username in SearchField:{username}')
            self.ids.search_result_item.text = username
            return username

        except Exception as e:
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
                user_details_screen.searched_user_phone = str(
                    user_data['phone'])  # Adjust this based on your data structure
                print(f"{user_data['phone']}")
            else:
                print(f"User with phone number {number} not found in the database")

            # # Pass the current user's phone number and the searched user's phone number to the UserDetailsScreen
            # user_details_screen.current_user_phone = str(app_tables.wallet_users.get(phone=number))
            # user_details_screen.searched_user_phone = self.on_search_text_entered()


class CustomMDTextField(MDTextField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.right_icon_callback = lambda: None

    def on_right_icon(self):
        self.right_icon_callback()


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
            transaction_type='Debit'
        )
        user_data_2 = app_tables.wallet_users_transaction.search(
            phone=current_user_phone,
            receiver_phone=searched_user_phone,
            transaction_type='Debit'

        )

        # Convert LiveObjectProxy results to lists
        user_data_1_list = list(user_data_1)
        user_data_2_list = list(user_data_2)

        # Combine the lists
        user_data = user_data_1_list + user_data_2_list
        # Sort the transaction data based on date in descending order
        user_data.sort(key=lambda x: x['date'])

        self.ids.transaction_list_mdlist.clear_widgets()

        # Iterate over the transaction data and display as chat-like messages
        for transaction in user_data:
            sender = transaction['phone']
            receiver = transaction['receiver_phone']
            fund = transaction['fund']
            date = transaction['date']

            # Check if date is not None before formatting
            if date is not None:
                # Extract only the date part from the datetime object
                date_str = date.strftime('%Y-%m-%d')  # Format the date as desired
            else:
                date_str = "Unknown Date"

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

            message_layout = MDBoxLayout(
                orientation="vertical",
                size_hint_y=None,
                height=dp(100),
                padding=[10, 5],
                spacing=2,
                pos_hint={'center_x': 0.5}
            )

            # Create label for transaction message
            message_label = MDLabel(
                text=message,
                font_size=20,
                size_hint_y=None,
                height=self.calculate_label_height(message),  # Calculate the height based on the message length
                halign=align,
                padding=dp(5),
                valign="middle",  # Center the text vertically
                theme_text_color="Custom",  # Use custom text color
                text_color=color,  # Set the color based on sender
                # md_bg_color=(0.8, 0.8, 0.8, 1)  # Background color for the message box
            )

            # message_label.bind(
            #     texture_size=lambda label, size: setattr(message_label, "md_bg_color",("#C4E3FF")))

            # Add the message label to the message layout
            message_layout.add_widget(message_label)

            # Add the message layout to the transaction list
            self.ids.transaction_list_mdlist.add_widget(message_layout)

    def calculate_label_height(self, text):
        # Calculate the height of the label based on the length of the text
        # You can adjust this method based on your requirements
        lines = text.count("\n") + 1
        return dp(40) * lines  # Adjust the height as needed

    def add_another_textfield(self, text):
        if text:
            self.ids.another_textfield.text = text
            self.ids.another_textfield.opacity = 1
        else:
            self.ids.another_textfield.opacity = 0

    def deduct_and_transfer(self, amount):
        print("deduct_and_transfer function called with text:", amount)
        # Convert amount to integer or float
        amount = int(amount)

        date = datetime.now()

        # Fetch current user's data from wallet_users_balance
        current_user_data = app_tables.wallet_users_balance.search(
            phone=int(self.current_user_phone),
            currency_type='INR'  # Add currency_type condition
        )
        if len(current_user_data) == 1:
            current_user_data = current_user_data[0]
            existing_bal = current_user_data['balance']
            if amount > existing_bal:
                toast("Insufficient Balance.")
            else:
                # Deduct amount from current user's balance
                current_user_data['balance'] -= amount
                current_user_data.update()
                print(f'{amount} deduced from {int(self.current_user_phone)}')
                # else:
                #     print("Error: More than one row matched for current user")

                app_tables.wallet_users_transaction.add_row(
                    receiver_phone=int(self.searched_user_phone),
                    phone=int(self.current_user_phone),
                    fund=amount,
                    date=date,
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
                    print(f'{amount} added to {int(self.searched_user_phone)}')
                    # else:
                    #     print("Error: More than one row matched for searched user")

                    app_tables.wallet_users_transaction.add_row(
                        receiver_phone=int(self.current_user_phone),
                        phone=int(self.searched_user_phone),
                        fund=amount,
                        date=date,
                        transaction_type="Credit"
                    )
                    Clock.schedule_once(lambda dt: self.clear_text_field(), 0.1)

                    # Show a success toast
                    toast("Money added successfully.")
                    self.manager.current = 'dashboard'
                    self.manager.show_balance()
                else:
                    print("Error: More than one row matched for searched user")
        else:
            print("Error: More than one row matched for current user")

    def clear_text_field(self):
        self.ids.my_text_field.text = ''

    def build(self):
        custom_text_field = CustomMDTextField()
        custom_text_field.right_icon_callback = self.deduct_and_transfer
        return custom_text_field

    def go_back(self):
        self.manager.current = 'addphone'


class WalletApp(MDApp):
    def build(self):
        # Initialize screen manager
        screen_manager = ScreenManager()

        # Add screens to the screen manager
        screen_manager.add_widget(AddPhoneScreen(name='add_phone'))
        screen_manager.add_widget(UserDetailsScreen(name='user_details'))
        return screen_manager


if __name__ == '__main__':
    WalletApp().run()








