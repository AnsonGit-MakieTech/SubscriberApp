

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
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

from variables import *
import os

from screen_home import (
    headline_layout
)


class TappableImage(ButtonBehavior, Image):
    button_event = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def on_press(self):
        print("Image tapped!") 
        if self.button_event:
            self.button_event()

class AccountHeader(FloatLayout):
    edit_icon : TappableImage = ObjectProperty(None)
    logout_icon : TappableImage = ObjectProperty(None)
    refresh_icon : TappableImage = ObjectProperty(None)

    buttons_spacing = NumericProperty(0)
    account_image_size = NumericProperty(100)
    account_fname_font_size = NumericProperty(15)

    account_image_radius = ListProperty([0, 0, 0, 0])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs) 

    
    # def on_parent(self, instance, parent):
    #     main_app = MDApp.get_running_app()
    #     if parent is None:
    #         if self.update_sizing in main_app.on_size_events_of_all_widgets:
    #             main_app.on_size_events_of_all_widgets.remove(self.update_sizing)
    #     else:
    #         if self.update_sizing not in main_app.on_size_events_of_all_widgets:
    #             main_app.on_size_events_of_all_widgets.append(self.update_sizing)
            
    

    def on_kv_post(self, *args):
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        self.edit_icon.source = os.path.join(parent_dir, 'assets', 'edit_icon.png')
        self.logout_icon.source = os.path.join(parent_dir, 'assets', 'logout_icon.png')
        self.refresh_icon.source = os.path.join(parent_dir, 'assets', 'refresh_icon.png')
        
    
    def update_sizing(self, width, height ):
        multiplier = 0.08
        self.edit_icon.size = (width * multiplier, width * multiplier)
        self.logout_icon.size = (width * multiplier, width * multiplier)
        self.refresh_icon.size = (width * multiplier, width * multiplier)
        self.buttons_spacing = width * 0.01

        self.account_image_size = min(width, height) * 0.25

        self.account_fname_font_size = min(width, height) * 0.09

        rad = min(width, height) * 0.05
        if rad > 16:
            rad = 16
        self.account_image_radius = [rad, rad, rad, rad]

class HomeScreen(Screen):
    
    account_header : AccountHeader = ObjectProperty(None)
    header_height : NumericProperty = NumericProperty(0)
     
    home_screen_spacing = NumericProperty(0)
    home_screen_radius = ListProperty([0, 0, 0, 0])
    home_screen_padding = ListProperty([0, 0, 0, 0])


    headline : headline_layout.HeadlineLayout = ObjectProperty(None)



    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.opacity = 0


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
        self.header_height = min(width, height) * 0.5

        if self.account_header is not None:
            self.account_header.update_sizing(width=width, height=height)
        
        self.home_screen_spacing = min(width, height) * 0.05

        hrad = min(width, height) * 0.05
        if hrad > 16:
            hrad = 16
        self.home_screen_radius = [hrad, hrad, 0 , 0]
        hpad = min(width, height) * 0.06
        if hpad > 20:
            hpad = 20
        self.home_screen_padding = [hpad, hpad, hpad, hpad]
        
        
        if self.headline is not None:
            self.headline.update_sizing(width=width, height=height)
        
        
        
        
        # print(f"width: {width} , height: {height}, hpad: {hpad}")




    def on_enter(self, *args):
        
        main_app  = MDApp.get_running_app()
        # Clock.schedule_once( lambda *args : main_app.logout_modal.open() , 2)
        # Clock.schedule_once( lambda *args : main_app.process_modal.display_error("Successfully Processed") , 4)
        anim = Animation(opacity=1, duration=0.5)
        anim.bind( on_start= main_app.on_window_resize, on_complete=self.remove_outside_screens)
        anim.start(self)
        # print("entering logoin")
        self.account_header.logout_icon.button_event = main_app.logout_modal.open
        self.account_header.edit_icon.button_event = main_app.add_ticket_modal.open
        self.account_header.refresh_icon.button_event = main_app.process_modal.open

        Clock.schedule_once(self.load_all_connected_screen, 1)
 
        return super().on_enter(*args)
 
    
    def remove_outside_screens(self, *args):
        # This function used to removed the outside screens ( login, register and forgot password)
        main_app  = MDApp.get_running_app()
        # main_app.root_screen_manager.remove_screen(LOGIN_SCREEN)
        # main_app.root_screen_manager.remove_screen(CREATE_ACCOUNT_SCREEN)
        # main_app.root_screen_manager.remove_screen(FORGOT_ACCOUNT_SCREEN)

        main_app.close_welcome_popup()

    
    def load_all_connected_screen(self, *args):
        main_app  = MDApp.get_running_app()
        
        if not main_app.root_screen_manager.does_screen_exist(ADD_PLAN_SCREEN): 
            main_app.root_screen_manager.builder_load_screen('screen_add_plan', 'screen_add_plan.kv', ADD_PLAN_SCREEN )
            main_app.root_screen_manager.add_handler_screen(ADD_PLAN_SCREEN)



