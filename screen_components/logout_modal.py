from kivy.uix.accordion import Widget
from kivy.uix.actionbar import Label


from kivy.uix.accordion import ObjectProperty, BooleanProperty
from kivy.uix.modalview import ModalView

from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout

import os
 
from kivy.uix.behaviors import ButtonBehavior
from kivymd.app import MDApp

from kivy.properties import ObjectProperty, NumericProperty, StringProperty , ListProperty, BooleanProperty
from kivymd.uix.behaviors import CommonElevationBehavior, RectangularRippleBehavior
from kivymd.uix.boxlayout import MDBoxLayout 
from kivy.utils import get_color_from_hex


class CustomButton(
    CommonElevationBehavior,
    RectangularRippleBehavior,
    ButtonBehavior,
    MDBoxLayout
):
    content_background_radius = ListProperty([ 8 , 8, 8 , 8 ])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = get_color_from_hex("#FAF0E6")
        
        # self.bind(size=self.update_sizing)
        Clock.schedule_once(self.update_sizing, 0.1)
        self.opacity = 0
        self.elevation = 0
    
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
        width, height = self.size
        r = min(width, height) * 0.2 # You can change 0.05 to any fraction
        self.content_background_radius = [r, r, r, r]

    def on_parent(self, instance, value):
        # Widget is now attached to the tree
        if value:
            # Animate appearance
            Animation(opacity=1, elevation=4, d=0.3).start(self)


class LogoutModal(ModalView):
    
    title_font_size = NumericProperty(14)
    content_font_size = NumericProperty(14)
    main_layout : BoxLayout = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
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
    
    def on_kv_post(self, base_widget):
        Clock.schedule_once(self.update_sizing, 0.1)
        return super().on_kv_post(base_widget)
    
    def update_sizing(self, *args):
        width, height = self.size
        self.title_font_size = min(width, height) * 0.045
        self.content_font_size = min(width, height) * 0.03
        
        padding_x = int(width * 0.08)
        padding_y = int(height * 0.05)
    
        # Set padding as (left, top, right, bottom)
        self.main_layout.padding = [padding_x, padding_y, padding_x, padding_y]
        self.main_layout.spacing = int(height * 0.005)


kv_logout_modal = '''
<LogoutModal>:
    auto_dismiss: True
    auto_dismiss: False
    background: ""  # Removes default dim background
    background_color: 0, 0, 0, 0
    
    main_layout : main_layout
    
    BoxLayout:
        id: main_layout
        orientation:"vertical"
        size_hint: 0.75 , 0.25
        pos_hint: { "center_x": 0.5 , "center_y": 0.5 }  


        canvas.before:
            Color:
                rgba: chex("#FAF0E6")
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [10]

        Widget:
            size_hint: 1, 0.025
        Label:
            size_hint: 1, 0.2
            text: "Logout Confirmation"
            font_size: root.title_font_size
            color: chex("#352F44")
            font_name: "p_bold"
        Widget:
            size_hint: 1, 0.1
        Label: 
            size_hint: 1, 0.2
            valign: "middle"  # Or "center"
            halign: "center"
            font_name: "p_light"
            font_size: root.content_font_size
            color: chex("#014367")
            text: "Are you sure you want to logout?"
        
        Widget:
            size_hint: 1, 0.2

        BoxLayout:
            size_hint: 1, 0.25
            orientation: "horizontal"

            Widget:
                size_hint: 0.13, 1
            
            CustomButton:
                size_hint: 0.4, 1
                md_bg_color: chex("#5C5470")
                on_release: root.dismiss()
                
                Label: 
                    size_hint: 1, 1
                    font_name: "p_bold"
                    font_size: root.content_font_size
                    color: chex("#FFFFFF")
                    text: "Cancel"
                    
            Widget:
                size_hint: 0.1, 1

            CustomButton:
                size_hint: 0.4, 1
                md_bg_color: chex("#A30000")
                
                Label: 
                    size_hint: 1, 1
                    font_name: "p_bold"
                    font_size: root.content_font_size
                    color: chex("#FFFFFF")
                    text: "Logout"
                
            Widget:
                size_hint: 0.13, 1
            
        Widget:
            size_hint: 1, 0.025

<CustomButton>:
    theme_elevation_level: "Custom"
    elevation_level: 2
    theme_shadow_offset: "Custom"
    shadow_offset: 0, -3
    theme_shadow_softness: "Custom"
    shadow_softness: 12
    shadow_radius: root.content_background_radius
    radius: root.content_background_radius
    
'''

