import re
import sqlite3
from datetime import datetime
from anvil.tables import app_tables
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import Screen
from kivy.base import EventLoop

KV = """
<SignInScreen>:
    Screen:
        MDTopAppBar:
            left_action_items: [["arrow-left", lambda x: root.go_back()]]
            title: 'Login'
            md_bg_color: "#1e75b9"
            specific_text_color: "#ffffff"
            pos_hint: {'top':1}

        BoxLayout:
            orientation: 'vertical'
            padding: dp(10)
            spacing: dp(10)
            size_hint_y: None
            height: dp(200)
            pos_hint: {'center_x': 0.5, 'center_y': 0.4}

            Image:
                source: 'images/login.jpg'  # Update with your image file path
                size_hint_y: None
                height: dp(170)  # Adjust the height as needed
                pos_hint: {'center_x': 0.5}
                
            MDTextField:
                id: input_text
                hint_text: "Mobile Number/User ID/Email ID"
                helper_text: "Enter your mobile number, user ID, or email ID"
                helper_text_mode: "on_focus"
                multiline: False
                required: True
                # fill_color: 255//1, 0, 0, 0.5 

            MDTextField:
                id: password_input
                hint_text: "Password"
                helper_text: "Enter your password"
                helper_text_mode: "on_focus"
                password: True
                multiline: False
                required: True
                #icon_right:"eye"
                #on_right_icon: app.toggle_password_visibility()

            MDRectangleFlatButton:
                text: "Login"
                on_release: root.sign_in(input_text.text, password_input.text)
                size_hint_x: None
                width: "150dp"
                pos_hint: {'center_x': 0.5}

"""
Builder.load_string(KV)


class SignInScreen(Screen):
    def go_back(self):
        self.manager.current = 'landing'
        self.ids.input_text.text = ''
        self.ids.password_input.text = ''

    def __init__(self, **kwargs):
        super(SignInScreen, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)

    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key in [27, 9]:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False

    def sign_in(self, input_text, password):
        date = datetime.now()
        if input_text == '' or password == '':
            # Show popup for required fields
            self.show_popup("All Fields are Required")
        else:
            try:
                if re.match(r'^\d{10}$', input_text):  # Phone number with 10 digits
                    user = app_tables.wallet_users.get(phone=float(input_text), password=password)
                elif re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', input_text):  # Email
                    user = app_tables.wallet_users.get(email=input_text, password=password)
                else:  # Assuming it's a username
                    user = app_tables.wallet_users.get(username=input_text, password=password)

                # Check if the user was found
                if user is None:
                    # Show popup for invalid user
                    self.show_popup("Invalid User")
                else:
                    # Now 'user' contains the Anvil row
                    user.update(last_login=date)
                    user_data = dict(user)
                    user_data['last_login'] = str(user_data['last_login'])
                    user.update(last_login=date)
                    print(user_data)
                    # Show popup for successful login
                    self.show_popup("Login Successful")

                    for screen in self.manager.screens:
                        self.manager.remove_widget(screen)
                    # App.get_running_app().authenticated_user_number = row['phone']
                    self.manager.add_widget(Factory.DashBoardScreen(name='dashboard'))
                    self.manager.current = 'dashboard'

                    # Save user data to JsonStore (if needed)
                    store = JsonStore('user_data.json')
                    store.put('user', value=user_data)
                    try:
                        conn = sqlite3.connect('wallet_database.db')
                        cursor = conn.cursor()
                        user = JsonStore('user_data.json').get('user')['value']
                        phone = user['phone']
                        username = user['username']
                        email = user['email']
                        password = user['password']
                        confirm_email = user['confirm_email']
                        aadhar_number = user['aadhar']
                        pan = user['pan']
                        address = user['address']
                        usertype = user['usertype']
                        banned = user['banned']
                        balance_limit = user['limit']
                        daily_limit = user['daily_limit']
                        last_login = user['last_login']

                        # Insert into wallet_users table
                        cursor.execute('''
                               INSERT INTO wallet_users (phone, username, email, password, confirm_email, aadhar_number,
                                                        pan, address, usertype, banned, balance_limit, daily_limit, last_login)
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                           ''', (phone, username, email, password, confirm_email, aadhar_number,
                                 pan, address, usertype, banned, balance_limit, daily_limit, last_login))

                        conn.commit()
                        conn.close()
                    except Exception as e:
                        print(e)
                    # Fetch and update dashboard
                    self.manager.fetch_and_update_navbar()
                    self.manager.show_balance()

            except Exception as e:
                print(e)

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
        self.ids.input_text.text = ''
        self.ids.password_input.text = ''
