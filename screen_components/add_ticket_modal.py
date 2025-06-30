from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.modalview import ModalView

from kivy.animation import Animation
from kivymd.app import MDApp
import os

from kivy.properties import ObjectProperty, NumericProperty, StringProperty, BooleanProperty
 
from kivy.uix.dropdown import DropDown

from screen_components import app_button

from kivy.utils import get_color_from_hex
from kivymd.uix.boxlayout import MDBoxLayout 
from kivymd.uix.behaviors import CommonElevationBehavior, RectangularRippleBehavior
from kivy.properties import ListProperty
from kivy.core.window import Window

from kivy.clock import Clock
from variables import *


class AddTicketModalDetailsTextInput(
    # CommonElevationBehavior,
    # RectangularRippleBehavior,
    MDBoxLayout):
    content_background_radius = ListProperty([ 8 , 8, 8 , 8 ])
    details_font_size = NumericProperty(0)

    text_input = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = get_color_from_hex("#352F44")

    
    def update_sizing(self, *args):
        width, height = self.size
        self.details_font_size = int(min(width, height) * 0.05)
        # print(f"width: {width}, height: {height}, font_size: {self.details_font_size}")

    def get_text(self):
        if self.text_input is None:
            return ""
        return self.text_input.text

    def clear_text(self):
        if self.text_input is None:
            return
        self.text_input.text = ""

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

    selected_plan = StringProperty("Click here to select plan") # This is the id of the plan 
    selected_value = StringProperty("None")

    is_fill_form = BooleanProperty(False)
    is_open = BooleanProperty(False)
    is_button_clicked = BooleanProperty(False)
    # drop_down_max_height = NumericProperty(150)


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
        print("instance ", instance.children[0].children)
        self.selected_plan = value.text
        self.selected_value = value.value
        print(f"Selected option: {value.text}")
        print(value)
        pass 

    def update_sizing(self, *args):
        width, height = Window.size
        self.h1_font_size = int(min(width, height) * 0.05)
        self.h2_font_size = int(min(width, height) * 0.04)
        self.widget_height_2 = int(min(width, height) * 0.009)
        self.widget_height_34 = int(min(width, height) * 0.12)

        if self.dropdown is not None:
            self.dropdown.max_height = int(width * 0.38)

        self.details_input.update_sizing()
 
    
    def on_open(self):
        anim = Animation(opacity=1, d=0.3)
        anim.bind(on_start=self.update_sizing)
        anim.start(self) 
        self.is_open = True
        Clock.schedule_interval(self.realtime_data_checker, 0.1)
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
           
        self.update_sizing()

    def on_pre_dismiss(self):
        self.opacity = 0
        self.is_open = False
        self.is_button_clicked = False
        self.selected_value = "None"
        self.selected_plan = "Click here to select plan"
        if self.details_input is not None:
            self.details_input.clear_text()
        return super().on_pre_dismiss()
    
    def realtime_data_checker(self, *args):
        
        if self.details_input is None:
            self.is_fill_form = False

        elif self.selected_value == "None" or self.details_input.get_text() == "":
            # print("The input is empty")
            self.is_fill_form = False
            self.submit_btn.disabled = True
            self.submit_btn.opacity = 0.8
            self.submit_btn.elevation_level = 0
            self.submit_btn.shadow_offset = (0, 0)
            self.submit_btn.shadow_softness = 0

        else:
            # print("The input is not empty")
            self.is_fill_form = True
            self.submit_btn.disabled = False
            self.submit_btn.opacity = 1
            self.submit_btn.elevation_level = 2
            self.submit_btn.shadow_offset = (0, -3)
            self.submit_btn.shadow_softness = 12 

        return self.is_open

    def activate_events(self):
        if not self.is_fill_form or self.is_button_clicked:
            return
        self.is_button_clicked = True
        main_app  = MDApp.get_running_app()
        key = UPLOAD_TICKET_KEY
        action = "add_ticket"
        need_data = {
            "plan_id": self.selected_value,
            "details": self.details_input.get_text()
        }
        main_app.communications.post_data_action(need_data , key, action)
        self.dismiss() 
        main_app.process_modal.open()
        main_app.process_modal.proccess_text = "Please wait while we report your ticket . . ."

        def check_response(*args): 
            com_data = main_app.communications.get_and_remove(key)
            if com_data is None: 
                print("No data received")
                return True
            
            if not com_data.get('result'):
                print(f'Error: {com_data.get("message", None)}')   
                def display_error(*args):
                    main_app.process_modal.display_error(com_data.get('message', None))
                Clock.schedule_once(display_error, 1) 
                self.is_button_clicked = False
                return False
            message = com_data.get("message", "Sucessfully submitted your ticket report, please wait for a response")
            main_app.process_modal.display_success(message=message, with_dismiss=True)

            return False
         
        Clock.schedule_interval(check_response, 1)





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
                on_release: root.activate_events()
                
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

    text_input : text_input
    
    TextInput:
        id: text_input
        size_hint: 1, 1
        hint_text: "Provide additional information about the problem . . ." 
        multiline: True 
        background_color: 0, 0, 0, 0  # Transparent
        foreground_color: chex("#FFFFFF")  # This is the actual text color
        cursor_color: 1, 1, 1, 1
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