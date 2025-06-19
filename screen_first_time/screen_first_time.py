
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

# from screen_login.screen_login import LoginScreen




class FirstTimeScreen(Screen): 
    logo = StringProperty('')
    image_size = NumericProperty(100)
    visit_icon = StringProperty('')
    visit_icon_size = NumericProperty(100)
    charles_tv_icon_spacing = NumericProperty(10)
    has_wifi_icon = StringProperty('')
    register_icon = StringProperty('')
    button_icon_size = NumericProperty(100)


    h1_font_size = NumericProperty(30)
    h2_font_size = NumericProperty(20)
    h3_font_size = NumericProperty(15)
    h4_font_size = NumericProperty(12)

    button_spacing = NumericProperty(20)
    button_size = NumericProperty(200)
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.opacity = 0
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        self.logo = os.path.join(parent_dir, 'assets', 'app_logo.png')
        self.visit_icon = os.path.join(parent_dir, 'assets', 'visit_icon.png')
        self.has_wifi_icon = os.path.join(parent_dir, 'assets', 'has_wifi_icon.png')
        self.register_icon = os.path.join(parent_dir, 'assets', 'register_icon.png')
 

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
        self.image_size = min(width, height) * 0.45 
        self.button_icon_size = min(width, height) * 0.12

        self.h1_font_size = int(min(width, height) * 0.038)
        self.h2_font_size = int(min(width, height) * 0.033)
        self.h3_font_size = int(min(width, height) * 0.025)
        self.h4_font_size = int(min(width, height) * 0.023)

        self.button_spacing = int(min(width, height) * 0.08)
        self.button_size = int(min(width, height) * 0.3)

        self.visit_icon_size = int(min(width, height) * 0.06)
        self.charles_tv_icon_spacing = int(min(width, height) * 0.02)


        
        print(f'width: {width}, height: {height} , image_size: {self.image_size}')



    def on_enter(self, *args):
        main_app  = MDApp.get_running_app()
        
        anim = Animation(opacity=1, duration=0.5)
        anim.bind(on_start= main_app.on_window_resize , on_complete = main_app.close_welcome_popup)
        anim.start(self)

        Clock.schedule_once(self.load_connected_screen)
        return super().on_enter(*args)

    def on_leave(self, *args):
        self.opacity = 0
        return super().on_leave(*args)
    

    def goto_login_screen(self, *args):
        main_app  = MDApp.get_running_app()
        Clock.schedule_once(main_app.show_welcome_popup) 
        main_app.root_screen_manager.change_screen(LOGIN_SCREEN)


    def goto_showcase_screen(self, *args):
        main_app  = MDApp.get_running_app()
        Clock.schedule_once(main_app.show_welcome_popup) 
        main_app.root_screen_manager.change_screen(PRODUCT_SHOWCASE_SCREEN)

 
    def goto_create_screen(self, *args):
        main_app  = MDApp.get_running_app()
        Clock.schedule_once(main_app.show_welcome_popup) 
        main_app.root_screen_manager.change_screen(CREATE_ACCOUNT_SCREEN)


    def load_connected_screen(self, *args):
        main_app  = MDApp.get_running_app()
        if not main_app.root_screen_manager.does_screen_exist(LOGIN_SCREEN):
            main_app.root_screen_manager.builder_load_screen('screen_login', 'screen_login.kv', LOGIN_SCREEN )
            main_app.root_screen_manager.add_handler_screen(LOGIN_SCREEN)
        
        if not main_app.root_screen_manager.does_screen_exist(PRODUCT_SHOWCASE_SCREEN):
            main_app.root_screen_manager.builder_load_screen('screen_product_showcase', 'screen_product_showcase.kv', PRODUCT_SHOWCASE_SCREEN )
            main_app.root_screen_manager.add_handler_screen(PRODUCT_SHOWCASE_SCREEN)
        
        if not main_app.root_screen_manager.does_screen_exist(CREATE_ACCOUNT_SCREEN):
            main_app.root_screen_manager.builder_load_screen('screen_create_account', 'screen_create_account.kv', CREATE_ACCOUNT_SCREEN )
            main_app.root_screen_manager.add_handler_screen(CREATE_ACCOUNT_SCREEN)







