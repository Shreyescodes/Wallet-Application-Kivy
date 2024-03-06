from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from kivy.clock import Clock

loading_screen = """
<loadingScreen>:
    BoxLayout:
        orientation: 'vertical'
        spacing: dp(20)
        BoxLayout:
            orientation: 'vertical'
        Image:
            source: "images/2.png"  # Update the path to your image
            size_hint: None, None
            size: dp(60), dp(60)
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}

        Label:
            id: loading_label
            text: "Loading"
            font_size: "20sp"
            #bold: True
            color: 0, 0, 0, 1  # Black color
"""

Builder.load_string(loading_screen)


class loadingScreen(Screen):
    def on_enter(self):
        # Start updating the dots label
        Clock.schedule_interval(self.update_dots, 0.5)

    def update_dots(self, dt):
        # Update the dots label with one dot at a time
        dots_label = self.ids.loading_label
        current_text = dots_label.text

        if current_text == "Loading...":
            dots_label.text = "Loading"
        else:
            dots_label.text += "."
