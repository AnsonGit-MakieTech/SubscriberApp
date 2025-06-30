from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.modalview import ModalView

from kivy.animation import Animation
from kivymd.app import MDApp
import os

from kivy.properties import ObjectProperty, NumericProperty, StringProperty
 
from kivy.uix.dropdown import DropDown

from screen_components import app_button

from kivy.utils import get_color_from_hex
from kivymd.uix.boxlayout import MDBoxLayout 
from kivymd.uix.behaviors import CommonElevationBehavior, RectangularRippleBehavior
from kivy.properties import ListProperty
from kivy.core.window import Window


class AddTicketModalDetailsTextInput(
    # CommonElevationBehavior,
    # RectangularRippleBehavior,
    MDBoxLayout):
    content_background_radius = ListProperty([ 8 , 8, 8 , 8 ])
    details_font_size = NumericProperty(0)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = get_color_from_hex("#352F44")

    
    def update_sizing(self, *args):
        width, height = self.size
        self.details_font_size = int(min(width, height) * 0.05)
        # print(f"width: {width}, height: {height}, font_size: {self.details_font_size}")


class DropdownButton(app_button.AppButton):
    text = StringProperty("Plan 1")
    text_font_size = NumericProperty(16)
    value = StringProperty("None")

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

class AddTicketModal(ModalView):

    h2_font_size = NumericProperty(16)
    h1_font_size = NumericProperty(20)
    main_layout = ObjectProperty()

    widget_height_2 = NumericProperty(0)
    widget_height_34 = NumericProperty(0)

    details_input : AddTicketModalDetailsTextInput = ObjectProperty(None)
    dropdown_btn : app_button.AppButton = ObjectProperty(None)
    canncel_btn : app_button.AppButton = ObjectProperty(None)
    submit_btn : app_button.AppButton = ObjectProperty(None)

    dropdown : DropDown = ObjectProperty(None)

    selected_plan = StringProperty("Click Here To Select")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.opacity = 0
        self.dropdown = DropDown(max_height=150)   
        self.dropdown_btn.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=self.on_select)
        self.dropdown_btn.update_color("#5C5470")
        self.canncel_btn.update_color("#A30000")
        self.submit_btn.update_color("#5C5470")
     

    def on_select(self, instance, value):
        
        self.selected_plan = value.text
        print(f"Selected option: {value.text}")
        print(value)
        pass 

    def update_sizing(self, *args):
        width, height = Window.size
        self.h1_font_size = int(min(width, height) * 0.05)
        self.h2_font_size = int(min(width, height) * 0.04)
        self.widget_height_2 = int(min(width, height) * 0.009)
        self.widget_height_34 = int(min(width, height) * 0.12)
        self.details_input.update_sizing()
 
    
    def on_open(self):
        anim = Animation(opacity=1, d=0.3)
        anim.bind(on_start=self.update_sizing)
        anim.start(self) 
        return super().on_open()

    def setup_data(self, plans = None):
        if plans is None:
            return
        
        self.dropdown.clear_widgets()
        
        self.update_sizing()
        # Create dropdown options
        for pkey, pvalue in plans.items():
            widget = Widget(size_hint_y=None, height=self.widget_height_2)
            self.dropdown.add_widget(widget)
            btn = DropdownButton(size_hint_y=None, height=self.widget_height_34)
            btn.text = pvalue.get("name") 
            btn.value = pvalue.get("id")
            btn.bind(on_release=lambda btn: self.dropdown.select(btn))
            self.dropdown.add_widget(btn)
            print(f"pkey: {pkey}, pvalue: {pvalue}")
          


    def on_pre_dismiss(self):
        self.opacity = 0
        return super().on_pre_dismiss()
    




kv_add_ticket_modal = '''
<AddTicketModal>: 
    size_hint: 1, 1
    auto_dismiss: False
    background: ""  # Removes default dim background
    background_color: 0, 0, 0, 0

    dropdown_btn : dropdown_btn
    details_input : details_input
    canncel_btn : cancel_btn
    submit_btn : submit_btn

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
            size_hint: 1, 0.02

        Label:
            size_hint: 1, 0.15
            font_size: root.h1_font_size
            text: "Router Repair Request Form"
            color: chex("#26231F")
            font_name: "p_bold"
            text_size: self.width, None 
            valign: "middle"
            halign: "center"

        Label:
            size_hint: 1, 0.077
            font_size: root.h2_font_size
            text: "    Select Plan *"
            color: chex("#5C5470")
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
                size_hint: 0.8, 1
                id: dropdown_btn
                Label:
                    size_hint: 1, 1
                    text: root.selected_plan
                    font_name: "p_bold"
                    font_size: root.h2_font_size
                    color: chex("#FFFFFF")
            Widget:
                size_hint: 0.1, 1
        Label:
            size_hint: 1, 0.075
            font_size: root.h2_font_size
            text: "    Repair Details *"
            color: chex("#5C5470")
            font_name: "p_medium"
            text_size: self.width, None 
            valign: "middle"  # Or "center"
            halign: "left"  # "left", "right", or "center" depending on your goal
        BoxLayout:
            size_hint: 1, 0.40
            orientation: "horizontal"
            
            Widget:
                size_hint: 0.1, 1

            AddTicketModalDetailsTextInput:
                size_hint: 0.8, 1
                id : details_input

            Widget:
                size_hint: 0.1, 1


        Widget:
            size_hint: 1, 0.07


        BoxLayout:
            size_hint: 1, 0.07
            orientation: "horizontal"

            Widget:
                size_hint: 0.1, 1

            AppButton:
                size_hint: 0.3, 1
                id: cancel_btn
                on_release:
                    root.dismiss()

                Label:
                    size_hint: 1, 1
                    text: "Cancel"
                    font_name: "p_bold"
                    font_size: root.h2_font_size
                    color: chex("#FFFFFF")

            Widget:
                size_hint: 0.2, 1

            AppButton:
                size_hint: 0.3, 1
                id: submit_btn
                
                Label:
                    size_hint: 1, 1
                    text: "Submit"
                    font_name: "p_bold"
                    font_size: root.h2_font_size
                    color: chex("#FFFFFF")
            
            Widget:
                size_hint: 0.1, 1

        Widget:
            size_hint: 1, 0.04

            


<AddTicketModalDetailsTextInput>:
    # theme_elevation_level: "Custom"
    # elevation_level: 2
    # theme_shadow_offset: "Custom"
    # shadow_offset: 0, -3
    # theme_shadow_softness: "Custom"
    # shadow_softness: 12
    # shadow_radius: root.content_background_radius
    radius: root.content_background_radius

    TextInput:
        size_hint: 1, 1
        hint_text: "Provide additional information about the problem . . ." 
        multiline: True 
        background_color: 0, 0, 0, 0  # Transparent
        foreground_color: chex("#FFFFFF")  # This is the actual text color
        cursor_color: chex("#26231F")  # Optional, to see the cursor better
        font_name: 'p_regular'
        font_size: root.details_font_size
        padding: [15]  # Add padding for readability 



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