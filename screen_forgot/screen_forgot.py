
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty , ListProperty
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout 
from kivy.animation import Animation
from kivy.uix.button import Button
from kivy.uix.image import Image
from types import MethodType  # ✅ Import MethodType
from kivy.clock import Clock
from kivy.utils import platform
from kivy.uix.screenmanager import SlideTransition, FadeTransition, SwapTransition, ScreenManager
from kivymd.app import MDApp 

import os

from screen_components import text_input
from variables import *
from screen_components import app_button, top_form_buttons, text_input






class ForgotAccountScreen(Screen):
    adaptive_radius = ListProperty([ 0, 0, 24, 24])
    login_logo = StringProperty("")
    forgot_account_logo = StringProperty("")
    
    info_title_font_size = NumericProperty(14)
    info_content_font_size = NumericProperty(10) 
    
    forgot_account_title_font_size = NumericProperty(14)
    forgot_account_content_font_size = NumericProperty(10)
    
    header_buttons : top_form_buttons.HeaderButtons = ObjectProperty(None)
    username_text_input : text_input.OneLineInput = ObjectProperty(None)
    new_password_text_input : text_input.OneLineInput = ObjectProperty(None)
    retype_new_password_text_input : text_input.OneLineInput = ObjectProperty(None)
    
    submit_button : app_button.AppButton = ObjectProperty(None)
    submit_button_font_size = NumericProperty(14)
    
    h1_font_size = NumericProperty(14)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.opacity = 0
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        self.login_logo = os.path.join(parent_dir, 'assets', 'login_info.png')
        self.forgot_account_logo = os.path.join(parent_dir, 'assets', 'forgot_account_logo.png')
        
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
        
        self.forgot_account_title_font_size = int(width* 0.07)
        self.forgot_account_content_font_size = int(width  * 0.03)
        if self.forgot_account_title_font_size > 29:
            self.forgot_account_title_font_size = 29
        if self.forgot_account_content_font_size > 25:
            self.forgot_account_content_font_size = 25
        self.h1_font_size = int(width * 0.04)
        if self.h1_font_size > 17:
            self.h1_font_size = 17
        self.submit_button_font_size = int(width * 0.03)
        if self.submit_button_font_size > 19:
            self.submit_button_font_size = 19
    
    def on_enter(self, *args):
        main_app  = MDApp.get_running_app()
        # Clock.schedule_once( lambda *args : main_app.logout_modal.open() , 2)
        # Clock.schedule_once( lambda *args : main_app.process_modal.display_error("Successfully Processed") , 4)
        # Clock.schedule_once( lambda *args : main_app.add_ticket_modal.open() , 2)
        # main_app.on_window_resize()
        
        self.submit_button.update_color("#352F44")
        self.username_text_input.costumized_input(hint_text="Type your username here . . .")
        self.new_password_text_input.costumized_input(hint_text="Type your new password here . . .")
        self.retype_new_password_text_input.costumized_input(hint_text="Retype your new password here . . .")
        self.header_buttons.customized_ui(button_text_1 = "Login Account" , button_text_2 = "Create Account")
        anim = Animation(opacity=1, duration=0.5)
        anim.bind(on_complete= main_app.on_window_resize)
        anim.start(self)
        
        # print("entering logoin")
        return super().on_enter(*args)