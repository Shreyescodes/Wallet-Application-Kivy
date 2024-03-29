from logging import root
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.lang import Builder
from kivymd.uix.screen import Screen
from kivy.metrics import dp
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.list import TwoLineAvatarIconListItem
from anvil.tables import app_tables
from kivymd.uix.spinner import MDSpinner
from addAccount import AddAccountScreen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import IconRightWidget
from kivy.properties import DictProperty
KV = '''
<AccmanageScreen>:
    BoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "Account Management"
            left_action_items: [['arrow-left', lambda x: root.go_back()]]
            right_action_items: [["bank",lambda x: root.nav_account()]]
            elevation:4
        ScrollView:
            GridLayout:
                cols: 1
                spacing: dp(10)
                size_hint_y: None
                height: self.minimum_height
                id: account_details_container
                
        MDBottomAppBar:
            MDTopAppBar:
                mode: 'end'
                type: 'bottom'
                icon: 'bank'
                on_action_button: root.nav_account()        
'''
Builder.load_string(KV)


class AccmanageScreen(Screen):
    def go_back(self):
        existing_screen = self.manager.get_screen('accmanage')
        self.manager.current = 'dashboard'
        self.manager.remove_widget(existing_screen)


    def on_pre_enter(self, *args):
        # Called before the screen is displayed, show loading animation
        self.show_loading_animation()
        # Use Clock.schedule_once to simulate loading and update details after a delay
        Clock.schedule_once(lambda dt: self.update_details(), 2)

    def show_loading_animation(self):
        # Create and add an MDSpinner to the layout
        self.loading_spinner = MDSpinner(
            size_hint=(None, None),  # Use relative sizing for better scaling
            size=(dp(46), dp(46)),  # Adjust size as needed
            pos=(Window.width / 2 - dp(46) / 2, Window.height / 2 - dp(46) / 2)
        )
        self.ids.account_details_container.add_widget(self.loading_spinner)

    def hide_loading_animation(self):
        # Remove the loading MDSpinner from the layout
        self.ids.account_details_container.remove_widget(self.loading_spinner)

    def nav_account(self):
        self.manager.add_widget(Factory.AddAccountScreen(name='addaccount'))
        self.manager.current = 'addaccount'

    """while creating widgets dynamically cannot access ids as they wont be present in self.ids instead create a dictionary
        and store it in this scenario its dynamic_ids """
    dynmaic_ids = DictProperty({})
    def update_details(self):
        try:
            store = JsonStore('user_data.json')
            phone = store.get('user')['value']["phone"]

            # Call the server function to fetch account details and bank names
            bank_names = app_tables.wallet_users_account.search(phone=phone)
            bank_names_str = [str(row['bank_name']) for row in bank_names]
            print(len(bank_names_str))
            # Clear existing widgets in the GridLayout
            account_details_container = self.ids.account_details_container
            account_details_container.clear_widgets()

            # Add OneLineListItems for each bank name
            # right_action= [["dots-vertical", lambda x: self.callback(x)]]
            print(self.ids.keys())
            #if there is only one bank account of the user it will set that account to default
            if len(bank_names_str) == 1:
                # for bank_name in bank_names_str:
                items=TwoLineAvatarIconListItem(
                                       id=f'{bank_names_str[0]}',
                                       text=f'{bank_names_str[0]}',
                                       secondary_text='primary account',
                                       on_press=lambda bank_name: self.setting_default_account(f'{bank_name}'),
                                       )
                account_details_container.add_widget(items)
                phone = JsonStore('user_data.json').get('user')['value']['phone']
                users = app_tables.wallet_users.get(phone=phone)
                users.update(default_account = bank_names_str[0])
            #if user has multiple accounts it will show options to select the default account
            if len(bank_names_str)>1:
                for bank_name in bank_names_str:
                    id = bank_name
                    items=TwoLineAvatarIconListItem(
                                        # id=id,
                                        IconRightWidget(id=id,icon="dots-vertical",on_release =lambda x: self.show_menu(x)),
                                        text=f'{bank_name}',
                                        # on_press=lambda bank_name: self.setting_default_account(f'{bank_name}'),
                                        )
                    # items.add_widget()
                    account_details_container.add_widget(items)
                    self.dynmaic_ids[id] = items
            print(self.dynmaic_ids)
            self.hide_loading_animation()
            if len(bank_names_str)>1:
                phone = JsonStore('user_data.json').get('user')['value']['phone']
                users = app_tables.wallet_users.get(phone=phone)
                users_default_account = users['default_account']
                print(users_default_account)
                if users_default_account != None:
                    self.dynmaic_ids[users_default_account].secondary_text='primary account'
        except Exception as e:
            print(f"Error updating details: {e}")
            self.hide_loading_animation()
    #checking this code to get bank details
    # def setting_default_account(self,bank):
    #     #gives the bank account
    #     # getting the id of the button pressed in this we are getting the bank names
    #     bank_name = bank.id
    #     # print(bank.id)
    #     print(self.ids.keys())
    #     # print('clicked on the bank')
    #     phone = JsonStore('user_data.json').get('user')['value']['phone']
    #     data_account=app_tables.wallet_users_account.search(phone=phone,bank_name=bank_name)
        
    #     for i in data_account:
    #         print(dict(i))
    
    def show_menu(self,instance):
        # print(y)
        menu_items = [
            {
                "text": "set primary",
                "on_release": lambda x=instance: self.set_primary(x),
                # 'on_release':lambda :self.menu_callback()
            }   # Customize menu items here
            # for i in range(1)
        ]
        self.menu = MDDropdownMenu(items=menu_items)
        self.menu.caller = instance  # Set the button that triggered the menu
        self.menu.open()

    def set_primary(self,x):
        print(x)
        print(self.dynmaic_ids[x.id])
         # Print text of each item
        for i in self.dynmaic_ids:
            if i == x.id:
                self.dynmaic_ids[i].secondary_text='primary account'
            else:self.dynmaic_ids[i].secondary_text=''
                # print(self.dynmaic_ids[i].text)
          
        bank_name=x.id
        phone = JsonStore('user_data.json').get('user')['value']['phone']
        users = app_tables.wallet_users.get(phone=phone)
        users.update(default_account = bank_name)
        self.menu.dismiss()  