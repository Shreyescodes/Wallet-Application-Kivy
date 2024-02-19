# from datetime import datetime
# import requests
# from anvil.tables import app_tables
# from kivy.lang import Builder
# from kivy.storage.jsonstore import JsonStore
# from kivymd.toast import toast
# from kivymd.uix.button import MDFlatButton
# from kivymd.uix.dialog import MDDialog
# from kivymd.uix.screen import Screen
# from kivy.base import EventLoop
# from kivy.core.window import Window
# kv_string = '''
# <TransferScreen>
#     MDScreen:
#         MDTopAppBar:
#             title: 'Money Transfer'
#             elevation: 3
#             left_action_items: [['arrow-left', lambda x: root.go_back()]]
#             md_bg_color: "#1e75b9"
#             specific_text_color: "#ffffff"
#             pos_hint:{'top':1}
#         MDLabel:
#             text: 'Choose Currency Type'
#             font_size: '24sp'  # Adjust the font size as needed
#             bold: True
#             pos_hint: {'center_x': 0.2, 'center_y': 0.39}
#         BoxLayout:
#             orientation: 'vertical'
#             padding: dp(10)
#             spacing: dp(20)
#             size_hint_y: None
#             height: self.minimum_height
#             pos_hint: {'center_x': 0.5, 'center_y': 0.5}
#
#             # Image:
#             #     source: 'images/trans.jpg'  # Update with your image file path
#             #     size_hint_y: None
#             #     height: dp(170)  # Adjust the height as needed
#             #     pos_hint: {'center_x': 0.5}
#
#             Spinner:
#                 id: currency_spinner
#                 text: 'Currency'
#                 values: ['INR', 'USD', 'EUROS', 'POUND']
#                 size_hint: None, None
#                 pos_hint: {'center_x': 0.5, 'center_y': 0.35}
#                 size: "150dp", "50dp"
#                 # on_text: app.select_currency(self.text)
#                 md_bg_color: 52/255.0, 171/255.0, 235/255.0,0
#                 canvas.before:
#                     Color:
#                         rgba: 52/255.0, 171/255.0, 235/255.0,0  # Set the background color (in this case, a dark gray)
#                     Rectangle:
#                         pos: self.pos
#                         size: self.size
#
#             MDTextField:
#                 id:amount_field
#                 mode:'rectangle'
#                 hint_text: "Amount"
#                 helper_text: "Enter the amount to transfer"
#                 helper_text_mode: "on_focus"
#                 input_type: "number"
#                 spacing: dp(10)
#                 #pos_hint: {"center_x": 0.5, "center_y": 0.8}
#                 #width:300
#
#             MDTextField:
#                 id:mobile_no_field
#                 hint_text: "Mobile no"
#                 helper_text: "Enter Receiver's mobile number"
#                 helper_text_mode: "on_focus"
#                 input_type: "number"
#                 # pos_hint: {"center_x": 0.5, "center_y": 0.7}
#                 # size_hint_x:None
#                 # width:300
#
#
#
#
#             MDRaisedButton:
#                 text: "Transfer Money"
#                 on_release: root.transfer_money()
#                 pos_hint: {"center_x": 0.5, "center_y": 0.27}
#
# '''
# Builder.load_string(kv_string)
#
#
# class TransferScreen(Screen):
#     def go_back(self):
#         self.manager.current = 'dashboard'
#     def __init__(self, **kwargs):
#         super(TransferScreen, self).__init__(**kwargs)
#         EventLoop.window.bind(on_keyboard=self.on_key)
#
#
#     def on_key(self, window, key, scancode, codepoint, modifier):
#         # 27 is the key code for the back button on Android
#         if key in [27,9]:
#             self.go_back()
#             return True  # Indicates that the key event has been handled
#         return False
#     import requests
#     from kivymd.toast import toast
#     from kivymd.uix.dialog import MDDialog
#     from kivymd.uix.button import MDFlatButton
#     from datetime import datetime
#
#     def transfer_money(self):
#         # Get data from the text fields and spinner
#         amount = float(self.ids.amount_field.text)
#         try:
#             receiver_phone = float(self.ids.mobile_no_field.text)
#         except ValueError:
#             toast("Invalid mobile number. Please enter a valid numeric value.")
#             return
#         currency = self.ids.currency_spinner.text
#
#         store = JsonStore('user_data.json')
#         senders_phone = store.get('user')['value']["phone"]
#         date = datetime.now()
#         sender = app_tables.wallet_users_balance.get(phone=senders_phone, currency_type=currency)
#         # check reciever is exist or not
#         rec_exist = self.check_reg(receiver_phone)
#         if rec_exist is None:
#             self.show_not_registered_dialog()
#             return
#         reciever = app_tables.wallet_users_balance.get(phone=receiver_phone, currency_type=currency)
#         try:
#             if sender is not None:
#                 s_old_balance = sender['balance']
#                 if amount <= s_old_balance:
#                     new_balance = s_old_balance - amount
#                     sender['balance'] = new_balance
#                     if reciever is None:
#                         app_tables.wallet_users_balance.add_row(
#                             phone=receiver_phone,
#                             currency_type=currency,
#                             balance=amount
#                         )
#                     else:
#                         r_old_balance = reciever['balance']
#                         r_new_balance = r_old_balance + amount
#                         reciever['balance'] = r_new_balance
#                         reciever.update()
#                     sender.update()
#                 else:
#                     toast("balance is less than entered amount")
#                 app_tables.wallet_users_transaction.add_row(
#                     receiver_phone=receiver_phone,
#                     phone=senders_phone,
#                     fund=amount,
#                     date=date,
#                     transaction_status="success",
#                     transaction_type="debit"
#                 )
#                 app_tables.wallet_users_transaction.add_row(
#                     receiver_phone=senders_phone,
#                     phone=receiver_phone,
#                     fund=amount,
#                     date=date,
#                     transaction_type="credit",
#                     transaction_status="success"
#                 )
#                 toast("Money added successfully.")
#                 self.manager.current = 'dashboard'
#                 self.manager.show_balance()
#             else:
#                 toast("you dont have a balance in this currency type")
#         except Exception as e:
#             toast("an error occurred")
#             print(e)
#
#     def show_not_registered_dialog(self):
#         # Show a dialog indicating that the receiver's phone number is not registered
#         dialog = MDDialog(
#             title="Receiver Not Registered",
#             text="The provided phone number is not registered. Consider inviting the user to join.",
#             buttons=[
#                 MDFlatButton(
#                     text="OK",
#                     on_release=lambda *args: dialog.dismiss()
#                 )
#             ]
#         )
#         dialog.open()
#
#     def check_reg(self, phone):
#         return app_tables.wallet_users.get(phone=phone)
#
#
#
from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import Screen
from kivymd.uix.spinner import MDSpinner
from datetime import datetime
import requests
from anvil.tables import app_tables
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivymd.toast import toast
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import Screen
from kivy.base import EventLoop
from kivy.core.window import Window

kv_string = ''' 
<TransferScreen>:
    MDScreen:

        BoxLayout:
            orientation: 'vertical'
            
            MDTopAppBar:
                title: "Money Transfer          "
                left_action_items: [["arrow-left", lambda x: root.go_back()]]
                md_bg_color: app.theme_cls.primary_color
                specific_text_color: 1, 1, 1, 1
            
                
            ScrollView:
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: self.minimum_height
                    padding: "10dp"
                    spacing: "13dp"
                    Widget:
                        size_hint_y: None
                        height: '4dp'
                    MDLabel:
                        text: "Transfer to New Number"
                        halign: 'center'
                        bold:True
                        theme_text_color: "Secondary"
                    Widget:
                        size_hint_y: None
                        height: '7dp'
                    MDRectangleFlatButton:
                        radius:40,40,40,40
                        id: currency_spinner
                        text: 'Currency'
                        size_hint: 1, None
                        size: "150dp", "50dp"
                        pos_hint: {'center_x': 0.5}
                        on_release: root.show_currency_menu()    
        
                    MDTextField:
                        mode: "rectangle"
                        hint_text: " Beneficiary Name"
                        pos_hint: {'center_x': .5}
                        line_color_normal: app.theme_cls.primary_color
                        
                    
                            
                    MDTextField:
                        id:mobile_no_field
                        input_type: "number"
                        mode: "rectangle"
                        hint_text: " Mobile Number"
                        pos_hint: {'center_x': .5}
                        line_color_normal: app.theme_cls.primary_color
        
                    MDLabel:
                        text: "Note:Please note that only the beneficiary account number and IFSC information will be used for Quick transfer. (Please ensure correctness), the beneficiary name provided will not be considered as per RBI guidelines."
                        theme_text_color: "Secondary"
                        font_size: "12sp"
                        halign: 'left'
                        size_hint_y: None
                        height: self.texture_size[1] + dp(10)  # Adjust padding
                    Widget:
                        size_hint_y: None
                        height: '4dp'    
                    BoxLayout:
                        orientation: "horizontal"
                        row:1
                        col:2
                        spacing:dp(5)
                        padding:dp(-5)
                        pos_hint: {'center_x': 0.5, 'center_y': 0.35}
                       
                        MDCheckbox:
                            id: test_money
                            size_hint: None, None
                            size: "48dp", "48dp"
                            pos_hint: {'center_x': 0.5, 'center_y': 0.35}
                            on_active: root.update_transfer_amount(self.active)
            
                        MDLabel:
                            text: "Send 1$ as test money amount (Optional)"
                            theme_text_color: "Secondary"
                            font_size: "12sp"
                            halign: 'left'
                            size_hint_y: None
                            height: self.texture_size[1] + dp(10)  # Adjust padding
                            pos_hint: {'center_x': 0.5, 'center_y': 0.35}
                    Widget:
                        size_hint_y: None
                        height: '3dp'
                    MDTextField:
                        id:amount_field
                        mode: "rectangle"
                        hint_text: " Transfer Amount"
                        pos_hint: {'center_x': .5}
                        line_color_normal: app.theme_cls.primary_color
        
                    MDTextField:
                        mode: "rectangle"
                        hint_text: " Enter Purpose"
                        pos_hint: {'center_x': .5}
                        line_color_normal: app.theme_cls.primary_color
                    Widget:
                        size_hint_y: None
                        height: '5dp'
                    MDRectangleFlatIconButton:
                        text: "Pay"
                        pos_hint: {"center_x": .5}
                        md_bg_color: app.theme_cls.primary_color
                        text_color: 1, 1, 1, 1
                        size_hint: .7, None
                        on_release: root.transfer_money() 


'''
Builder.load_string(kv_string)


class TransferScreen(Screen):

    def go_back(self):
        self.manager.current = 'dashboard'

    def __init__(self, **kwargs):
        super(TransferScreen, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)

    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key in [27, 9]:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False

    import requests
    from kivymd.toast import toast
    from kivymd.uix.dialog import MDDialog
    from kivymd.uix.button import MDFlatButton
    from datetime import datetime

    def transfer_money(self):
        # Get data from the text fields and spinner
        amount = float(self.ids.amount_field.text)
        try:
            receiver_phone = float(self.ids.mobile_no_field.text)
        except ValueError:
            toast("Invalid mobile number. Please enter a valid numeric value.")
            return
        currency = self.ids.currency_spinner.text

        store = JsonStore('user_data.json')
        senders_phone = store.get('user')['value']["phone"]
        date = datetime.now()
        sender = app_tables.wallet_users_balance.get(phone=senders_phone, currency_type=currency)
        # check reciever is exist or not
        rec_exist = self.check_reg(receiver_phone)
        if rec_exist is None:
            self.show_not_registered_dialog()
            return
        reciever = app_tables.wallet_users_balance.get(phone=receiver_phone, currency_type=currency)
        try:
            if sender is not None:
                s_old_balance = sender['balance']
                if amount <= s_old_balance:
                    new_balance = s_old_balance - amount
                    sender['balance'] = new_balance
                    if reciever is None:
                        app_tables.wallet_users_balance.add_row(
                            phone=receiver_phone,
                            currency_type=currency,
                            balance=amount
                        )
                    else:
                        r_old_balance = reciever['balance']
                        r_new_balance = r_old_balance + amount
                        reciever['balance'] = r_new_balance
                        reciever.update()
                    sender.update()
                else:
                    toast("balance is less than entered amount")
                app_tables.wallet_users_transaction.add_row(
                    receiver_phone=receiver_phone,
                    phone=senders_phone,
                    fund=amount,
                    date=date,
                    transaction_status="success",
                    transaction_type="Debit"
                )
                app_tables.wallet_users_transaction.add_row(
                    receiver_phone=senders_phone,
                    phone=receiver_phone,
                    fund=amount,
                    date=date,
                    transaction_type="Credit",
                    transaction_status="success"
                )
                toast("Money added successfully.")
                self.manager.current = 'dashboard'
                self.manager.show_balance()
            else:
                toast("you dont have a balance in this currency type")
        except Exception as e:
            toast("an error occurred")
            print(e)

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


    def check_reg(self, phone):
        return app_tables.wallet_users.get(phone=phone)

    def show_currency_menu(self):
        currencies = ['INR', 'USD', 'EUROS', 'POUND']
        menu_items = [{"text": currency, "viewclass": "OneLineListItem", "height": dp(44),"on_release": lambda x=currency: self.test(x)} for currency in currencies]

        menu = MDDropdownMenu(
            caller=self.ids.currency_spinner,
            items=menu_items,
            width_mult=4,
        )

        def set_currency(instance_menu, instance_menu_item):
            self.selected_currency = instance_menu_item.text
            self.ids.currency_spinner.text = self.selected_currency
            menu.dismiss()

        menu.bind(on_release=set_currency)
        menu.open()
    def test(self,text):
        self.ids.currency_spinner.text = text

    def update_transfer_amount(self, active):
        if active:
            self.ids.amount_field.text = "1"
        else:
            self.ids.amount_field.text = ""


