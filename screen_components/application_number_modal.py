
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







class ApplicationNumberModal(ModalView):
    content_background_radius = ListProperty([ 8 , 8, 8 , 8 ])
    button_radius = ListProperty([ 8 , 8, 8 , 8 ])
    
    h1_font_size = NumericProperty(30)
    h2_font_size = NumericProperty(20)
    h3_font_size = NumericProperty(20)
    application_number_font_size = NumericProperty(20)

    content_text = StringProperty("Great! Your application number has been generated. Please [font=p_semibold]screenshot[/font] or [font=p_semibold]copy this number[/font] now—you'll need to show it when you visit our office to complete your payment and app registration.")
    copy_text = StringProperty("   Copy Number    ")
    proceed_text = StringProperty("Returns to home screen")
    application_number = StringProperty('A-102345')


    copy_icon = StringProperty('')
    copy_icon_size = NumericProperty(100)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.opacity = 0
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        self.copy_icon = os.path.join(parent_dir, 'assets', 'copy_icon.png')


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
        self.h2_font_size = min(width , height) * 0.023
        self.h3_font_size = min(width , height) * 0.021
        self.application_number_font_size = min(width , height) * 0.051
    
        self.copy_icon_size = min(width , height) * 0.04

        brad = min(width, height) * 0.01
        if brad > 10:
            brad = 10
        self.button_radius = [brad, brad, brad, brad]
        

        print(f"width: {width}, height: {height}, rad: {height}")
 
    def on_open(self):
        anim = Animation(opacity=1, d=0.3)
        anim.bind(on_start=self.update_sizing)
        anim.start(self)
        return super().on_open()

    def on_pre_dismiss(self):
        self.opacity = 0
        return super().on_pre_dismiss()
    



kv_application_number_modal = '''
<ApplicationNumberModal>: 
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
        orientation: 'vertical'
        pos_hint: {'center_x': 0.5,'center_y': 0.5}
        size_hint: 0.85, 0.33
        md_bg_color: chex('#352F44')
        radius: root.content_background_radius 

        
        Widget:
            size_hint: 1, .1
        
        Label:
            size_hint: 1, .1
            pos_hint: {'x': 0.05} 
            text: "Your Application Number"
            color: chex("#FFFFFF")
            font_name: 'p_semibold' 
            text_size: self.size
            halign: 'left'
            valign: 'middle'
            font_size: root.h1_font_size

        
        Label:
            size_hint: 0.87, .17
            pos_hint: {'x': 0.05} 
            text: root.content_text
            color: chex("#FFFFFF")
            font_name: 'p_extralight' 
            text_size: self.size
            halign: 'left'
            valign: 'top'
            font_size: root.h2_font_size
            markup: True
        
        MDBoxLayout:
            size_hint: 1, .1

            Widget:
                size_hint: 0.85, 1
            
                
            

            AppButton:
                md_bg_color: chex("#352F44")
                size_hint: None, 1
                adaptive_width: True
                radius: [0]

                Label:
                    size_hint: None , 1 
                    text: root.copy_text
                    font_size: root.h3_font_size
                    color: chex("#B9B4C7")
                    font_name: "p_light"
                    text_size: None, self.height
                    halign: "right"
                    valign: "middle" 
                    width: self.texture_size[0]


                Image:
                    source: root.copy_icon
                    size_hint: None, None
                    size: root.copy_icon_size, root.copy_icon_size
                    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                    allow_stretch: True
                    keep_ratio: False


            Widget:
                size_hint: 0.15, 1
                

        BoxLayout:
            size_hint: 1, .25
            orientation: 'horizontal'

            Widget:
                size_hint: 0.15, 1

            AppButton:
                size_hint: 0.7, 1
                md_bg_color: chex("#5C5470")
                radius: root.content_background_radius

                Label:
                    size_hint: 1, 1
                    text: root.application_number
                    font_size: root.application_number_font_size
                    font_name: "p_semibold"


            Widget:
                size_hint: 0.15, 1

        
        Widget:
            size_hint: 1, .1
        
        AppButton:
            size_hint: 1, .1 
            adaptive_width: True
            orientation: "horizontal"
            md_bg_color: chex("#F98585")
            radius: root.button_radius
            pos_hint: {"right": 0.9}

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
            size_hint: 1, .08

'''



