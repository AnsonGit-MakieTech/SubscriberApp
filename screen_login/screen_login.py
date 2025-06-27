
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty , ListProperty, BooleanProperty
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
from kivy.lang.builder import Builder

from screen_components import text_input
from variables import *
from screen_components import app_button

from screen_home.screen_home import HomeScreen
from screen_add_plan.screen_add_plan import AddPlanScreen
 


class FormLayout(BoxLayout):
    login_logo = StringProperty("")
    adaptive_font_size = NumericProperty(14)
    login_button_font_size = NumericProperty(14)
    login_button_radius = ListProperty([8, 8, 8, 8])
    info_title_font_size = NumericProperty(14)
    info_content_font_size = NumericProperty(10)

    link_font_size = NumericProperty(10)

    login_event = ObjectProperty(None)
    login_button : app_button.AppButton = ObjectProperty(None)
    username_input : text_input.OneLineInput = ObjectProperty(None)
    password_input : text_input.OneLineInput = ObjectProperty(None)

    is_on_screen = BooleanProperty(False)
    is_fill_form = BooleanProperty(False)

    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        self.login_logo = os.path.join(parent_dir, 'assets', 'login_info.png')  
    
    def update_ui(self, *args):
        if self.login_button is None or self.username_input is None or self.password_input is None:
            Clock.schedule_once(self.update_ui, 0.1)
            return 
        self.username_input.costumized_input(bgcolor = "#5C5470", hint_text = "Please provide your username here . . .", is_password = False)
        self.password_input.costumized_input(bgcolor = "#5C5470", hint_text = "Please provide your password here . . .", is_password = True)
        self.is_on_screen = True
        Clock.schedule_interval(self.realtime_input_validation, 0.1)

    
    def update_sizing(self, *args):
        width , height = self.size
        self.adaptive_font_size = int(min( width, height) * 0.05)  # 60% of label height
        padding_x = int(width * 0.08)
        padding_y = int(height * 0.05)
    
        # Set padding as (left, top, right, bottom)
        self.padding = [padding_x, padding_y, padding_x, padding_y]
        self.spacing = int(height * 0.005)

        self.login_button_font_size = int(min( width, height) * 0.035)
        r = min(width, height) * 0.02  # You can tweak 0.2 for rounder edges
        self.login_button_radius = [r, r, r, r]

        self.info_title_font_size = int(min( width, height) * 0.03)
        self.info_content_font_size = int(min( width, height) * 0.02)
        self.link_font_size = int(min( width, height) * 0.025)

    def login_account(self):  
        if not self.is_fill_form:
            return
        main_app  = MDApp.get_running_app()
        key = "login_account"
        action = "login_account"
        main_app.app_data[LOGIN_KEY] = {}
        main_app.app_data[LOGIN_KEY]['username'] = self.username_input.text_input.text
        main_app.app_data[LOGIN_KEY]['password'] = self.password_input.text_input.text 
        need_data = main_app.app_data[LOGIN_KEY]
        main_app.communications.post_data_action(need_data , key, action)
        
        main_app.process_modal.proccess_text = "Please wait while we verify your account . . ."
        main_app.process_modal.open()

        def check_response(*args):
            com_data = main_app.communications.get_and_remove(key)
            if com_data is None: 
                print("No data received")
                return True
            
            if not com_data.get('result'):
                print(f'Error: {com_data.get("message", None)}')  
                main_app.process_modal.display_error(com_data.get('message', None))
                return False 
            
            main_app.process_modal.dismiss()
            Clock.schedule_once(main_app.show_welcome_popup)  
            if not main_app.root_screen_manager.does_screen_exist(HOME_SCREEN):
                main_app.load_all_home_screen_modal()
                main_app.root_screen_manager.builder_load_screen('screen_home', 'screen_home.kv', HOME_SCREEN )
                main_app.root_screen_manager.add_handler_screen(HOME_SCREEN)
            
            main_app.delete_key_in_app_data(LOGIN_KEY)
            main_app.root_screen_manager.change_screen(HOME_SCREEN)
            return False
         
        Clock.schedule_interval(check_response, 1)

    def register_account(self):
        print("Register button pressed!")
        main_app  = MDApp.get_running_app()
        Clock.schedule_once(main_app.show_welcome_popup)  
        if not main_app.root_screen_manager.does_screen_exist(FORGOT_ACCOUNT_SCREEN):
            main_app.root_screen_manager.builder_load_screen('screen_forgot', 'screen_forgot.kv', FORGOT_ACCOUNT_SCREEN )
            main_app.root_screen_manager.add_handler_screen(FORGOT_ACCOUNT_SCREEN)
        main_app.root_screen_manager.change_screen(FORGOT_ACCOUNT_SCREEN)

    def realtime_input_validation(self, *args):
        if self.username_input.text_input.text == "" or self.password_input.text_input.text == "" :
            print("The input is empty")
            self.is_fill_form = False
            self.login_button.disabled = True
            self.login_button.opacity = 0.8
        else:
            print("The input is not empty")
            self.is_fill_form = True
            self.login_button.disabled = False
            self.login_button.opacity = 1
        return self.is_on_screen

    def down_realtime_input_validation(self, *args):
        self.is_on_screen = False
        self.username_input.text_input.text = ""
        self.password_input.text_input.text = ""

class LogoLocation(BoxLayout):

    login_logo = StringProperty("")
    title_font_size = NumericProperty(20)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        parent_dir = os.path.dirname(os.path.dirname(__file__)) 
        
        self.login_logo = os.path.join(parent_dir, 'assets', 'login_logo.png')

        # Wait for layout to be ready then compute font size
        Clock.schedule_once(self.init_font_size, 0)
        

    def init_font_size(self, *args):
        # Bind only to the label widget after it's added and ready
        label = self.ids.get('title_label')
        if label:
            label.bind(size=self.on_label_resize)
            self.on_label_resize(label, label.size)

    def on_label_resize(self, instance, size):
        width, height = size
        self.title_font_size = int(min( width, height) * 0.6)  # 60% of label height




class LoginScreen(Screen):
    adaptive_radius = ListProperty([24, 24, 0, 0])
    container_box : FormLayout = ObjectProperty(None)

    is_logging_in = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.opacity = 0

    def on_parent(self, instance, parent):
        main_app = MDApp.get_running_app()
        if parent is None:
            if self.update_radius in main_app.on_size_events_of_all_widgets:
                main_app.on_size_events_of_all_widgets.remove(self.update_radius)
        else:
            if self.update_radius not in main_app.on_size_events_of_all_widgets:
                main_app.on_size_events_of_all_widgets.append(self.update_radius)
            self.update_radius() 


    def update_radius(self, *args):
        if self.container_box:
            width, height = self.container_box.size
            r = min(width, height) * 0.05  # You can change 0.05 to any fraction
            self.adaptive_radius = [r, r, 0, 0]
            self.container_box.update_sizing()

    def on_enter(self, *args):
        main_app  = MDApp.get_running_app() 
        anim = Animation(opacity=1, duration=0.5)
        anim.bind(on_start= main_app.on_window_resize , on_complete = main_app.close_welcome_popup)
        anim.start(self)  
        Clock.schedule_once(self.load_connected_screen)
        if self.container_box is not None:
            Clock.schedule_once(self.container_box.update_ui)
        return super().on_enter(*args)


    def on_leave(self, *args):
        self.opacity = 0
        if self.container_box is not None:
            self.container_box.down_realtime_input_validation()
        return super().on_leave(*args)

 
    

    def load_connected_screen(self, *args):
        
        main_app  = MDApp.get_running_app()
        
        if not main_app.root_screen_manager.does_screen_exist(HOME_SCREEN):
            main_app.load_all_home_screen_modal()
            main_app.root_screen_manager.builder_load_screen('screen_home', 'screen_home.kv', HOME_SCREEN )
            main_app.root_screen_manager.add_handler_screen(HOME_SCREEN)

        if not main_app.root_screen_manager.does_screen_exist(FORGOT_ACCOUNT_SCREEN):
            main_app.root_screen_manager.builder_load_screen('screen_forgot', 'screen_forgot.kv', FORGOT_ACCOUNT_SCREEN )
            main_app.root_screen_manager.add_handler_screen(FORGOT_ACCOUNT_SCREEN)
        
 

         
       
