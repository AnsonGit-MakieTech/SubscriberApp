
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






class FormLayout(BoxLayout):
    login_logo = StringProperty("")
    adaptive_font_size = NumericProperty(14)
    login_button_font_size = NumericProperty(14)
    login_button_radius = ListProperty([8, 8, 8, 8])
    info_title_font_size = NumericProperty(14)
    info_content_font_size = NumericProperty(10)

    login_event = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        self.login_logo = os.path.join(parent_dir, 'assets', 'login_info.png')
        Clock.schedule_once(self.update_sizing, 0)
        # self.bind(size=self.update_sizing)

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

    def login_account(self):
        print("Login button pressed!")
        self.login_event()


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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.opacity = 0

    # def on_kv_post(self, base_widget):
        
    #     container = self.ids.container_box
    #     container.bind(size=self.update_radius)


    def on_parent(self, instance, parent):
        main_app = MDApp.get_running_app()
        if parent is None:
            if self.update_radius in main_app.on_size_events_of_all_widgets:
                main_app.on_size_events_of_all_widgets.remove(self.update_radius)
        else:
            if self.update_radius not in main_app.on_size_events_of_all_widgets:
                main_app.on_size_events_of_all_widgets.append(self.update_radius)
            self.update_radius()
        if parent:
            self.container_box.login_event = self.login_event


    # def on_parent(self, instance, parent):
    #     if parent:
    #         self.container_box.login_event = self.login_event

    def update_radius(self, *args):
        if self.container_box:
            width, height = self.container_box.size
            r = min(width, height) * 0.05  # You can change 0.05 to any fraction
            self.adaptive_radius = [r, r, 0, 0]

    def on_enter(self, *args):
        main_app  = MDApp.get_running_app()
        # Clock.schedule_once( lambda *args : main_app.logout_modal.open() , 2)
        # Clock.schedule_once( lambda *args : main_app.process_modal.display_error("Successfully Processed") , 4)
        Clock.schedule_once( lambda *args : main_app.add_ticket_modal.open() , 2)
        # main_app.on_window_resize()
        anim = Animation(opacity=1, duration=0.5)
        anim.bind(on_complete= main_app.on_window_resize)
        anim.start(self)
        
        # print("entering logoin")
        return super().on_enter(*args)

    def login_event(self):
        print("login event")
        main_app  = MDApp.get_running_app()
        Clock.schedule_once(main_app.show_welcome_popup) 
        self.manager.current = HOME_SCREEN


