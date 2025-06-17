
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
from kivy.utils import get_color_from_hex

import os

from screen_components import text_input
from variables import *
from screen_components import app_button, top_form_buttons, text_input
 
from kivy.uix.widget import Widget
from kivy.properties import ListProperty
from kivy.graphics import Color, Ellipse

class AdaptiveCircle(Widget):
    color = ListProperty(get_color_from_hex("#5C5470"))  # default: opaque red

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # draw the circle once
        with self.canvas:
            Color(rgba=self.color)
            # placeholder for the ellipse instruction
            self._ellipse = Ellipse(pos=self.pos, size=self.size)

        # whenever pos/size/color changes, update the ellipse
        self.bind(pos=self._update_graphics,
                  size=self._update_graphics,
                  color=self._update_color)

    def _update_graphics(self, *args):
        # keep the Ellipse in sync
        self._ellipse.pos = self.pos
        self._ellipse.size = self.size

    def _update_color(self, instance, value):
        # redraw the Color instruction
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=value)
        # note: if you want the circle to be behind other canvas ops,
        # you could put this in canvas.before instead of canvas.
 

class ProductShowcaseScreen(Screen): 
    circle_widget = ObjectProperty(None)

    h1_font_size = NumericProperty(30)
    h2_font_size = NumericProperty(20)
    h3_font_size = NumericProperty(16)
    h4_font_size = NumericProperty(14)
    h5_font_size = NumericProperty(12)

    cart_subscribe_icon = StringProperty('')


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.opacity = 0
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        self.cart_subscribe_icon = os.path.join(parent_dir, 'assets', 'cart_subscribe_icon.png') 
        

        
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

        if self.circle_widget is not None:
            circle_size = min(width, height) * 1.52
            self.circle_widget.size = (circle_size, circle_size)
        
        self.h1_font_size = min(width, height) * 0.04
        self.h2_font_size = min(width, height) * 0.03
        self.h3_font_size = min(width, height) * 0.025
        self.h4_font_size = min(width, height) * 0.02
        self.h5_font_size = min(width, height) * 0.015




