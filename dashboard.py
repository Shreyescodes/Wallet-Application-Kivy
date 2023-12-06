from kivy.properties import ListProperty, StringProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.floatlayout import FloatLayout
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import HoverBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.window import Window
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.navigationdrawer import MDNavigationLayout
from kivymd.uix.screen import Screen
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
Window.size = (300, 500)

navigation_helper = """
<DashBoardScreen>:
    Screen:
        MDNavigationLayout:
            MDScreenManager:
                MDScreen:
                    BottomAppBar:
                        MDBottomNavigation:
                            spacing:dp(10)
                            panel_color:get_color_from_hex("#3489eb")
                            text_color_active:get_color_from_hex("F5F5F5")
                            MDBottomNavigationItem:
                                name:"Withdraw"
                                text:'Withdraw'
                                font_size: '20sp'
                                icon:'bank-transfer-out'
                                on_tab_release:root.manager.nav_withdraw()
                            MDBottomNavigationItem:
                                name:"Withdraw"
                                text:'Transfer'
                                text_size: dp(1)
                                icon:'bank-transfer-in'
                                on_tab_release:root.manager.nav_transfer()
                            MDBottomNavigationItem:
                                name:"Withdraw"
                                text:'Add Money'
                                text_size:dp(8)
                                icon:'wallet-plus'
                                on_tab_release: root.manager.nav_topup()
                    MDTopAppBar:
                        title: "G-Wallet"
                        elevation: 4
                        pos_hint: {"top": 1}
                        md_bg_color: "#3489eb"
                        specific_text_color: "F5F5F5"
                        left_action_items:
                            [['menu', lambda x: nav_drawer.set_state("open")]]


                    #Main page

                    BoxLayout:
                        orientation: 'vertical'
                        spacing:dp(20)
                        padding: dp(10)
                        pos_hint:{'center_y':.37}

                        GridLayout:
                            #spacing:dp(100)
                            #padding:dp(5)
                            cols: 3
                            spacing:dp(20)
                            rows:4



                            # Icon and label for recharge prepaid mobile
                            BoxLayout:

                                spacing: dp(10)
                                orientation: 'vertical'
                                size_hint_y: None
                                height: self.minimum_height
                                width:20

                                MDIconButton:
                                    icon: 'cellphone-wireless'
                                    pos_hint: {'center_x': 0.5}
                                    on_release: app.recharge_prepaid_mobile()  # Replace with your actual function
                                    padding: dp(20)

                                MDLabel:
                                    text: 'Recharge Prepaid Mobile'
                                    halign: 'center'
                                    font_size: '10sp'

                            # Icon and label for pay electricity bill
                            BoxLayout:

                                spacing: dp(10)
                                orientation: 'vertical'
                                size_hint_y: None
                                height: self.minimum_height

                                MDIconButton:
                                    icon: 'flash'
                                    pos_hint: {'center_x': 0.5}
                                    on_release: app.pay_electricity_bill()  # Replace with your actual function
                                    padding: dp(20)

                                MDLabel:
                                    text: 'Pay Electricity Bill'
                                    halign: 'center'
                                    font_size: '10sp'

                            # Icon and label for recharge DTH connection
                            BoxLayout:

                                spacing: dp(10)
                                orientation: 'vertical'
                                size_hint_y: None
                                height: self.minimum_height

                                MDIconButton:
                                    icon: 'satellite-variant'
                                    pos_hint: {'center_x': 0.5}
                                    on_release: app.recharge_dth_connection()  # Replace with your actual function
                                    padding: dp(20)

                                MDLabel:
                                    text: 'Recharge DTH Connection'
                                    halign: 'center'
                                    font_size: '10sp'

                            # Icon and label for book gas cylinder
                            BoxLayout:

                                spacing: dp(10)
                                orientation: 'vertical'
                                size_hint_y: None
                                height: self.minimum_height

                                MDIconButton:
                                    icon: 'gas-cylinder'
                                    pos_hint: {'center_x': 0.5}
                                    on_release: app.book_gas_cylinder()  # Replace with your actual function
                                    padding: dp(20)

                                MDLabel:
                                    text: 'Book Gas Cylinder'
                                    halign: 'center'
                                    font_size: '10sp'

                             # Icon and label for pay broadband & landline bill
                            BoxLayout:
                                spacing: dp(10)
                                orientation: 'vertical'
                                size_hint_y: None
                                height: self.minimum_height

                                MDIconButton:
                                    icon: 'router-wireless'
                                    pos_hint: {'center_x': 0.5}
                                    on_release: app.pay_broadband_landline_bill()  # Replace with your actual function
                                    padding: dp(20)

                                MDLabel:
                                    text:  'Broadband & Landline Bill'
                                    halign: 'center'
                                    font_size: '10sp'

                            # Icon and label for pay education fee
                            BoxLayout:
                                spacing: dp(10)
                                orientation: 'vertical'
                                size_hint_y: None
                                height: self.minimum_height

                                MDIconButton:
                                    icon: 'school'
                                    pos_hint: {'center_x': 0.5}
                                    on_release: app.pay_education_fee()  # Replace with your actual function
                                    padding: dp(20)

                                MDLabel:
                                    text: 'Pay Education Fee'
                                    halign: 'center'
                                    font_size: '10sp'        




                            # Icon and label for Movies Tickets
                            BoxLayout:
                                spacing: dp(10)
                                orientation: 'vertical'
                                size_hint_y: None
                                height: self.minimum_height
                                width: 20

                                MDIconButton:
                                    icon: 'movie'
                                    pos_hint: {'center_x': 0.5}
                                    on_release: app.book_movies_tickets()  # Replace with your actual function
                                    padding: dp(20)

                                MDLabel:
                                    text: 'Movies Tickets'
                                    halign: 'center'
                                    font_size: '10sp'

                            # Icon and label for Flight Tickets
                            BoxLayout:
                                spacing: dp(10)
                                orientation: 'vertical'
                                size_hint_y: None
                                height: self.minimum_height

                                MDIconButton:
                                    icon: 'airplane'
                                    pos_hint: {'center_x': 0.5}
                                    on_release: app.book_flight_tickets()  # Replace with your actual function
                                    padding: dp(20)

                                MDLabel:
                                    text: 'Flight Tickets'
                                    halign: 'center'
                                    font_size: '10sp'

                            # Icon and label for Bus Tickets
                            BoxLayout:
                                spacing: dp(10)
                                orientation: 'vertical'
                                size_hint_y: None
                                height: self.minimum_height

                                MDIconButton:
                                    icon: 'bus'
                                    pos_hint: {'center_x': 0.5}
                                    on_release: app.book_bus_tickets()  # Replace with your actual function
                                    padding: dp(20)

                                MDLabel:
                                    text: 'Bus Tickets'
                                    halign: 'center'
                                    font_size: '10sp'

                            # Icon and label for Train Tickets
                            BoxLayout:
                                spacing: dp(10)
                                orientation: 'vertical'
                                size_hint_y: None
                                height: self.minimum_height

                                MDIconButton:
                                    icon: 'train'
                                    pos_hint: {'center_x': 0.5}
                                    on_release: app.book_train_tickets()  # Replace with your actual function
                                    padding: dp(20)

                                MDLabel:
                                    text: 'Train Tickets'
                                    halign: 'center'
                                    font_size: '10sp'

                            # Icon and label for Buy Insurance
                            BoxLayout:
                                spacing: dp(10)
                                orientation: 'vertical'
                                size_hint_y: None
                                height: self.minimum_height

                                MDIconButton:
                                    icon: 'shield-check'
                                    pos_hint: {'center_x': 0.5}
                                    on_release: app.buy_insurance()  # Replace with your actual function
                                    padding: dp(20)

                                MDLabel:
                                    text: 'Buy Insurance'
                                    halign: 'center'
                                    font_size: '10sp'

                            # Icon and label for International Flights
                            BoxLayout:
                                spacing: dp(10)
                                orientation: 'vertical'
                                size_hint_y: None
                                height: self.minimum_height

                                MDIconButton:
                                    icon: 'earth'
                                    pos_hint: {'center_x': 0.5}
                                    on_release: app.book_international_flights()  # Replace with your actual function
                                    padding: dp(20)

                                MDLabel:
                                    text: 'International Flights'
                                    halign: 'center'
                                    font_size: '10sp'



            MDNavigationDrawer:
                id: nav_drawer
                radius: (0, 10, 10, 0)

                ContentNavigationDrawer:

                    BoxLayout:
                        size: root.width, root.height
                        spacing: '12dp'
                        padding: '8dp'
                        orientation: "vertical"
                        pos_hint:{'top':1}

                        MDLabel:
                            id: username_label
                            text:''
                            font_style:"Subtitle1"
                            size_hint_y:None
                            height: self.texture_size[1]


                        MDLabel:
                            id: email_label
                            text:''
                            font_style:"Caption" 
                            size_hint_y:None
                            height: self.texture_size[1]


                        BoxLayout:
                            orientation: "vertical"
                            padding: 20
                            pos_hint:{'center_x':0.44}

                            MDCard:
                                radius: [50, 50, 50, 50]
                                orientation: 'vertical'
                                size_hint: 1, 0.4
                                height: self.minimum_height
                                md_bg_color: 0.9, 0.9, 0.9, 1
                        
                                # BoxLayout:
                                #     size_hint_y: None
                                #     height: "40dp"
                                #     padding: "8dp"
                                # 
                                #     MDLabel:
                                #         text: 'e-wallet'
                                #         theme_text_color: 'Primary'
                                #         halign: 'left'
                                #         valign: 'center'
                        
                                BoxLayout:
                                    padding: "20dp"
                                    orientation: 'horizontal'
                                    spacing: "10dp"
                                    
                                    MDLabel:
                                        id:balance_lbl
                                        text: 'Balance'
                                        theme_text_color: 'Secondary'
                                        pos_hint: {'center_y':0.5}
                                        font_size: self.width / 9  # Adjust the font size based on the width of the card
                                        bold: True
                                        halign: 'center'
                        
                                    MDIconButton:
                                        id: options_button
                                        icon: "currency-btc"
                                        on_release: root.show_currency_options(self)
                                        pos_hint: {'center_y':0.5}
                                        md_bg_color: 0.7, 0.7, 0.7, 1  # Blue background color
                                        theme_text_color: "Custom"
                                        text_color: 0, 0, 0, 1  # White text color
                                        
                                        




                        BoxLayout: 
                            size_hint_y: None
                            height: dp(250)
                            pos_hint: {'center_x': 0.45, 'y': 130}        

                            BoxLayout:
                                orientation: "vertical"
                                size_hint_y: None
                                height: self.minimum_height
                                spacing: '8dp'

                                OneLineIconListItem:
                                    text: "Profile"
                                    on_release: root.manager.profile_view()
                                    IconLeftWidget:
                                        icon: "face-man-profile" 


                                OneLineIconListItem:
                                    text: "Transaction History"
                                    on_release:root.manager.go_to_transaction()
                                    IconLeftWidget:
                                        icon: "history"

                                OneLineIconListItem:
                                    text: "Add Bank Account"
                                    on_release: root.manager.nav_account()
                                    IconLeftWidget:
                                        icon: "bank"

                                OneLineIconListItem:
                                    text: "Business"
                                    IconLeftWidget:
                                        icon: "account"        

                                OneLineIconListItem:
                                    text: "Log-out"
                                    on_release: root.manager.logout()
                                    IconLeftWidget:
                                        icon: "logout"        

"""
Builder.load_string(navigation_helper)


class BottomAppBar(FloatLayout):
    pass


class ContentNavigationDrawer(MDBoxLayout):
    pass


class DashBoardScreen(Screen):
    def show_currency_options(self, button):
        currency_options = ["INR", "POUND", "USD", "EUROS"]
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
        phone_no = store.get('user')['value'][3]
        total_balance = self.manager.get_total_balance(phone_no)
        # Convert the total balance to the selected currency
        converted_balance = self.convert_currency(total_balance, instance_menu_item)

        # Update the label with the selected currency and converted balance
        self.ids.balance_lbl.text = f'{converted_balance} {instance_menu_item}'
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


class WalletApp(MDApp):
    pass


if __name__ == '__main__':
    WalletApp().run()
