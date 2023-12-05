import sqlite3

from kivy.core.window import Window
from kivymd.uix.screen import Screen
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu

Window.size = (300, 500)

KV = """
<Topup>
    MDTopAppBar:
        left_action_items: [["arrow-left", lambda x: root.go_back()]]
        title: "Top Up"
        pos_hint: {'top': 1}

    RelativeLayout:

    MDTextField:
        id: amount_field
        hint_text: "Enter Amount"
        mode: "rectangle"
        keyboardType: "numeric"
        required: True
        size_hint: None, None
        size: dp(200), dp(48)  # Adjust the size as needed
        pos_hint: {'center_x': 0.5, 'center_y': 0.65}

    MDRectangleFlatButton:
        id: bank_dropdown
        text: "change bank account"
        theme_text_color: "Custom"
        text_color: 0, 0, 0, 1  # White text color
        line_color: 0, 0, 0, 1  # Black border color
        size_hint: None, None
        on_release: root.dropdown()
        size: dp(200), dp(48)
        pos_hint: {'center_x': 0.5, 'center_y': 0.45}
        
    MDRaisedButton:
        text: "Add Money"
        on_press: root.manager.add_money()
        size_hint: None, None
        size: dp(200), dp(48)
        pos_hint: {'center_x': 0.5, 'center_y': 0.3}
    
    MDBottomAppBar:
        MDTopAppBar:
            mode: 'center'
            type: 'bottom'
            icon: 'bank'
            elevation: 1
            on_action_button: root.manager.nav_account()
"""


class Topup(Screen):
    def go_back(self):
        self.manager.current = 'dashboard'

    def dropdown(self):
        # Connect to the database
        conn = sqlite3.connect('wallet_app.db')
        cursor = conn.cursor()

        try:
            # Replace 'your_phone_number' with the actual phone number you want to fetch accounts for
            phone_number = '7019834252'

            # Execute a query to fetch unique bank names for the given phone number
            cursor.execute("SELECT DISTINCT bank_name FROM account_details WHERE phone=?", (phone_number,))
            bank_names = [row[0] for row in cursor.fetchall()]

            # Create the menu list dynamically based on the fetched bank names
            self.menu_list = [
                {"viewclass": "OneLineListItem", "text": bank_name, "on_release": lambda x=bank_name: self.test(x)}
                for bank_name in bank_names
            ]

            # Create and open the dropdown menu
            self.menu = MDDropdownMenu(
                caller=self.ids.bank_dropdown,
                items=self.menu_list,
                width_mult=4
            )
            self.menu.open()

        except sqlite3.Error as e:
            print(f"SQLite error: {e}")

        finally:
            # Close the database connection
            conn.close()

    def test(self, text):
        print(text)
        self.ids.bank_dropdown.text = text
        self.menu.dismiss()


Builder.load_string(KV)


class WalletApp(MDApp):
    def build(self):
        return Topup()


if __name__ == "__main__":
    WalletApp().run()
