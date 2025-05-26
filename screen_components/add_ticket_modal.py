from kivy.uix.accordion import Widget
from kivy.uix.actionbar import Label
from kivymd.uix.behaviors.ripple_behavior import RoundedRectangle
from kivy.uix.accordion import ObjectProperty, BooleanProperty
from kivy.uix.modalview import ModalView

from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
import os

from kivy.properties import ObjectProperty, NumericProperty, StringProperty

from kivy.graphics import PushMatrix, PopMatrix, Rotate, Translate





class AddTicketModal(ModalView):

    title_font_size = NumericProperty(20)
    main_layout = ObjectProperty()
    
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
        main_app = MDApp.get_running_app()
        width, height = self.size
        self.title_font_size = int(min(width, height) * 0.05)


kv_add_ticket_modal = '''
<AddTicketModal>: 
    size_hint: 1, 1
    auto_dismiss: False
    background: ""  # Removes default dim background
    background_color: 0, 0, 0, 0

    BoxLayout:
        orientation: "vertical"
        size_hint: 0.85 , 0.7
        pos_hint: { "center_x": 0.5 , "center_y": 0.5 }
        # padding: 20, 20, 20, 20
        id : main_layout

        canvas.before:
            Color:
                rgba : chex("#B9B4C7")
            RoundedRectangle:
                pos: self.pos
                size: self.size
                # radius: [20, 20, 20, 20]
                radius: [0]

        Widget:
            size_hint: 1, 0.05

        Label:
            size_hint: 1, 0.15
            font_size: root.title_font_size
            text: "Router Repair Request Form"
            color: chex("#5C5470")
            font_name: "p_bold"

        Button:
            size_hint: 1, 0.075

        Button:
            size_hint: 1, 0.1
        Button:
            size_hint: 1, 0.075
        Button:
            size_hint: 1, 0.40
        Button:
            size_hint: 1, 0.1
        Widget:
            size_hint: 1, 0.05

        
        


'''