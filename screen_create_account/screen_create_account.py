
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.opacity = 0

    # def on_parent(self, instance, parent):
    #     main_app = MDApp.get_running_app()
    #     if parent is None:
    #         if self.update_radius in main_app.on_size_events_of_all_widgets:
    #             main_app.on_size_events_of_all_widgets.remove(self.update_radius)
    #     else:
    #         if self.update_radius not in main_app.on_size_events_of_all_widgets:
    #             main_app.on_size_events_of_all_widgets.append(self.update_radius)
    #         self.update_radius()
    #     if parent:
    #         self.container_box.login_event = self.login_event


    # def update_radius(self, *args):
    #     if self.container_box:
    #         width, height = self.container_box.size
    #         r = min(width, height) * 0.05  # You can change 0.05 to any fraction
    #         self.adaptive_radius = [r, r, 0, 0]

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