import re
import requests
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import Screen

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

    def sign_in(self, input_text, password):
        if input_text == '' or password == '':
            # Show popup for required fields
            self.show_popup("All Fields are Required")
        else:
            try:
                database_url = "https://e-wallet-realtime-database-default-rtdb.asia-southeast1.firebasedatabase.app/"

                # Function to query the 'login' collection in Firebase
                def query_login_collection(field, value):
                    login_endpoint = f"{database_url}/login.json"
                    params = {'orderBy': f'"{field}"', 'equalTo': f'"{value}"'}
                    response = requests.get(login_endpoint, params=params)
                    return response.json()

                # Use regex to determine the type of input
                if re.match(r'^\d{10}$', input_text):  # Phone number with 10 digits
                    query_result = query_login_collection('phone', input_text)
                elif re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', input_text):  # Email
                    query_result = query_login_collection('gmail', input_text)
                else:  # Assuming it's a username
                    query_result = query_login_collection('username', input_text)

                # Check if any documents were found
                if not query_result:
                    # Show popup for invalid user
                    self.show_popup("Invalid User")
                else:
                    # Fetch the first document (if there are multiple matches, you may need to handle it differently)
                    user_data = next(iter(query_result.values()))

                    # Now 'user_data' contains the inner dictionary
                    row = user_data
                    print(row)
                    # Show popup for successful login
                    self.show_popup("Login Successful")
                    self.manager.current = 'dashboard'

                    # Save user data to JsonStore (if needed)
                    store = JsonStore('user_data.json')
                    store.put('user', value=row)

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
