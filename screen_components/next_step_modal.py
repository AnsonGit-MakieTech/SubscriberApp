
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.opacity = 0
         
    
    def on_kv_post(self, base_widget):
        Clock.schedule_once(self.update_sizing, 0.1)
        return super().on_kv_post(base_widget)
    
    def update_sizing(self, *args):
        width, height = self.size 
 
    def on_open(self):
        anim = Animation(opacity=1, d=0.3)
        anim.bind(on_start=self.update_sizing)
        anim.start(self)
        return super().on_open()

    def on_pre_dismiss(self):
        self.opacity = 0
        return super().on_pre_dismiss()
    


kv_next_step_modal = '''
<NextStepModal>:


'''



