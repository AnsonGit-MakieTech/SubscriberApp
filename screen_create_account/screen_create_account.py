from kivy.uix.accordion import DictProperty

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty , ListProperty, DictProperty
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout 
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.animation import Animation
from kivy.uix.button import Button
from kivy.uix.image import Image
from types import MethodType  # ✅ Import MethodType
from kivy.clock import Clock
from kivy.utils import platform
from kivy.uix.screenmanager import SlideTransition, FadeTransition, SwapTransition, ScreenManager
from kivymd.app import MDApp 
from kivy.uix.widget import Widget
from kivy.uix.dropdown import DropDown
from kivy.utils import get_color_from_hex

import os

from screen_components import text_input
from variables import *
from screen_components import app_button, top_form_buttons, text_input


class CityDropdownButton(app_button.AppButton):
    text = StringProperty("Select City")
    text_font_size = NumericProperty(16)
    value = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = get_color_from_hex("#5C5470")
        self.opacity = 0
        self.elevation = 0
 
    
    def update_sizing(self, *args):
        width, height = self.size
        self.text_font_size = int(min(width, height) * 0.3)

class AccountRegistrationFormLayout(
    MDBoxLayout
):
    
    h1_font_size = NumericProperty(14)
    h2_font_size = NumericProperty(14)
    valid_id_image_width = NumericProperty(250)
    
    first_name_input: text_input.OneLineInput = ObjectProperty(None)
    last_name_input: text_input.OneLineInput = ObjectProperty(None)
    middle_name_input: text_input.OneLineInput = ObjectProperty(None)
    email_input: text_input.OneLineInput = ObjectProperty(None)
    street_input : text_input.OneLineInput = ObjectProperty(None)
    barangay_input: text_input.OneLineInput = ObjectProperty(None)
    city_input: text_input.OneLineInput = ObjectProperty(None)
    phone1_input: text_input.OneLineInput = ObjectProperty(None)
    phone2_input: text_input.OneLineInput = ObjectProperty(None)
    phone3_input: text_input.OneLineInput = ObjectProperty(None)
    
    
    selected_city = StringProperty("Select City")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opacity = 0

        self.dropdown = DropDown(max_height=150)

        # Create dropdown options
        for option in ["Click Here To Select", "Option 1", "Option 2", "Option 3", "Option 4"]:
            widget = Widget(size_hint_y=None, height=2)
            self.dropdown.add_widget(widget)
            btn = CityDropdownButton(size_hint_y=None, height=34)
            btn.text = option
            btn.value = option
            btn.bind(on_release=lambda btn: self.dropdown.select(btn))
            self.dropdown.add_widget(btn)

        # Bind button from KV to open dropdown
        self.dropdown.bind(on_select=self.on_select)

    def on_select(self, instance, value):
        self.selected_city = value.text
        print(f"Selected option: {value.text}")
        print(value)
        pass

    
    def customized_ui(self):
        self.city_input.bind(on_release=self.dropdown.open)
        self.first_name_input.costumized_input( hint_text = "First Name . . ." )
        self.last_name_input.costumized_input( hint_text = "Last Name . . ." )
        self.middle_name_input.costumized_input( hint_text = "Middle Name . . ." )
        self.email_input.costumized_input( hint_text = "Email . . ." )
        self.street_input.costumized_input( hint_text = "Street . . ." )
        self.barangay_input.costumized_input( hint_text = "Barangay . . ." )
        self.city_input.update_color("#5C5470")
        self.phone1_input.costumized_input( hint_text = "Primary Phone Number (required)" )
        self.phone2_input.costumized_input( hint_text = "Additional Phone Number (optional)" )
        self.phone3_input.costumized_input( hint_text = "Additional Phone Number (optional)" )


    def update_sizing(self, *args):
        width, height = self.size
        self.h1_font_size = int(width * 0.043)
        if self.h1_font_size > 18:
            self.h1_font_size = 18
        self.h2_font_size = int(width * 0.038)
        if self.h2_font_size > 16:
            self.h2_font_size = 16
        
        self.valid_id_image_width = int(width * 0.9)
        if self.valid_id_image_width > 250:
            self.valid_id_image_width = 250
        print(f"width: {width}, height: {height} , valid_id_image_width: {self.valid_id_image_width}")


class CreateAccountScreen(Screen): 
    login_logo = StringProperty("")
    create_account_logo = StringProperty("")
    
    info_title_font_size = NumericProperty(14)
    info_content_font_size = NumericProperty(10)
    adaptive_radius = ListProperty([ 0, 0, 24, 24])
    
    create_account_title_font_size = NumericProperty(14)
    create_account_content_font_size = NumericProperty(10)
    
    header_buttons : top_form_buttons.HeaderButtons = ObjectProperty(None)
    find_my_location_button : app_button.AppButton = ObjectProperty(None)
    
    find_my_location_button_font_size = NumericProperty(14)
    
    h1_font_size = NumericProperty(14)
    h2_font_size = NumericProperty(14)

    
    registration_form : BoxLayout = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.opacity = 0
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        self.login_logo = os.path.join(parent_dir, 'assets', 'login_info.png')
        self.create_account_logo = os.path.join(parent_dir, 'assets', 'create_account_logo.png')

    def on_parent(self, instance, parent):
        main_app = MDApp.get_running_app()
        if parent is None:
            if self.update_sizing in main_app.on_size_events_of_all_widgets:
                main_app.on_size_events_of_all_widgets.remove(self.update_sizing)
        else:
            if self.update_sizing not in main_app.on_size_events_of_all_widgets:
                main_app.on_size_events_of_all_widgets.append(self.update_sizing)
            self.update_sizing() 

    def update_sizing(self, *args):
        width , height = self.size 
        self.info_title_font_size = int(min( width, height) * 0.03)
        self.info_content_font_size = int(min( width, height) * 0.02)
        r = min(width, height) * 0.05  # You can change 0.05 to any fraction
        self.adaptive_radius = [0, 0, r, r]
        self.header_buttons.update_sizing()
        
        self.create_account_title_font_size = int(width* 0.06)
        self.create_account_content_font_size = int(width  * 0.03)
        if self.create_account_title_font_size > 27:
            self.create_account_title_font_size = 27
        if self.create_account_content_font_size > 25:
            self.create_account_content_font_size = 25
        self.h1_font_size = int(width * 0.04)
        if self.h1_font_size > 17:
            self.h1_font_size = 17
        self.h2_font_size = int(width * 0.03)
        if self.h2_font_size > 15:
            self.h2_font_size = 15
        self.find_my_location_button_font_size = int(width * 0.03)
        if self.find_my_location_button_font_size > 19:
            self.find_my_location_button_font_size = 19
        
        if self.registration_form is not None:
            if len(self.registration_form.children) > 0:
                self.registration_form.children[0].update_sizing()
            

    def on_enter(self, *args):
        main_app  = MDApp.get_running_app()
        # Clock.schedule_once( lambda *args : main_app.logout_modal.open() , 2)
        # Clock.schedule_once( lambda *args : main_app.process_modal.display_error("Successfully Processed") , 4)
        # Clock.schedule_once( lambda *args : main_app.add_ticket_modal.open() , 2)
        # main_app.on_window_resize()
        
        Clock.schedule_once(self.display_registration_form, 1) # Used to display the registration form

        self.find_my_location_button.update_color("#352F44")
        anim = Animation(opacity=1, duration=0.5)
        anim.bind(on_complete= main_app.on_window_resize)
        anim.start(self)
        
        
        # print("entering logoin")
        return super().on_enter(*args)
    

    def display_registration_form(self, *args):
        if not self.registration_form:
            Clock.schedule_once(self.display_registration_form, 0.1)
            return

        if len(self.registration_form.children) < 1:
            registration = AccountRegistrationFormLayout()
            anim = Animation(opacity=1, duration=0.5)
            anim.start(registration)
            self.registration_form.add_widget(registration) 
            registration.customized_ui()


    def find_my_location(self, *args):
        main_app = MDApp.get_running_app()
        main_app.user_map_verification_modal.open() 
    
