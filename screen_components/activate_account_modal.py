
from kivy.uix.modalview import ModalView
 
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


class ActivateAccountModal(ModalView):
    content_background_radius = ListProperty([ 8 , 8, 8 , 8 ])
    button_radius = ListProperty([ 8 , 8, 8 , 8 ])

    h1_font_size = NumericProperty(30)
    h2_font_size = NumericProperty(20)

    content_text = StringProperty("We've just sent an email with your activation link. Please check your inbox (and spam folder) and click the link to complete your registration.")
    proceed_text = StringProperty('Returns to home screen')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.opacity = 0 
         
    
    def on_kv_post(self, base_widget):
        Clock.schedule_once(self.update_sizing, 0.1)
        return super().on_kv_post(base_widget)
    
    def update_sizing(self, *args):
        width, height = self.size 

        rad = min(width , height) * 0.02
        if rad > 10:
            rad = 10
        self.content_background_radius = [rad, rad, rad, rad] 

        self.h1_font_size = min(width , height) * 0.03
        self.h2_font_size = min(width , height) * 0.025
        
        brad = min(width, height) * 0.01
        if brad > 10:
            brad = 10
        self.button_radius = [brad, brad, brad, brad]

        print(f"width: {width}, height: {height}, rad: {rad}")
 
    def on_open(self):
        anim = Animation(opacity=1, d=0.3)
        anim.bind(on_start=self.update_sizing)
        anim.start(self)
        return super().on_open()

    def on_pre_dismiss(self):
        self.opacity = 0
        return super().on_pre_dismiss()
    

kv_activate_account_modal = '''
<ActivateAccountModal>: 
    size_hint: 1, 1
    # auto_dismiss: False
    background: ""
    background_color: 0, 0, 0, 0
    overlay_color : 0, 0, 0, 0

    canvas.before:
        Color:
            rgb: chex("#5C5470")
            a: 0.5
        Rectangle:
            pos: self.pos
            size: self.size

            
    MDBoxLayout:
        orientation: "vertical"
        pos_hint: {"center_x": 0.5,"center_y": 0.5}
        size_hint: 0.85, 0.23
        md_bg_color: chex("#352F44")
        radius: root.content_background_radius 


        Widget:
            size_hint: 1, 0.15

            
        Label:
            size_hint: 1, 0.15 
            pos_hint: {"x": 0.05}  
            text: "Activate Your Account"
            color: chex("#FFFFFF")
            font_name: "p_semibold" 
            text_size: self.size
            halign: "left"
            valign: "middle"
            font_size: root.h1_font_size

        Label:
            size_hint: 0.9, 0.4
            pos_hint: {"x": 0.05}  
            text: root.content_text
            color: chex("#FFFFFF")
            font_name: "p_extralight" 
            text_size: self.size
            halign: "left"
            valign: "top"
            font_size: root.h2_font_size

        AppButton:
            size_hint: None, 0.15
            adaptive_width: True
            orientation: "horizontal"
            md_bg_color: chex("#F98585")
            radius: root.button_radius
            pos_hint: {"right": 0.95}

            Label: 
                size_hint: None , 1 
                text: "    "
                font_size: root.h1_font_size 
                font_name: "p_extrabold"
                text_size: None, self.height
                halign: "left"
                valign: "middle" 
                width: self.texture_size[0]

            Label: 
                size_hint: None , 1 
                text: root.proceed_text
                font_size: root.h1_font_size
                color: chex("#352F44")
                font_name: "p_extrabold"
                text_size: None, self.height
                halign: "left"
                valign: "middle" 
                width: self.texture_size[0]

            Label: 
                size_hint: None , 1 
                text: "    "
                font_size: root.h1_font_size 
                font_name: "p_extrabold"
                text_size: None, self.height
                halign: "left"
                valign: "middle" 
                width: self.texture_size[0]

        Widget:
            size_hint: 1, 0.15
 



'''





