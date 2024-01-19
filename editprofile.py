import requests
from kivy.lang import Builder
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import Screen

KV = """
<EditUser>
    BoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: 'Edit Profile'
            elevation: 3
            left_action_items: [['arrow-left', lambda x: root.go_back()]]
            md_bg_color: "#1e75b9"
            specific_text_color: "#ffffff"
        ScrollView:
            BoxLayout:
                orientation: "vertical"
                spacing: "10dp"
                padding: ["10dp", "1dp", "10dp", "1dp"]
                size_hint_y: None
                height: self.minimum_height
                pos_hint: {'top': 1}

                MDTextField:
                    id: username
                    text:""
                    hint_text: "Username"
                    helper_text: "Enter your username"
                    icon_right: "account"

                MDTextField:
                    id: email
                    text:""
                    hint_text: "Email"
                    helper_text: "Enter your email"
                    icon_right: "email"

                MDTextField:
                    id: phone
                    text:""
                    hint_text: "Phone Number"
                    helper_text: "Enter your phone number"
                    icon_right: "phone"
                    #readonly: True

                MDTextField:
                    id: password
                    text:""
                    hint_text: "Password"
                    helper_text: "Enter your password"
                    icon_right: "lock"
                MDTextField:
                    id: aadhaar
                    text:""
                    hint_text: "Aadhaar Number"
                    helper_text: "Enter your Aadhaar number"
                    icon_right: "fingerprint"
                    readonly: True

                MDTextField:
                    id: pan
                    text:""
                    hint_text: "PAN Number"
                    helper_text: "Enter your PAN number"
                    icon_right: "credit-card"
                    readonly: True

                MDTextField:
                    id: address
                    text:""
                    hint_text: "Address"
                    helper_text: "Enter your address"
                    icon_right: "home"

                MDRaisedButton:
                    text: "Save Edit"
                    on_release: root.save_edit()
                    pos_hint: {'center_x': 0.5}
                    #pos_hint:{'center_x': 0.8, 'center_y':0.4}
                    
"""
Builder.load_string(KV)



class EditUser(Screen):
    def go_back(self):
        self.manager.current = 'settings'

    def save_edit(self):
        edit_scr = self.manager.get_screen('edituser')
        phone = edit_scr.ids.phone.text
        username = edit_scr.ids.username.text
        gmail = edit_scr.ids.email.text
        password = edit_scr.ids.password.text
        Aadhaar = edit_scr.ids.aadhaar.text
        pan = edit_scr.ids.pan.text
        address = edit_scr.ids.address.text

        try:
            # Replace "your-project-id" with your actual Firebase project ID
            database_url = "https://e-wallet-realtime-database-default-rtdb.asia-southeast1.firebasedatabase.app"
            login_endpoint = f"{database_url}/login/{phone}.json"

            # Make a GET request to check if the user exists
            response = requests.get(login_endpoint)

            # Check if the user exists (status code 200)
            if response.status_code == 200:
                # Make a PATCH request to update the user details
                response = requests.patch(login_endpoint, json={
                    'username': username,
                    'gmail': gmail,
                    'password': password,
                    'Aadhaar': Aadhaar,
                    'pan': pan,
                    'address': address
                })

                # Check if the update was successful
                if response.status_code == 200:
                    print("User details updated successfully.")
                    self.show_update_success_popup()
                else:
                    print(f"Failed to update user details. Status code: {response.status_code}")
                    self.manager.show_error_popup(f"Failed to update user details. Status code: {response.status_code}")
            else:
                print(f"User with phone number {phone} does not exist.")
                self.manager.show_error_popup(f"User with phone number {phone} does not exist.")

        except Exception as e:
            print(f"Error updating user details: {e}")
            self.manager.show_error_popup(f"Error updating user details: {e}")
            print(e)

    def show_update_success_popup(self):
        dialog = MDDialog(
            title="Update Success",
            text="Your profile has been updated successfully. Please log in again.",
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda *args: (dialog.dismiss(), self.manager.logout())
                )
            ]
        )
        dialog.open()
