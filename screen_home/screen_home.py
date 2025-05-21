

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

import os


class TappableImage(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def on_press(self):
        print("Image tapped!")  

class AccountHeader(FloatLayout):
    edit_icon : TappableImage = ObjectProperty(None)
    logout_icon : TappableImage = ObjectProperty(None)
    refresh_icon : TappableImage = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.update_sizing)
    
    def on_kv_post(self, *args):
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        self.edit_icon.source = os.path.join(parent_dir, 'assets', 'edit_icon.png')
        self.logout_icon.source = os.path.join(parent_dir, 'assets', 'logout_icon.png')
        self.refresh_icon.source = os.path.join(parent_dir, 'assets', 'refresh_icon.png')
        
    
    def update_sizing(self, *args):
        width , height = self.size
        multiplier = 0.1
        self.edit_icon.size = (width * multiplier, height * multiplier)
        self.logout_icon.size = (width * multiplier, height * multiplier)
        self.refresh_icon.size = (width * multiplier, height * multiplier)

class HomeScreen(Screen):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.update_sizing)
    
    def update_sizing(self, *args):
        width , height = self.size


    def on_enter(self, *args):
        main_app  = MDApp.get_running_app()
        Clock.schedule_once( lambda *args : main_app.process_modal.open() , 2)
        Clock.schedule_once( lambda *args : main_app.process_modal.display_error("Successfully Processed") , 4)
        
        # print("entering logoin")
        return super().on_enter(*args)