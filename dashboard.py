import base64
import io
import traceback
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.uix.image import Image
import qrcode
from kivy.storage.jsonstore import JsonStore
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivymd.material_resources import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from anvil.tables import app_tables
from kivy.core.window import Window
from addPhone import AddPhoneScreen
from transfer import TransferScreen
from withdraw import WithdrawScreen
from accmanage import AccmanageScreen
from addAccount import AddAccountScreen
from complaint import ComplaintScreen
from help import HelpScreen
from settings import SettingsScreen
from transaction import Transaction
from viewprofile import Profile
from Wallet import AddMoneyScreen
from loadingScreen import loadingScreen

navigation_helper = """
<DashBoardScreen>:
    MDNavigationLayout:
        MDScreenManager:
            MDScreen:
                MDBoxLayout:
                    orientation: "vertical"
                    size_hint_y :0.1
                    pos_hint:{"top":1}
                    #md_bg_color: "#fe5016"
                    
                    MDTopAppBar:
                        title: "[b][color=#ffffff]G WALLET[/color][/b]"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1
                        elevation: 1
                        pos_hint: {"center_y": 1}
                        md_bg_color: "#148EFE"
                        specific_text_color: "#000000"
                        elevation: 1
                        left_action_items:
                            [['menu', lambda x: nav_drawer.set_state("open")]]
                        right_action_items: [["account-circle", lambda x: print("Image Button Pressed")]] 
                    MDBoxLayout:
                        orientation: "vertical"                   
                MDBoxLayout:
                    orientation: "vertical"
                    size_hint_y: 0.1
                    pos_hint: {"top":0.9}
                    
                    
                    MDCard:
                        orientation: "vertical"
                        size_hint: None, None
                        size: "320dp", "30dp"
                        md_bg_color: "#C4E3FF"
                        radius: [dp(15), dp(15), dp(15), dp(15)]
                        pos_hint: {"center_y": 1, "center_x": 0.5}
                
                        MDLabel:
                            text: "Search in G Wallet"
                            theme_text_color: "Custom"  # Disable theme color
                            text_color: 0, 0, 0, 1
                            # size_hint_y:None
                            pos_hint: {"center_x": 0.8, "center_y": 0.5}
                            font_size: "15sp"
                            
                    MDBoxLayout:
                        orientation: "vertical"
                        size_hint: None, None
                        size: "320dp", "20dp"
                MDBoxLayout:
                    orientation: "vertical"
                    size_hint_y :0.5
                    pos_hint:{"top":0.8}
                    #md_bg_color: "#1650fe"
                    
                    MDBoxLayout:
                        orientation: "vertical"
                        pos_hint: {"center_x": 0.5,"center_y":0.5}
                        #md_bg_color: "#fe168a"
                        size_hint_y: 1
                        size_hint_x: 1
                        
                        
                        MDGridLayout:
                            cols: 3
                            rows: 3
                            spacing: dp(25)
                            size_hint: (None, None)  # Set size_hint to None
                            width: self.minimum_width  # Set width explicitly
                            height: self.minimum_height  # Set height explicitly
                            pos_hint: {"center_x": 0.5, "center_y": 0.5}
                            
                            
                            MDCard:
                                orientation: "vertical"
                                size_hint: None, None
                                size: "70dp", "70dp"
                                md_bg_color: "#ffffff"
                                radius: [dp(20), dp(20), dp(20), dp(20)]
                                pos_hint_y: None
                                pos_hint_x:  None
                                # elevation: 1 
                                on_release: root.nav_transfer()
                            
                                MDBoxLayout:
                                    orientation: "vertical"
                                    size_hint_y: None
                                    height: "70dp"
                                    spacing: dp(-12)
                                    
                                    Image:
                                        source: "images/money-transfer.png"
                                        size_hint: (0.3, 1)
                                        pos_hint:{"center_x":0.5,"center_y":0.2}
                                    
                                    MDLabel:
                                        text: "Transfer"
                                        color: 20/255, 142/255, 254/255,1
                                        font_size: "14sp"
                                        halign: "center"
                                        
                                        
                                    MDLabel:
                                        text: "Money"
                                        color: 20/255, 142/255, 254/255,1
                                        font_size: "14sp"
                                        halign: "center"
                                        
                            MDCard:
                                orientation: "vertical"
                                size_hint: None, None
                                size: "70dp", "70dp"
                                md_bg_color: "#ffffff"
                                radius: [dp(20), dp(20), dp(20), dp(20)]
                                pos_hint_y: None
                                pos_hint_x:  None
                                # elevation: 1
                                on_release: root.Add_Money()
                                MDBoxLayout:
                                    orientation: "vertical"
                                    size_hint_y: None
                                    height: "70dp"
                                    spacing: dp(-12)
                                    
                                    Image:
                                        source: "images/wallet.png"
                                        size_hint: (0.3, 1)
                                        pos_hint:{"center_x":0.5,"center_y":0.2}
                                    
                                    MDLabel:
                                        text: "Your"
                                        color: 20/255, 142/255, 254/255,1
                                        font_size: "14sp"
                                        halign: "center"
                                        
                                    MDLabel:
                                        text: "Wallet"
                                        color: 20/255, 142/255, 254/255,1
                                        font_size: "14sp"
                                        halign: "center"    
                            MDCard:
                                orientation: "vertical"
                                size_hint: None, None
                                size: "70dp", "70dp"
                                md_bg_color: "#ffffff"
                                radius: [dp(20), dp(20), dp(20), dp(20)]
                                pos_hint_y: None
                                pos_hint_x:  None 
                                # elevation: 1
                                on_release: root.nav_withdraw()       
                                MDBoxLayout:
                                    orientation: "vertical"
                                    size_hint_y: None
                                    height: "70dp"
                                    spacing: dp(-12)
                                    
                                    Image:
                                        source: "images/cash-withdrawal.png"
                                        size_hint: (0.3, 1)
                                        pos_hint:{"center_x":0.5,"center_y":0.2}
                                    
                                    MDLabel:
                                        text: "Withdraw"
                                        color: 20/255, 142/255, 254/255,1
                                        font_size: "14sp"
                                        halign: "center"
                                    MDLabel:
                                        text: "  Money"
                                        color: 20/255, 142/255, 254/255,1 
                                        font_size: "14sp" 
                                        halign: "center"  
                            MDCard:
                                orientation: "vertical"
                                size_hint: None, None
                                size: "70dp", "70dp"
                                md_bg_color: "#ffffff"
                                radius: [dp(20), dp(20), dp(20), dp(20)]
                                pos_hint_y: None
                                pos_hint_x:  None
                                # elevation: 1 
                                on_release: root.nav_addPhone()       
                                MDBoxLayout:
                                    orientation: "vertical"
                                    size_hint_y: None
                                    height: "70dp"
                                    spacing: dp(-12)
                                    
                                    Image:
                                        source: "images/phone.png"
                                        size_hint: (0.3, 1)
                                        pos_hint:{"center_x":0.5,"center_y":0.2}
                                    
                                    MDLabel:
                                        text: "Pay"
                                        color: 20/255, 142/255, 254/255,1
                                        font_size: "14sp"
                                        halign: "center"
                                        
                                    MDLabel:
                                        text: "contacts"
                                        color: 20/255, 142/255, 254/255,1 
                                        font_size: "14sp"
                                        halign: "center"   
                                    
                            MDCard:
                                orientation: "vertical"
                                size_hint: None, None
                                size: "70dp", "70dp"
                                md_bg_color: "#ffffff"
                                radius: [dp(20), dp(20), dp(20), dp(20)]
                                pos_hint_y: None
                                pos_hint_x:  None
                                # elevation: 1 
                                     
                                MDBoxLayout:
                                    orientation: "vertical"
                                    size_hint_y: None
                                    height: "70dp"
                                    spacing: dp(-12)
                                    
                                    Image:
                                        source: "images/topup.png"
                                        size_hint: (0.3, 1)
                                        pos_hint:{"center_x":0.5,"center_y":0.2}
                                    
                                    MDLabel:
                                        text: "Auto"
                                        color: 20/255, 142/255, 254/255,1
                                        font_size: "14sp"
                                        halign: "center"
                                    MDLabel:
                                        text: "Topup"
                                        color: 20/255, 142/255, 254/255,1 
                                        font_size: "14sp"
                                        halign: "center"   
                            MDCard:
                                orientation: "vertical"
                                size_hint: None, None
                                size: "70dp", "70dp"
                                md_bg_color: "#ffffff"
                                radius: [dp(20), dp(20), dp(20), dp(20)]
                                pos_hint_y: None
                                pos_hint_x:  None
                                # elevation: 1 
                                on_release: root.bank_account()         
                                MDBoxLayout:
                                    orientation: "vertical"
                                    size_hint_y: None
                                    height: "70dp"
                                    spacing: dp(-12)
                                    
                                    Image:
                                        source: "images/museum.png"
                                        size_hint: (0.3, 1)
                                        pos_hint:{"center_x":0.5,"center_y":0.2}
                                    
                                    MDLabel:
                                        text: "Bank"
                                        color: 20/255, 142/255, 254/255,1
                                        font_size: "14sp"
                                        halign: "center"
                                        
                                    MDLabel:
                                        text: "Accounts"
                                        color: 20/255, 142/255, 254/255,1
                                        font_size: "14sp"
                                        halign: "center"    
                            MDCard:
                                orientation: "vertical"
                                size_hint: None, None
                                size: "70dp", "70dp"
                                md_bg_color: "#ffffff"
                                radius: [dp(20), dp(20), dp(20), dp(20)]
                                pos_hint_y: None
                                pos_hint_x:  None
                                # elevation: 1
                                on_release: root.nav_transfer()  
                                MDBoxLayout:
                                    orientation: "vertical"
                                    size_hint_y: None
                                    height: "70dp"
                                    spacing: dp(-12)
                                    
                                    Image:
                                        source: "images/self-transfer.png"
                                        size_hint: (0.3, 1)
                                        pos_hint:{"center_x":0.5,"center_y":0.2}
                                    
                                    MDLabel:
                                        text: "Self"
                                        color: 20/255, 142/255, 254/255,1
                                        font_size: "14sp"
                                        halign: "center"
                                        
                                    MDLabel:
                                        text: "Transfer"
                                        color: 20/255, 142/255, 254/255,1
                                        font_size: "14sp"
                                        halign: "center"   
                                    
                            MDCard:
                                orientation: "vertical"
                                size_hint: None, None
                                size: "70dp", "70dp"
                                md_bg_color: "#ffffff"
                                radius: [dp(20), dp(20), dp(20), dp(20)]
                                pos_hint_y: None
                                pos_hint_x:  None
                                # elevation: 1        
                                MDBoxLayout:
                                    orientation: "vertical"
                                    size_hint_y: None
                                    height: "70dp"
                                    spacing: dp(-12)
                                    
                                    Image:
                                        source: "images/refer.png"
                                        size_hint: (0.3, 1)
                                        pos_hint:{"center_x":0.5,"center_y":0.2}
                                    
                                    MDLabel:
                                        text: "Refer a"
                                        color: 20/255, 142/255, 254/255,1
                                        font_size: "14sp"
                                        halign: "center"
                                        
                                    MDLabel:
                                        text: "friend"
                                        color: 20/255, 142/255, 254/255,1 
                                        font_size: "14sp"
                                        halign: "center"   
                                    
                            MDCard:
                                orientation: "vertical"
                                size_hint: None, None
                                size: "70dp", "70dp"
                                md_bg_color: "#ffffff"
                                radius: [dp(20), dp(20), dp(20), dp(20)]
                                pos_hint_y: None
                                pos_hint_x:  None
                                # elevation: 1        
                                MDBoxLayout:
                                    orientation: "vertical"
                                    size_hint_y: None
                                    height: "70dp"
                                    spacing: dp(-12)
                                    
                                    Image:
                                        source: "images/scanner.png"
                                        size_hint: (0.3, 1)
                                        pos_hint:{"center_x":0.5,"center_y":0.2}
                                    
                                    MDLabel:
                                        text: "Scan a"
                                        color: 20/255, 142/255, 254/255,1
                                        font_size: "14sp"
                                        halign: "center"
                                    MDLabel:
                                        text: "QR Code"
                                        color: 20/255, 142/255, 254/255,
                                        font_size: "14sp" 
                                        halign: "center"
                    
                        MDBoxLayout:
                            orientation: "vertical"
                            #md_bg_color: "#fefe16"
                            
                MDBoxLayout:
                    orientation: "vertical"
                    size_hint_y :0.4
                    pos_hint:{"center_y":0.12}
                    md_bg_color: "#C4E3FF"
                    spacing: dp(-10)
                    
                    MDBoxLayout:
                        orientation: "vertical"
                        size_hint_y :0.28
                        pos_hint:{"center_y":1}
                
                        MDCard:
                            orientation: "horizontal"
                            size_hint_y :0.1
                            md_bg_color: "#C4E3FF"
                            on_release: root.generate_qr_code()  
                            Image:
                                source: "images/qr-code.png"
                                size_hint: (0.5, 0.5)
                                pos_hint:{"center_x":0.1}
                                
                            MDLabel:
                                text: "Receive money from QR code"
                                theme_text_color: "Custom"  # Disable theme color
                                text_color: 0, 0, 0, 1
                                font_size: "13sp"
                                pos_hint:{"center_y":0.25}
                            Image:
                                source: "images/right-chevron.png"
                                size_hint: (0.4, 0.4)        
                        MDCard:
                            orientation: "horizontal"
                            size_hint_y :0.1
                            md_bg_color: "#C4E3FF"
                            on_release: root.go_to_transaction()  
                            Image:
                                source: "images/history.png"
                                size_hint: (0.5, 0.5)
                                
                            MDLabel:
                                text: "See transaction history"
                                theme_text_color: "Custom"  # Disable theme color
                                text_color: 0, 0, 0, 1
                                font_size: "13sp"
                                pos_hint:{"center_y":0.25}
                            Image:
                                source: "images/right-chevron.png"
                                size_hint: (0.4, 0.4)    
                        MDCard:
                            orientation: "horizontal"
                            size_hint_y :0.1
                            md_bg_color: "#C4E3FF"
                            Image:
                                source: "images/balance.png"
                                size_hint: (0.5, 0.5)
                            MDLabel:
                                text: "Check balance"
                                theme_text_color: "Custom"  # Disable theme color
                                text_color: 0, 0, 0, 1
                                font_size: "13sp"
                                pos_hint:{"center_y":0.25}
                            Image:
                                source: "images/right-chevron.png"
                                size_hint: (0.4, 0.4)    
                        MDCard:
                            orientation: "horizontal"
                            size_hint_y :0.1
                            md_bg_color: "#C4E3FF"
                            on_release: root.nav_settings()  
                            Image:
                                source: "images/setting.png"
                                size_hint: (0.5, 0.5)
                                
                            MDLabel:
                                text: "Settings"
                                theme_text_color: "Custom"  # Disable theme color
                                text_color: 0, 0, 0, 1
                                font_size: "13sp"
                                pos_hint:{"center_y":0.25}
                            Image:
                                source: "images/right-chevron.png"
                                size_hint: (0.4, 0.4)    
                    MDBoxLayout:
                        orientation: "vertical" 
                        size_hint_y:0.12     
                                                                                                                                                  
        MDNavigationDrawer:
            id: nav_drawer
            radius: (0, 10, 10, 0)
            #md_bg_color: "#148EFE"
            padding: 0 
            spacing: 0
            ContentNavigationDrawer:
                MDBoxLayout:
                    orientation: "vertical"
                    #md_bg_color: "#148EFE"
                    
                    MDBoxLayout: #for user information
                        orientation: "horizontal"
                        md_bg_color: "#148EFE"
                        size_hint_y: 0.2
                        pos_hint: {"top":1}
                        
                        MDBoxLayout: # for labels
                            orientation: "vertical"
                            #md_bg_color: "#fe1616"
                            size_hint_x: 0.6
                            
                            MDLabel:
                                text: "[b]your name[/b]"
                                id:username_label
                                markup: True
                                theme_text_color: "Custom"  # Disable theme color
                                text_color: 1, 1, 1, 1
                                font_size: "15sp"
                                pos_hint:{"center_x":0.7}
                            MDLabel:
                                text: "[b]Email[/b]"
                                id:email_label
                                markup: True
                                theme_text_color: "Custom"  # Disable theme color
                                text_color: 1, 1, 1, 1
                                font_size: "15sp"
                                pos_hint:{"center_x":0.7}
                            MDLabel:
                                text: "[b]phone number[/b]"
                                id:contact_label
                                markup: True
                                theme_text_color: "Custom"  # Disable theme color
                                text_color: 1, 1, 1, 1
                                font_size: "15sp"
                                pos_hint:{"center_x":0.7}        
                        MDBoxLayout: # for labels
                            orientation: "vertical"
                            #md_bg_color: "#5016fe"
                            size_hint_x: 0.4    
                            Image:
                                source: "images/user.png"
                                size_hint: (0.5, 0.5)
                                pos_hint:{"center_x":0.5,"center_y":0.3}
                                
                            
                    MDBoxLayout: #for features
                        orientation: "vertical"
                        size_hint_y: 0.6
                        pos_hint: {"top":0.8}
                        
                        MDCard:
                            orientation: "horizontal"
                            size_hint_y :0.1
                            on_release: root.generate_qr_code()
                            Image:
                                source: "images/qr-code.png"
                                size_hint: (0.4, 0.4)
                                pos_hint:{"center_x":0.1}
                            MDLabel:
                                text: "Your QR code"
                                theme_text_color: "Custom"  # Disable theme color
                                text_color: 0, 0, 0, 1
                                font_size: "15sp"
                                pos_hint:{"center_y":0.2} 
                      
                        MDCard:
                            orientation: "horizontal"
                            size_hint_y :0.1
                            Image:
                                source: "images/topup.png"
                                size_hint: (0.4, 0.4)
                                pos_hint:{"center_x":0.1}
                            MDLabel:
                                text: "Auto topup"
                                theme_text_color: "Custom"  # Disable theme color
                                text_color: 0, 0, 0, 1
                                font_size: "15sp"
                                pos_hint:{"center_y":0.2}   
                        MDCard:
                            orientation: "horizontal"
                            size_hint_y :0.1
                            on_release: root.nav_settings()  
                            Image:
                                source: "images/setting.png"
                                size_hint: (0.4, 0.4)
                                pos_hint:{"center_x":0.1}
                            MDLabel:
                                text: "Settings"
                                theme_text_color: "Custom"  # Disable theme color
                                text_color: 0, 0, 0, 1
                                font_size: "15sp"
                                pos_hint:{"center_y":0.2}         
                        MDCard:
                            orientation: "horizontal"
                            size_hint_y :0.1
                            on_release: root.profile_view()
                            Image:
                                source: "images/account.png"
                                size_hint: (0.4, 0.4)
                                pos_hint:{"center_x":0.1}
                            MDLabel:
                                text: "Manage account"
                                theme_text_color: "Custom"  # Disable theme color
                                text_color: 0, 0, 0, 1
                                font_size: "15sp"
                                pos_hint:{"center_y":0.2}        
                        MDCard:
                            orientation: "horizontal"
                            size_hint_y :0.1
                            on_release: root.nav_help()
                            Image:
                                source: "images/help.png"
                                size_hint: (0.4, 0.4)
                                pos_hint:{"center_x":0.1}
                            MDLabel:
                                text: "Get help"
                                theme_text_color: "Custom"  # Disable theme color
                                text_color: 0, 0, 0, 1
                                font_size: "15sp"
                                pos_hint:{"center_y":0.2} 
                                
                        MDCard:
                            orientation: "horizontal"
                            size_hint_y :0.1
                            on_release: root.nav_complaint()
                            Image:
                                source: "images/report.png"
                                size_hint: (0.4, 0.4)
                                pos_hint:{"center_x":0.1}
                            MDLabel:
                                text: "Raise a complaint"
                                theme_text_color: "Custom"  # Disable theme color
                                text_color: 0, 0, 0, 1
                                font_size: "15sp"
                                pos_hint:{"center_y":0.2}
                                
                        MDCard:
                            orientation: "horizontal"
                            size_hint_y :0.1
                            on_release: root.manager.logout()
                            Image:
                                source: "images/logout.png"
                                size_hint: (0.4, 0.4)
                                pos_hint:{"center_x":0.1}
                            MDLabel:
                                text: "Logout"
                                theme_text_color: "Custom"  # Disable theme color
                                text_color: 0, 0, 0, 1
                                font_size: "15sp"
                                pos_hint:{"center_y":0.2}         
                    MDBoxLayout:
                        orientation:"vertical"
                        size_hint_y: 0.15
                        #md_bg_color: "#fefe16"
                           
"""
Builder.load_string(navigation_helper)


class BottomAppBar(FloatLayout):
    pass


class MDCardBoxLayout(BoxLayout):
    pass


class ContentNavigationDrawer(MDBoxLayout):
    pass


class DashBoardScreen(Screen):
    def get_username(self):
        store = JsonStore('user_data.json').get('user')['value']
        return store["username"]

    def nav_addPhone(self):
        self.manager.add_widget(Factory.loadingScreen(name='loading'))
        self.manager.current = "loading"
        Clock.schedule_once(lambda dt: self.show_addphone_screen(), 2)

    def show_addphone_screen(self):
        self.manager.add_widget(Factory.AddPhoneScreen(name='addphone'))
        self.manager.current = 'addphone'

    def fetch_and_update_addPhone(self):
        store = JsonStore('user_data.json').get('user')['value']
        # Update labels in ComplaintScreen
        addPhone_screen = self.get_screen('addPhone')
        addPhone_screen.ids.contact_label.text = store["phone"]

    def profile_view(self):
        store = JsonStore('user_data.json').get('user')['value']
        username = store["username"]
        gmail = store["email"]
        phone = store["phone"]
        aadhaar = store["aadhar"]
        address = store["address"]
        pan = store["pan"]
        self.manager.add_widget(Factory.Profile(name='profile'))
        profile_screen = self.manager.get_screen('profile')
        profile_screen.ids.username_label.text = f"Username:{username}"  # Assuming username is at index 1
        profile_screen.ids.email_label.text = f"Email:{gmail}"  # Assuming email is at index 0
        profile_screen.ids.contact_label.text = f"Mobile No:{phone}"
        profile_screen.ids.aadhaar_label.text = f"Aadhar:{aadhaar}"
        profile_screen.ids.pan_label.text = f"Pan no:{pan}"
        profile_screen.ids.address_label.text = f"Address:{address}"
        self.manager.add_widget(Factory.Profile(name='profile'))
        # Navigate to the 'Profile' screen
        self.manager.current = 'profile'

    def account_details_exist(self, phone):
        try:
            return app_tables.wallet_users_account.search(phone=phone)  # Returns a list of accounts
        except Exception as e:
            print(f"Error fetching accounts: {e}")
            return False

    def nav_withdraw(self):
        self.manager.add_widget(Factory.loadingScreen(name='loading'))
        self.manager.current = "loading"
        phone = JsonStore('user_data.json').get('user')['value']["phone"]
        account_details = self.account_details_exist(phone)
        if account_details:
            Clock.schedule_once(lambda dt: self.show_withdraw_screen(), 2)

        else:
            self.show_add_account_dialog()

    def show_withdraw_screen(self):
        self.manager.add_widget(Factory.WithdrawScreen(name='withdraw'))
        self.manager.current = 'withdraw'

    def nav_transfer(self):
        self.manager.add_widget(Factory.loadingScreen(name='loading'))
        self.manager.current = "loading"
        phone = JsonStore('user_data.json').get('user')['value']["phone"]
        account_details = self.account_details_exist(phone)
        if account_details:
            Clock.schedule_once(lambda dt: self.show_transfer_screen(), 2)

        else:
            self.show_add_account_dialog()

    def show_transfer_screen(self):
        self.manager.add_widget(Factory.TransferScreen(name='transfer'))
        self.manager.current = 'transfer'

    def show_add_account_dialog(self):
        dialog = MDDialog(
            title="Bank Account Not Found",
            text="You don't have a bank account associated with your phone number. "
                 "Would you like to add a bank account?",
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    on_release=lambda *args: (dialog.dismiss(), setattr(self.manager, 'current', 'dashboard'))),
                MDFlatButton(
                    text="OK",
                    on_release=lambda *args:
                    (dialog.dismiss(), setattr(self.manager, 'current', 'addaccount'))),
            ],
        )
        dialog.open()

    def go_to_transaction(self):
        self.on_start()
        Clock.schedule_once(lambda dt: self.show_transaction_screen(), 2)

    def show_transaction_screen(self):
        self.manager.add_widget(Factory.Transaction(name='transaction'))
        self.manager.current = 'transaction'

    def on_start(self):
        self.manager.add_widget(Factory.loadingScreen(name='loading'))
        self.manager.current = "loading"
        self.get_transaction_history()

    def get_transaction_history(self):
        try:
            # Get the phone number from the JSON file
            store = JsonStore('user_data.json').get('user')['value']
            phone = store['phone']
            # Query the 'transactions' table to fetch the transaction history
            transactions = list(app_tables.wallet_users_transaction.search(phone=phone))
            self.manager.add_widget(Factory.Transaction(name='transaction'))
            trans_screen = self.manager.get_screen('transaction')
            trans_screen.ids.transaction_list.clear_widgets()

            current_date = ""

            for transaction in sorted(filter(lambda x: x['date'] is not None, transactions), key=lambda x: x['date'],
                                      reverse=True):
                transaction_datetime = transaction['date']
                transaction_date_str = transaction_datetime.strftime('%Y-%m-%d')
                transaction_date = transaction_date_str.split(' ')[0]
                transactions_text = f"{transaction['receiver_phone']}"
                fund_text = f"{transaction['fund']}"

                if transaction_date != current_date:
                    current_date = transaction_date
                    header_text = f"[b]{transaction_date}[/b]"
                    trans_screen.ids.transaction_list.add_widget(
                        OneLineListItem(text=header_text, theme_text_color='Custom', text_color=[0, 0, 0, 1]))

                transaction_container = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(36))

                # Add transaction details
                transaction_label = MDLabel(text=f"{transactions_text}", theme_text_color='Custom',
                                            text_color=[0, 0, 0, 1], halign='left', padding=(15, 15))
                transaction_container.add_widget(transaction_label)

                transaction_container.add_widget(Widget(size_hint_x=None, width=dp(20)))

                if transaction['transaction_type'] == 'Credit':
                    fund_color = [0, 0.5, 0, 1]
                    sign = '+'
                else:
                    fund_color = [1, 0, 0, 1]
                    sign = '-'

                fund_label = MDLabel(text=f"{sign}₹{fund_text}", theme_text_color='Custom', text_color=fund_color,
                                     halign='right', padding=(15, 15))
                transaction_container.add_widget(fund_label)

                trans_screen.ids.transaction_list.add_widget(transaction_container)
        except Exception as e:
            print(f"Error getting transaction history: {e} ,{traceback.format_exc()}")

    menu = None  # Add this line to declare the menu attribute
    options_button_icon_mapping = {
        "INR": "currency-inr",
        "GBP": "currency-gbp",
        "USD": "currency-usd",
        "EUR": "currency-eur"
    }

    def show_currency_options(self, button):
        currency_options = ["INR", "GBP", "USD", "EUR"]
        self.menu_list = [
            {"viewclass": "OneLineListItem", "text": currency, "on_release": lambda x=currency: self.menu_callback(x)}
            for currency in currency_options
        ]

        # Create and open the dropdown menu
        self.menu = MDDropdownMenu(
            caller=button,
            items=self.menu_list,
            width_mult=4
        )
        self.menu.open()

    def menu_callback(self, instance_menu_item):
        print(f"Selected currency: {instance_menu_item}")
        store = JsonStore('user_data.json')
        phone_no = store.get('user')['value']["phone"]
        total_balance = self.manager.get_total_balance(phone_no, instance_menu_item)
        # Convert the total balance to the selected currency

        self.ids.balance_lbl.text = f'balance: {total_balance} '
        print(total_balance)
        self.ids.options_button.icon = self.options_button_icon_mapping.get(instance_menu_item, "currency-inr")
        self.menu.dismiss()

    def convert_currency(self, amount, to_currency):
        # Implement your currency conversion logic here
        # You may use an external API or a predefined exchange rate table

        # For simplicity, let's assume a basic conversion formula
        exchange_rate = {
            "USD": 0.014,  # Example exchange rates, replace with actual rates
            "EUROS": 0.012,
            "INR": 1.0,
            "POUND": 0.011
        }

        converted_amount = amount * exchange_rate.get(to_currency, 1.0)
        return round(converted_amount, 2)  # Round to two decimal places

    def generate_qr_code(self):
        phone = JsonStore('user_data.json').get('user')['value']["phone"]
        qr_code = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr_code.add_data(phone)
        qr_code.make(fit=True)

        img = qr_code.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        png_data = buffer.getvalue()
        self.show_qr(png_data)

    def show_qr(self, png_data):
        qr_code_popup = Popup(title='Your QR Code', size_hint=(0.8, 0.8))
        qr_code_image = Image()
        qr_code_image.source = 'data:image/png;base64,' + base64.b64encode(png_data).decode('utf-8')
        qr_code_popup.add_widget(qr_code_image)
        qr_code_popup.open()

    def nav_addContact(self):
        self.manager.current = 'addcontact'

    def Add_Money(self):
        self.manager.add_widget(Factory.loadingScreen(name='loading'))
        self.manager.current = "loading"
        Clock.schedule_once(lambda dt: self.show_addmoney_screen(), 2)

    def show_addmoney_screen(self):
        self.manager.add_widget(Factory.AddMoneyScreen(name='Wallet'))
        self.manager.current = 'Wallet'

    def bank_account(self):
        self.manager.add_widget(Factory.loadingScreen(name='loading'))
        self.manager.current = "loading"
        Clock.schedule_once(lambda dt: self.show_bankaccount_screen(), 2)

    def show_bankaccount_screen(self):
        self.manager.add_widget(Factory.AccmanageScreen(name='accmanage'))
        self.manager.current = 'accmanage'

    def nav_settings(self):
        self.manager.add_widget(Factory.loadingScreen(name='loading'))
        self.manager.current = "loading"
        Clock.schedule_once(lambda dt: self.show_settings_screen(), 2)

    def show_settings_screen(self):
        self.manager.add_widget(Factory.SettingsScreen(name='settings'))
        self.manager.current = 'settings'

    def nav_help(self):
        self.manager.add_widget(Factory.loadingScreen(name='loading'))
        self.manager.current = "loading"
        Clock.schedule_once(lambda dt: self.show_help_screen(), 2)

    def show_help_screen(self):
        self.manager.add_widget(Factory.HelpScreen(name='help'))
        self.manager.current = "help"

    def nav_complaint(self):
        self.manager.add_widget(Factory.loadingScreen(name='loading'))
        self.manager.current = "loading"
        Clock.schedule_once(lambda dt: self.show_complaint_screen(), 2)

    def show_complaint_screen(self):
        self.manager.add_widget(Factory.ComplaintScreen(name='complaint'))
        self.manager.current = "complaint"
