
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
from screen_components import app_button






class CreateAccountScreen(Screen):
    adaptive_radius = ListProperty([24, 24, 0, 0]) 
    login_logo = StringProperty("")
    info_title_font_size = NumericProperty(14)
    info_content_font_size = NumericProperty(10)
    adaptive_radius = ListProperty([24, 24, 0, 0])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.opacity = 0
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        self.login_logo = os.path.join(parent_dir, 'assets', 'login_info.png')
        Clock.schedule_once(self.update_sizing, 0) 

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

    def on_enter(self, *args):
        main_app  = MDApp.get_running_app()
        # Clock.schedule_once( lambda *args : main_app.logout_modal.open() , 2)
        # Clock.schedule_once( lambda *args : main_app.process_modal.display_error("Successfully Processed") , 4)
        # Clock.schedule_once( lambda *args : main_app.add_ticket_modal.open() , 2)
        # main_app.on_window_resize()
        anim = Animation(opacity=1, duration=0.5)
        anim.bind(on_complete= main_app.on_window_resize)
        anim.start(self)
        
        # print("entering logoin")
        return super().on_enter(*args)