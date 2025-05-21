

from kivy.uix.accordion import ObjectProperty, BooleanProperty
from kivy.uix.modalview import ModalView

from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout

import os

from kivy.properties import ObjectProperty, NumericProperty, StringProperty



class LogoutModal(ModalView):
    
    setup_font_size = NumericProperty(14)
    main_layout : BoxLayout = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_font_size = 14
        
        Clock.schedule_once(self.update_sizing, 0.1)
        self.bind(size=self.update_sizing)
        
    
    def update_sizing(self, *args):
        width, height = self.size
        self.setup_font_size = min(width, height) * 0.035
        
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
        orientation:'vertical'
        padding: 20
        spacing: 10
        size_hint: 0.85 , 0.3
        pos_hint: { 'center_x': 0.5 , 'center_y': 0.5 }  


        canvas.before:
            Color:
                rgba: chex("#F7EEDD")
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [10]

        
    
'''

