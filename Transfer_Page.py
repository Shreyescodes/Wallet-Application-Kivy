from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
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
                    mode:'rectangle'
                    hint_text: "Amount"
                    helper_text: "Enter the amount to transfer"
                    helper_text_mode: "on_focus"
                    input_type: "number"
                    pos_hint: {"center_x": 0.5, "center_y": 0.8}
                    size_hint_x:None
                    width:300
              
                MDTextField:
                    hint_text: "Mobile no"
                    helper_text: "Enter Receiver's mobile number"
                    helper_text_mode: "on_focus"
                    input_type: "number"
                    pos_hint: {"center_x": 0.5, "center_y": 0.7}
                    size_hint_x:None
                    width:300
                    
            
                MDTextField:
                    hint_text: "Receiver's Name"
                    helper_text: "Enter receiver's name"
                    helper_text_mode: "on_focus"
                    pos_hint: {"center_x": 0.5, "center_y": 0.6}
                    size_hint_x:None
                    width:300
                    
                MDTextField:
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
                    on_text: app.select_currency(self.text)
                    md_bg_color: 52/255.0, 171/255.0, 235/255.0,0  
                    canvas.before:
                        Color:
                            rgba: 52/255.0, 171/255.0, 235/255.0,0  # Set the background color (in this case, a dark gray)
                        Rectangle:
                            pos: self.pos
                            size: self.size   
                    
                MDRaisedButton:
                    text: "Transfer Money"
                    on_release: root.manager.transfer_money(self)
                    pos_hint: {"center_x": 0.5, "center_y": 0.4}

'''
Builder.load_string(kv_string)
class TransferScreen(Screen):
    def go_back(self):
        self.manager.current = 'dashboard'
class MoneyTransferApp(MDApp):
    def build(self):
        # self.theme_cls.theme_style = "Dark"
        # self.theme_cls.primary_palette = "BlueGray"

        return Builder.load_string(kv_string)
    def select_currency(self, currency):
        self.root.ids.currency_spinner.text = currency

    def transfer_money(self, instance):
        # Implement the money transfer logic here
        transfer_amount = self.root.children[4].text
        sender_name = self.root.children[0].text
        mobile_no_number = self.root.children[1].text
        receiver_name = self.root.children[2].text
        receiver_account_number = self.root.children[3].text


        # Add your logic for money transfer here
        print(
            f"Transfer from {sender_name} ({mobile_no_number}) to {receiver_name} ({receiver_account_number}): {transfer_amount}")


if __name__ == "__main__":
    MoneyTransferApp().run()
