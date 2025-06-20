
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


class NextStepModal(ModalView):
    content_background_radius = ListProperty([ 8 , 8, 8 , 8 ])
    h1_font_size = NumericProperty(30)
    h2_font_size = NumericProperty(20)

    button_spacing = NumericProperty(20)
    button_size = NumericProperty(200)
    button_icon_size = NumericProperty(100)
    button_radius = ListProperty([ 8 , 8, 8 , 8 ])
    
    online_icon = StringProperty('')
    online_unselected_icon = StringProperty('')
    visit_icon = StringProperty('')
    visit_unselected_icon = StringProperty('')
    is_pay_online_selected = BooleanProperty(True)

    online_text = StringProperty('Finish your application instantly with secure online payment.')
    visit_text = StringProperty('Generate an application number now and bring it to our office to pay in person.')
    proceed_text = StringProperty('Proceed to Payment')

    content_text = StringProperty("      Decide how you'd like to complete your application" )
    

    button_action_for_online = ObjectProperty(None)
    button_action_for_visit = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.opacity = 0
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        self.visit_icon = os.path.join(parent_dir, 'assets', 'intro_visit_icon.png')
        self.visit_unselected_icon = os.path.join(parent_dir, 'assets', 'intro_visit_unselect_icon.png')
        self.online_icon = os.path.join(parent_dir, 'assets', 'pay_online_icon.png')
        self.online_unselected_icon = os.path.join(parent_dir, 'assets', 'pay_online_unselect_icon.png')
         
    
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

        self.button_spacing = int(min(width, height) * 0.08)
        self.button_size = int(min(width, height) * 0.2)
        self.button_icon_size = min(width, height) * 0.08
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
    
    def select_pay_online(self, *args):
        self.is_pay_online_selected = True 
        self.proceed_text = 'Proceed to Payment'
        print("select_pay_online")
    
    def select_visit(self, *args):
        self.is_pay_online_selected = False 
        self.proceed_text = 'Generate Application Number'
        print("select_visit")

    
    def activate_event(self, *args):
        if self.is_pay_online_selected:
            self.button_action_for_online()
        else:
            self.dismiss()
            self.button_action_for_visit()

            

kv_next_step_modal = '''
<NextStepModal>: 
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
        size_hint: 0.85, 0.33
        md_bg_color: chex("#352F44")
        radius: root.content_background_radius 


        Widget:
            size_hint: 1, .1

        Label:
            size_hint: 1, .1
            text: "         Choose Your Next Step" 
            color: chex("#FFFFFF")
            font_name: "p_semibold" 
            text_size: self.size
            halign: "left"
            valign: "middle"
            font_size: root.h1_font_size

        Label:
            size_hint: 1, .07
            text: root.content_text
            color: chex("#FFFFFF")
            font_name: "p_extralight" 
            text_size: self.size
            halign: "left"
            valign: "middle"
            font_size: root.h2_font_size
 
        FloatLayout:
            size_hint: 1, .4 

            BoxLayout:
                size_hint: (1, None)
                height: root.button_size
                orientation: "horizontal"
                pos_hint: {"center_x" : 0.5, "center_y" : 0.5}
                spacing: root.button_spacing

                Widget:
                    
                AppButton:
                    size_hint: (None , None)
                    size: (root.button_size , root.button_size)
                    md_bg_color: chex("#B9B4C7") if root.is_pay_online_selected else chex("#5C5470")
                    radius: root.button_radius
                    on_release: root.select_pay_online()

                    FloatLayout:
                        
                        Image:
                            id: test_image
                            source: root.online_icon if root.is_pay_online_selected else root.online_unselected_icon
                            allow_stretch: True
                            keep_ratio: True
                            pos_hint: {"center_x" : 0.5, "center_y" : 0.5}
                            size_hint: (None , None)
                            size: root.button_icon_size, root.button_icon_size

                        Label: 
                            size_hint: 1 , 0.1 
                            text: "Pay Online"
                            font_size: root.h2_font_size
                            color: chex("#352F44") if root.is_pay_online_selected else chex("#B9B4C7")
                            font_name: "p_medium" 
                            pos_hint: {"center_x": 0.5 , "y" : 0.1}
                
                AppButton:
                    size_hint: (None , None)
                    size: (root.button_size , root.button_size)
                    md_bg_color: chex("#B9B4C7") if not root.is_pay_online_selected else chex("#5C5470")
                    radius: root.button_radius
                    on_release: root.select_visit()

                    FloatLayout:
                        
                        Image:
                            source: root.visit_unselected_icon if not root.is_pay_online_selected else root.visit_icon
                            allow_stretch: True
                            keep_ratio: True
                            pos_hint: {"center_x" : 0.5, "center_y" : 0.5}
                            size_hint: (None , None)
                            size: root.button_icon_size, root.button_icon_size

                        Label: 
                            size_hint: 1 , 0.1 
                            text: "Visit Office"
                            font_size: root.h2_font_size
                            color: chex("#352F44") if not root.is_pay_online_selected else chex("#B9B4C7")
                            font_name: "p_medium" 
                            pos_hint: {"center_x": 0.5 , "y" : 0.1}

                    
                
                Widget:

        Label:
            pos_hint: {"center_x": 0.5}
            size_hint: 0.9, .15
            text: root.online_text if root.is_pay_online_selected else root.visit_text
            color: chex("#FFFFFF")
            font_name: "p_extralight" 
            text_size: self.size
            halign: "center"
            valign: "middle"
            font_size: root.h2_font_size

        Widget:
            size_hint: 1, .02

        AppButton:
            size_hint: None, .1
            adaptive_width: True
            orientation: "horizontal"
            md_bg_color: chex("#F98585")
            radius: root.button_radius
            pos_hint: {"right": 0.95}
            on_release: root.activate_event()

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
            size_hint: 1, .06
 


'''



