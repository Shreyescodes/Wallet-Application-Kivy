import sqlite3
from kivy.core.window import Window
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder

Window.size = (300, 500)
kv_string = '''
<TransferScreen>
    MDScreen:
        BoxLayout:
            orientation: 'vertical'
            spacing:dp(10)
            MDTopAppBar:
                title: 'Money Transfer'
                elevation: 3
                left_action_items: [['arrow-left', lambda x: root.go_back()]]
                md_bg_color: app.theme_cls.primary_color 

            BoxLayout:
                orientation: 'vertical'
                spacing: dp(15)


                MDTextField:
                    id:amount_field
                    mode:'rectangle'
                    hint_text: "Amount"
                    helper_text: "Enter the amount to transfer"
                    helper_text_mode: "on_focus"
                    input_type: "number"
                    pos_hint: {"center_x": 0.5, "center_y": 0.8}
                    size_hint_x:None
                    width:300

                MDTextField:
                    id:mobile_no_field
                    hint_text: "Mobile no"
                    helper_text: "Enter Receiver's mobile number"
                    helper_text_mode: "on_focus"
                    input_type: "number"
                    pos_hint: {"center_x": 0.5, "center_y": 0.7}
                    size_hint_x:None
                    width:300


                MDTextField:
                    id:receiver_name_field
                    hint_text: "Receiver's Name"
                    helper_text: "Enter receiver's name"
                    helper_text_mode: "on_focus"
                    pos_hint: {"center_x": 0.5, "center_y": 0.6}
                    size_hint_x:None
                    width:300

                MDTextField:
                    id:receiver_e_wallet_field
                    hint_text: "Receiver's E-Wallet Number"
                    helper_text: "Enter receiver's t number"
                    helper_text_mode: "on_focus"
                    input_type: "number"
                    pos_hint: {"center_x": 0.5, "center_y": 0.5}
                    size_hint_x:None
                    width:300

                Spinner:
                    id: currency_spinner
                    text: 'Currency'
                    values: ['INR', 'USD', 'EUROS', 'POUND']
                    size_hint: None, None
                    pos_hint: {'center_x': 0.5, 'center_y': 0.45}
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
                    pos_hint: {"center_x": 0.5, "center_y": 0.4}

'''
Builder.load_string(kv_string)


class TransferScreen(Screen):
    def go_back(self):
        self.manager.current = 'dashboard'

    def transfer_money(self):
        # Get data from the text fields and spinner
        amount = float(self.ids.amount_field.text)
        receiver_phone = self.ids.mobile_no_field.text
        receiver_name = self.ids.receiver_name_field.text
        receiver_e_wallet = self.ids.receiver_e_wallet_field.text
        currency = self.ids.currency_spinner.text
        print(amount, receiver_phone, receiver_name, receiver_e_wallet, currency)

        store = JsonStore('user_data.json')
        sender_phone = store.get('user')['value'][3]
        conn = sqlite3.connect('wallet_app.db')
        cursor = conn.cursor()

        total_balance = self.manager.get_total_balance(sender_phone)
        print(total_balance)
        conn = sqlite3.connect('wallet_app.db')
        cursor = conn.cursor()
        if total_balance < amount:
            toast("insufficient balance")
            return
        try:
            cursor.execute("""INSERT INTO add_money ( currency_type, balance, e_money, phone_no, bank_name)
                            VALUES ( ?, ?, ?, ?, ?)""", (currency, 0, -amount, sender_phone, "e_wallet"))
            cursor.execute("""INSERT INTO add_money ( currency_type, balance, e_money, phone_no, bank_name)
                                        VALUES (?, ?, ?, ?, ?)""", (currency, 0, amount, receiver_phone, "e_wallet"))

            conn.commit()
            toast("money sent successfully")
            self.manager.get_total_balance(sender_phone)
            self.manager.show_balance()
            self.manager.current = 'dashboard'


        except ValueError:
            toast("invalid amount")

        finally:
            conn.close()


class MoneyTransferApp(MDApp):
    def build(self):
        # self.theme_cls.theme_style = "Dark"
        # self.theme_cls.primary_palette = "BlueGray"

        return Builder.load_string(kv_string)


if __name__ == "__main__":
    MoneyTransferApp().run()
