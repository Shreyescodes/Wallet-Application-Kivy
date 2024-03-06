from logging import root
from kivy.app import App
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.screen import Screen
from kivy.uix.camera import Camera
from kivy.base import EventLoop
from kivy.core.window import Window

KV = """
<Profile>:
    Screen:
        MDScreen:
            BoxLayout:
                orientation: "vertical"
                MDTopAppBar:
                    title: 'Profile'
                    elevation: 3
                    left_action_items: [['arrow-left', lambda x: root.go_back()]]
                    md_bg_color: "#148EFE"
                    specific_text_color: "#ffffff"
                # Scrollable part
                ScrollView:
                    BoxLayout: 
                        size_hint_y: None
                        height: dp(580)
                        pos_hint: {'center_x': 0.45, 'y': 280}
                        spacing:dp(15)
                        padding:dp(12)        

                        BoxLayout:
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height
                            spacing: dp(15)
                            padding: dp(12)

                            MDIconButton:
                                icon: "camera"
                                spacing:dp(15)
                                theme_text_color: "Custom"
                                text_color: app.theme_cls.primary_color
                                # hint_text_color_normal: "#484848"
                                # text_color_normal:"#484848"
                                # icon_left_color_normal:"#484848"
                                # line_color_normal:"#484848"
                                md_bg_color: "#e1eaea"
                                size_hint_y: None
                                height: 200
                                pos_hint: {'center_x': 0.5, 'center_y': 0.9}
                                on_release: root.open_camera()

                            # Profile Details
                            MDTextField:
                                hint_text:'Username'
                                spacing:dp(15)
                                id: username_label
                                hint_text_color_normal: "#148efe"
                                text_color_normal:"#484848"
                                icon_left_color_normal:"#148efe"
                                line_color_normal:"#148efe"
                                radius:[30,30,30,30]
                                icon_left: "account"
                                mode: "rectangle"
                                readonly: True

                            # BoxLayout:
                            #     orientation: 'horizontal'
                            #     size_hint_y: None
                            #     height: dp(66)
                            #     padding: dp(3)
                            #     spacing: dp(15)
                            MDTextField:
                                spacing:dp(15)
                                id: email_label
                                hint_text:'Email'
                                text_color_normal:"#484848"
                                hint_text_color_normal: "#148efe"
                                icon_left_color_normal:"#148efe"
                                line_color_normal:"#148efe"
                                radius:[30,30,30,30]
                                mode: "rectangle"
                                icon_left: "email"
                                readonly: True
                                theme_text_color: "Custom"
                                text_color: '#000000'  # Set text color to black
                                font_style: "Button"
                                bold: True
                                # MDIconButton:
                                #     icon: "pencil"
                                #     pos_hint: {'center_y': 0.5}
                                #     on_release: root.enable_email_edit()  

                            # BoxLayout:
                            #     orientation: 'horizontal'
                            #     size_hint_y: None
                            #     height: dp(66)
                            #     padding: dp(2.8)
                            #     spacing: dp(15)
                            MDTextField:
                                spacing: dp(15)
                                id: contact_label
                                hint_text:"Contact"
                                hint_text_color_normal: "#148efe"
                                text_color_normal:"#484848"
                                line_color_normal:"#148efe"
                                radius:[30,30,30,30]
                                mode: "rectangle"
                                icon_left: "phone"
                                readonly: True
                                theme_text_color: "Custom"
                                text_color: '#000000'  # Set text color to black
                                icon_left_color_normal:"#148efe"
                                font_style: "Button"
                                bold: True
                                # MDIconButton:
                                #     icon: "pencil"
                                #     pos_hint: {'center_y': 0.5}
                                #     on_release: root.enable_contact_edit() 

                            MDTextField:
                                spacing:dp(15)
                                id: aadhaar_label
                                hint_text_color_normal: "#148efe"
                                line_color_normal:"#148efe"
                                text_color_normal:"#484848"
                                hint_text:'Aadhaar'
                                radius:[30,30,30,30]
                                icon_left: "fingerprint"
                                icon_left_color_normal:"#148efe"
                                mode: "rectangle"
                                readonly: True

                            MDTextField:
                                spacing:dp(15)
                                id: pan_label
                                text_color_normal:"#484848"
                                hint_text_color_normal: "#148efe"
                                line_color_normal:"#148efe"
                                hint_text:'Pan'
                                radius:[30,30,30,30]
                                icon_left: "credit-card"
                                icon_left_color_normal:"#148efe"
                                #mode: "rectangle"
                                mode: "rectangle"
                                readonly: True

                            MDTextField:

                                hint_text:'Address'
                                hint_text_color_normal: "#148efe"
                                text_color_normal:"#484848"
                                line_color_normal:"#148efe"
                                # mode:'persistent'
                                text_color:0,0,0,1
                                # line_color_focus:1,0,0,1
                                font_color:0,0,0,1
                                id: address_label
                                icon_left: "map-marker"
                                icon_left_color_normal:"#148efe"
                                mode: "rectangle"
                                radius:[30,30,30,30]
                                readonly: True


                            MDRaisedButton:
                                spacing:dp(15)
                                id: edit_save_button
                                text: "Edit Profile"
                                size_hint: None, None
                                size: dp(150), dp(50)
                                pos_hint: {'center_x': 0.5}  
                                on_release: root.edit_profile()   

"""
Builder.load_string(KV)

from kivy.animation import Animation


class Profile(Screen):
    # current_user_data = None
    # editing_mode = False  # Initialize editing_mode attribute
    # email_editing = False  # Attribute to track email editing

    def animate_textfield(self):
        Animation(background_color=(1, 0.9, 0.9, 1)).start(self)

    def __init__(self, **kwargs):
        super(Profile, self).__init__(**kwargs)
        self.editing_mode = False  # Initialize editing_mode in the __init__ method
        self.email_editing = False  # Initialize email_editing

    # def enable_email_edit(self):
    #     self.ids.email_label.readonly = False  # Enable email editing
    #     self.ids.edit_save_button.text = "Save"  # Change button text to 'Save'
    #     self.email_editing = True  # Set email_editing flag to True

    # def save_email(self, new_email):
    #     self.ids.email_label.text = new_email  # Update the label with the new email
    #     self.update_email(new_email)  # Save the new email to the JSON file
    #     self.disable_email_edit()  # Disable email editing after saving

    # def disable_email_edit(self):
    #     self.ids.email_label.readonly = True  # Disable email editing
    #     self.ids.edit_save_button.text = "Edit Profile"  # Change button text to 'Edit Profile'
    #     self.email_editing = False  # Set email_editing flag to False

    def edit_profile(self):
        self.manager.add_widget(Factory.EditUser(name='edituser'))
        edit_screen = self.manager.get_screen('edituser')
        store = JsonStore('user_data.json').get('user')['value']
        edit_screen.ids.username.text = store["username"]
        edit_screen.ids.email.text = store["email"]
        edit_screen.ids.phone.text = str(store["phone"])
        edit_screen.ids.password.text = store["password"]
        edit_screen.ids.aadhaar.text = str(store["aadhar"])
        edit_screen.ids.pan.text = store["pan"]
        edit_screen.ids.address.text = store["address"]
        self.manager.current = 'edituser'

    # def save_profile(self):
    #     self.editing_mode = False  # Switch back to edit mode after saving

    # def update_email(self, new_email):
    #     # Update email in the JSON file
    #     store = JsonStore('user_data.json')  # Load the JSON store
    #     if store.exists('user'):
    #         user_data = store.get('user')
    #         user_data['value']['gmail'] = new_email  # Update the 'gmail' field with the new value
    #         store.put('user', **user_data)  # Put the updated data back into the JSON store
    #         self.fetch_and_update_navbar()
    #         self.fetch_and_update_complaint()
    #         print('new gmail updated')

    # def fetch_and_update_navbar(self):
    #     store = JsonStore('user_data.json').get('user')['value']
    #     # Update labels in NavbarScreen
    #     navbar_screen = self.manager.get_screen('navbar')
    #     navbar_screen.ids.username_label.text = store["username"]
    #     navbar_screen.ids.email_label.text = store["gmail"]
    #     navbar_screen.ids.contact_label.text = store["phone"]

    # def fetch_and_update_complaint(self):
    #     store = JsonStore('user_data.json').get('user')['value']
    #     # Update labels in ComplaintScreen
    #     complaint_screen = self.manager.get_screen('complaint')
    #     complaint_screen.ids.email_label.text = store["gmail"]

    # def edit_save_profile(self):
    #     if self.email_editing:
    #         new_email = self.ids.email_label.text  # Get the updated email from the UI
    #         self.update_email(new_email)  # Update email in the JSON file
    #         self.disable_email_edit()  # Disable email editing mode
    #         self.save_profile()  # If in email editing mode, save the email
    #     else:
    #         # Toggle between 'Edit Profile' and 'Save' for other fields
    #         if self.editing_mode:
    #             self.save_profile()  # If in save mode, save the profile
    #             self.ids.edit_save_button.text = "Edit Profile"  # Change button text to 'Edit Profile'
    #         else:
    #             self.edit_profile()  # If in edit mode, perform editing actions
    #             self.ids.edit_save_button.text = "Save"  # Change button text to 'Save'
    #         self.editing_mode = not self.editing_mode  # Toggle editing mode
    #         on_release: root.save_edit()

    def go_back(self):
        self.manager.current = 'dashboard'

    def __init__(self, **kwargs):
        super(Profile, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)

    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key in [27, 9]:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False

    def open_camera(self):
        print("Opening camera")
