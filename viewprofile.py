from logging import root
from kivy.app import App
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.screen import Screen
from kivy.uix.camera import Camera


KV = """
<Profile>
    name: 'view'
    BoxLayout:
        orientation: 'vertical'
        spacing: dp(10)
        # padding: dp(10)
        pos_hint: {'top': 1}

        MDTopAppBar:
            title: 'Profile'
            elevation: 3
            left_action_items: [['arrow-left', lambda x: root.go_back()]]
            md_bg_color: "#1e75b9"
            specific_text_color: "#ffffff"
            size_hint_y: None  # Disable automatic height adjustment
            height: dp(56)  # Set the desired height of the MDTopAppBar

        
        MDIconButton:
            icon: "camera"
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_color
            md_bg_color: "#e1eaea"
            size_hint_y: None
            height: 200
            pos_hint: {'center_x': 0.5, 'center_y': 0.9}
            on_release: root.open_camera()
                        

        ScrollView:
            BoxLayout:
                orientation: 'vertical'
                spacing: dp(5)
                padding: dp(20)

                # Profile Details
                MDTextField:
                    id: username_label
                    hint_text: "Username"
                    icon_left: "account"
                    mode: "rectangle"
                    readonly: True
                    

                BoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: dp(66)
                    padding: dp(2.8)
                    spacing: dp(5)
                    MDTextField:
                        id: email_label
                        hint_text: "Email"
                        mode: "rectangle"
                        icon_left: "email"
                        readonly: True
                        theme_text_color: "Custom"
                        text_color: '#000000'  # Set text color to black
                        font_style: "Button"
                        bold: True
                    MDIconButton:
                        icon: "pencil"
                        pos_hint: {'center_y': 0.5}
                        on_release: root.enable_email_edit()    

                BoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: dp(66)
                    padding: dp(2.8)
                    spacing: dp(5)
                    MDTextField:
                        id: contact_label
                        hint_text: "Phone No."
                        mode: "rectangle"
                        icon_left: "phone"
                        readonly: True
                        theme_text_color: "Custom"
                        text_color: '#000000'  # Set text color to black
                        font_style: "Button"
                        bold: True
                    MDIconButton:
                        icon: "pencil"
                        pos_hint: {'center_y': 0.5}
                        on_release: root.enable_contact_edit()
                MDTextField:
                    id: aadhaar_label
                    hint_text: "Aadhaar"
                    icon_left: "fingerprint"
                    mode: "rectangle"
                    readonly: True

                MDTextField:
                    id: pan_label
                    hint_text: "PAN"
                    icon_left: "credit-card"
                    #mode: "rectangle"
                    mode: "rectangle"
                    readonly: True

                MDTextField:
                    id: address_label
                    hint_text: "Address"
                    icon_left: "map-marker"
                    mode: "rectangle"
                    readonly: True

                MDRaisedButton:
                    id: edit_save_button
                    text: "Edit Profile"
                    size_hint: None, None
                    size: dp(150), dp(50)
                    pos_hint: {'center_x': 0.5}  
                    on_release: root.edit_save_profile()   

"""
Builder.load_string(KV)


class Profile(Screen):
    current_user_data = None
    editing_mode = False  # Initialize editing_mode attribute
    email_editing = False  # Attribute to track email editing


    def __init__(self, **kwargs):
        super(Profile, self).__init__(**kwargs)
        self.editing_mode = False  # Initialize editing_mode in the __init__ method
        self.email_editing = False  # Initialize email_editing
        
    def enable_email_edit(self):
        self.ids.email_label.readonly = False  # Enable email editing
        self.ids.edit_save_button.text = "Save"  # Change button text to 'Save'
        self.email_editing = True  # Set email_editing flag to True  

    def save_email(self, new_email):
        self.ids.email_label.text = new_email  # Update the label with the new email
        self.update_email(new_email)  # Save the new email to the JSON file
        self.disable_email_edit()  # Disable email editing after saving

    def disable_email_edit(self):
        self.ids.email_label.readonly = True  # Disable email editing
        self.ids.edit_save_button.text = "Edit Profile"  # Change button text to 'Edit Profile'
        self.email_editing = False  # Set email_editing flag to False

    def edit_profile(self):
        edit_screen = self.manager.get_screen('edituser')

        store = JsonStore('user_data.json').get('user')['value']

        edit_screen.ids.username.text = store["username"]
        edit_screen.ids.email.text = store["gmail"]
        edit_screen.ids.phone.text = store["phone"]
        edit_screen.ids.password.text = store["password"]
        edit_screen.ids.aadhaar.text = store["Aadhaar"]
        edit_screen.ids.pan.text = store["pan"]
        edit_screen.ids.address.text = store["address"]
        self.manager.current = 'edituser'

    def save_profile(self):
        self.editing_mode = False  # Switch back to edit mode after saving
        

    def update_email(self, new_email):
        # Update email in the JSON file
        store = JsonStore('user_data.json')  # Load the JSON store
        if store.exists('user'):
            user_data = store.get('user')
            user_data['value']['gmail'] = new_email  # Update the 'gmail' field with the new value
            store.put('user', **user_data)  # Put the updated data back into the JSON store
            self.fetch_and_update_navbar()
            self.fetch_and_update_complaint()
            print('new gmail updated')

    def fetch_and_update_navbar(self):
        store = JsonStore('user_data.json').get('user')['value']
        # Update labels in NavbarScreen
        navbar_screen = self.manager.get_screen('navbar')
        navbar_screen.ids.username_label.text = store["username"]
        navbar_screen.ids.email_label.text = store["gmail"]
        navbar_screen.ids.contact_label.text = store["phone"]      

    def fetch_and_update_complaint(self):
        store = JsonStore('user_data.json').get('user')['value']
        # Update labels in ComplaintScreen
        complaint_screen = self.manager.get_screen('complaint')
        complaint_screen.ids.email_label.text = store["gmail"]    
        
    def edit_save_profile(self):
        if self.email_editing:
            new_email = self.ids.email_label.text  # Get the updated email from the UI
            self.update_email(new_email)  # Update email in the JSON file     
            self.disable_email_edit()  # Disable email editing mode
            self.save_profile()  # If in email editing mode, save the email
        else:
            # Toggle between 'Edit Profile' and 'Save' for other fields
            if self.editing_mode:
                self.save_profile()  # If in save mode, save the profile
                self.ids.edit_save_button.text = "Edit Profile"  # Change button text to 'Edit Profile'
            else:
                self.edit_profile()  # If in edit mode, perform editing actions
                self.ids.edit_save_button.text = "Save"  # Change button text to 'Save'
            self.editing_mode = not self.editing_mode  # Toggle editing mode
            on_release: root.save_edit()
                
    def go_back(self):
        self.manager.current = 'navbar'

    def open_camera(self):
        print("Opening camera") 
           