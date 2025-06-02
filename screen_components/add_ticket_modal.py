from kivy.uix.actionbar import Button
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
from kivy.uix.dropdown import DropDown

from screen_components import app_button

from kivy.utils import get_color_from_hex

class DropdownButton(app_button.AppButton):
    text = StringProperty("Plan 1")
    text_font_size = NumericProperty(16)
    value = StringProperty("Plan 1")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = get_color_from_hex("#5C5470")
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
            Animation(opacity=1, elevation=4, d=0.3).start(self)
    
    def update_sizing(self, *args):
        width, height = self.size
        self.text_font_size = int(min(width, height) * 0.3)
        print(f"width: {width}, height: {height}, text_font_size: {self.text_font_size}, result : {min(width, height)}")

class AddTicketModal(ModalView):

    h2_font_size = NumericProperty(16)
    h1_font_size = NumericProperty(20)
    main_layout = ObjectProperty()

    dropdown_btn : app_button.AppButton = ObjectProperty(None)
    selected_plan = StringProperty("Click Here")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dropdown = DropDown(max_height=150)

        # Create dropdown options
        for option in ["Click Here", "Option 1", "Option 2", "Option 3", "Option 4"]:
            widget = Widget(size_hint_y=None, height=2)
            self.dropdown.add_widget(widget)
            btn = DropdownButton(size_hint_y=None, height=34)
            btn.text = option
            btn.value = option
            btn.bind(on_release=lambda btn: self.dropdown.select(btn))
            self.dropdown.add_widget(btn)

        # Bind button from KV to open dropdown
        self.dropdown_btn.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=self.on_select)
        self.dropdown_btn.update_color("#5C5470")
        

    def on_select(self, instance, value):
        self.selected_plan = value.text
        print(f"Selected option: {value.text}")
        print(value)
        pass
    
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
        self.h1_font_size = int(min(width, height) * 0.05)
        self.h2_font_size = int(min(width, height) * 0.04)


kv_add_ticket_modal = '''
<AddTicketModal>: 
    size_hint: 1, 1
    auto_dismiss: False
    background: ""  # Removes default dim background
    background_color: 0, 0, 0, 0

    dropdown_btn : dropdown_btn

    BoxLayout:
        orientation: "vertical"
        size_hint: 0.85 , 0.65
        pos_hint: { "center_x": 0.5 , "center_y": 0.5 }
        # padding: 20, 20, 20, 20
        id : main_layout

        canvas.before:
            Color:
                rgba : chex("#B9B4C7")
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [20, 20, 20, 20]
                # radius: [0]

        Widget:
            size_hint: 1, 0.05

        Label:
            size_hint: 1, 0.15
            font_size: root.h1_font_size
            text: "Router Repair Request Form"
            color: chex("#5C5470")
            font_name: "p_bold"

        Label:
            size_hint: 1, 0.077
            font_size: root.h2_font_size
            text: "    Select Plan *"
            color: chex("#FFFFFF")
            font_name: "p_medium"
            text_size: self.width, None 
            valign: "middle"  # Or "center"
            halign: "left"  # "left", "right", or "center" depending on your goal
        BoxLayout:
            size_hint: 1, 0.08
            orientation: "horizontal"
            Widget:
                size_hint: 0.1, 1
            AppButton:
                id: dropdown_btn
                Label:
                    size_hint: 0.8, 1
                    text: root.selected_plan
                    font_name: "p_bold"
                    font_size: root.h2_font_size
                    color: chex("#FFFFFF")
            Widget:
                size_hint: 0.1, 1
        Button:
            size_hint: 1, 0.075
        Button:
            size_hint: 1, 0.40
        Button:
            size_hint: 1, 0.1
        Widget:
            size_hint: 1, 0.05

    

<DropdownButton>:
    size_hint_y: None
    height: 36

    Label:
        size_hint: 1, 1
        text: root.text
        font_name: "p_bold"
        font_size: root.text_font_size
        color: chex("#FFFFFF")


'''