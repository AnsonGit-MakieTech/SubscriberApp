from kivy.uix.filechooser import string_types
from kivy.uix.actionbar import Label
from kivy.uix.accordion import FloatLayout
from kivy.uix.accordion import Widget
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.dropdown import ScrollView


from kivy.properties import ObjectProperty, NumericProperty, StringProperty , ListProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.behaviors import BackgroundColorBehavior, CommonElevationBehavior
from kivymd.uix.widget import MDWidget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.scrollview import ScrollView

from kivy.clock import Clock
import os


from screen_components import section_icon
from kivy.utils import get_color_from_hex

from kivy.uix.behaviors import ButtonBehavior

from kivymd.uix.behaviors import CommonElevationBehavior, RectangularRippleBehavior

from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior


class PlanClickableImage(ButtonBehavior, Image):
    pass


class PlanWidget(
    CommonElevationBehavior,
    RectangularRippleBehavior,
    ButtonBehavior,
    MDFloatLayout
):
    content_background_radius = ListProperty([ 8 , 8, 8 , 8 ])
    plan_icon = StringProperty("")
    view_icon : PlanClickableImage = ObjectProperty(None)
    is_viewing = BooleanProperty(False)
    widget_type = StringProperty("plan")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = get_color_from_hex("#FAF0E6")
        self.bind(size=self.update_sizing)
        Clock.schedule_once(self.update_sizing, 0.1)
        
        Clock.schedule_once(self.update_image, 0.1)
    
    def update_image(self, *args):
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        self.view_icon.source = os.path.join(parent_dir, 'assets', 'plan_not_selected.png')
        for key, widget in self.ids.items():
            print(f"id: {key}, widget: {widget}")

    def update_sizing(self, *args):
        width, height = self.size
        r = min(width, height) * 0.065  # You can change 0.05 to any fraction
        self.content_background_radius = [r, r, r, r]



class AddPlanWidget(
    CommonElevationBehavior,
    RectangularRippleBehavior,
    ButtonBehavior,
    MDBoxLayout
):
    content_background_radius = ListProperty([ 8 , 8, 8 , 8 ])
    add_plan_icon = StringProperty("")
    widget_type = StringProperty("add_plan")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = get_color_from_hex("#FAF0E6")
        self.bind(size=self.update_sizing)

        Clock.schedule_once(self.update_sizing, 0.1)
    
    def on_parent(self, instance, value):
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        self.add_plan_icon = os.path.join(parent_dir, 'assets', 'add_plan.png')

    def update_sizing(self, *args):
        width, height = self.size 
        r = min(width, height) * 0.065  # You can change 0.05 to any fraction
        self.content_background_radius = [r, r, r, r]

class EmptyPlanWidget(
    CommonElevationBehavior,
    RectangularRippleBehavior,
    ButtonBehavior,
    MDBoxLayout
):
    content_background_radius = ListProperty([8, 8, 8, 8])
    widget_type = StringProperty("empty_plan")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = get_color_from_hex("#FAF0E6")
        self.bind(size=self.update_sizing)
        Clock.schedule_once(self.update_sizing, 0.1)

    def update_sizing(self, *args):
        width, height = self.size
        r = min(width, height) * 0.045
        self.content_background_radius = [r, r, r, r]


class ListOfPlans(ScrollView):
    container_layout : BoxLayout = ObjectProperty(None)


class RouterLayout(MDBoxLayout):
    content_background_radius = ListProperty([ 8 , 8, 8 , 8 ])

    router_icon : section_icon.SectionIconLayout = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(size=self.update_sizing)
        Clock.schedule_once(self.update_sizing, 0.1)  # Delay to ensure size is ready

        Clock.schedule_once(self.setup_image, 1)

    def setup_image(self, *args):
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        self.router_icon.sec_icon = os.path.join(parent_dir, 'assets', 'router_icon.png')
        self.router_icon.display_additional = False
        self.router_icon.is_half_padding_left = True

    def update_sizing(self, *args):
        width, height = self.size
        self.spacing = max(4, int(width * 0.03))  # 3% of width, with min fallback
        r = min(width, height) * 0.035  # You can change 0.05 to any fraction
        self.content_background_radius = [r, r, r, r]

 

kv_router_layout = '''
<RouterLayout>:
    orientation: "vertical"
    size_hint: 1, None
    adaptive_height: True

    router_icon : router_icon

    canvas.before:
        Color:
            rgba: chex("#5C5470")
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: root.content_background_radius
    
    Widget:
        size_hint: 1, None
        height: 5

    SectionIconLayout:
        id: router_icon
        size_hint: 1, None 
    
    BoxLayout:
        size_hint: 1, None
        height: 15
        orientation: "horizontal"

        Widget:
            size_hint: 0.05, 1

        Label:
            size_hint: 0.95, 1
            font_size: 7
            color: chex("#FFFFFF")
            text: "All Plans Subscribed"
            font_name: "p_bold"
            text_size: self.size
            halign: "left"
            valign: "center"

    BoxLayout:
        size_hint: 1, None
        height: 80

        Widget:
            size_hint: 0.05, 1

        ListOfPlans:
            size_hint: 0.95, 1
    
    Widget:
        size_hint: 1, None
        height: 10


    

<PlanWidget>:
    size_hint: None, 1
    width: 120

    theme_elevation_level: "Custom"
    elevation_level: 2
    theme_shadow_offset: "Custom"
    shadow_offset: 0, -3
    theme_shadow_softness: "Custom"
    shadow_softness: 12
    shadow_radius: root.content_background_radius
    radius: root.content_background_radius
 
    view_icon : view_icon

    BoxLayout:
        size_hint: 1, 1
        pos_hint: {'center_x': 0.5,'center_y': 0.5}
        orientation: "vertical"

        Label:
            size_hint: 1, 0.2
            font_name: "p_light"
            font_size: 7
            color: chex("#352F44")
            text: "    Registering"
            halign: "left"
            valign: "middle" 
            text_size: self.size
        
        Widget:
            size_hint: 1, 0.15
        
        Label:
            size_hint: 1, 0.3
            font_name: "p_bold"
            font_size: 10
            color: chex("#352F44")
            text: "Home Plan"

        Widget:
            size_hint: 1, 0.15

            
        BoxLayout:
            size_hint: 1, 0.2
            orientation: "horizontal"

            Label:
                size_hint: 1, 1
                font_name: "p_regular"
                font_size: 7
                color: chex("#352F44")
                text: "    Monthly: P 1,500"
                halign: "left"
                valign: "middle" 
                text_size: self.size
        
    PlanClickableImage:
        id: view_icon
        size_hint: None, None
        height: 13
        width: 13
        pos_hint: {'right': 0.95,'y': 0.05}
        opacity: 1 if not root.is_viewing else 0.7

        on_release: root.is_viewing = True



    


<AddPlanWidget>:
    orientation: "vertical"
    size_hint: None, 1
    width: 120
    theme_elevation_level: "Custom"
    elevation_level: 2
    theme_shadow_offset: "Custom"
    shadow_offset: 0, -3
    theme_shadow_softness: "Custom"
    shadow_softness: 12
    shadow_radius: root.content_background_radius
    radius: root.content_background_radius
        


    Widget:
        size_hint: 1, 0.23

    FloatLayout:
        size_hint: 1, 0.3

        Image:
            pos_hint: {"center_x": 0.5,"center_y": 0.5}
            source: root.add_plan_icon
            allow_stretch: True
            keep_ration: True
            size_hint: None, 1
            width: 30
        
    Widget:
        size_hint: 1, 0.05

    Label:
        size_hint: 1, 0.1
        font_name: "p_extralight"
        font_size: 8
        color: chex("#352F44")
        text: "Add New Plan"

    Widget:
        size_hint: 1, 0.22




        

<EmptyPlanWidget>:
    orientation: "vertical"
    size_hint: None, 1
    width: 120

    theme_elevation_level: "Custom"
    elevation_level: 2
    theme_shadow_offset: "Custom"
    shadow_offset: 0, -3
    theme_shadow_softness: "Custom"
    shadow_softness: 12
    shadow_radius: root.content_background_radius
    radius: root.content_background_radius
 

    Widget:
        size_hint: 1, 0.4

    Label:
        size_hint: 1, 0.1
        font_name: "p_bold"
        font_size: 8
        color: chex("#352F44")
        text: "No plan yet?"

    Widget:
        size_hint: 1, 0.05

    Label:
        size_hint: 1, 0.1
        font_name: "p_extralight"
        font_size: 8
        color: chex("#352F44")
        text: "[u]Apply now[/u]"
        markup: True

    Widget:
        size_hint: 1, 0.35

    




<ListOfPlans>:
    do_scroll_x: True
    do_scroll_y: False
    bar_width: 0  # Optional: hide bar

    container_layout : container_layout

    BoxLayout:
        id: container_layout
        orientation: "horizontal"
        size_hint: (None, 1)
        width: self.minimum_width
        spacing: 20  # space between cards
        padding: 10, 5

        PlanWidget:

        EmptyPlanWidget:

        AddPlanWidget:
        













'''