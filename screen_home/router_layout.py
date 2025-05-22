from kivy.uix.actionbar import Label


from kivy.properties import ObjectProperty, NumericProperty, StringProperty , ListProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.behaviors import BackgroundColorBehavior, CommonElevationBehavior
from kivymd.uix.widget import MDWidget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.animation import Animation
from kivy.clock import Clock
import os


from screen_components import section_icon
from kivy.utils import get_color_from_hex

from kivy.uix.behaviors import ButtonBehavior

from kivymd.uix.behaviors import CommonElevationBehavior, RectangularRippleBehavior

from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior






class PlansAddsOnsWidget(
    CommonElevationBehavior,
    RectangularRippleBehavior,
    ButtonBehavior,
    MDBoxLayout
):
    content_background_radius = ListProperty([ 8 , 8, 8 , 8 ])
    widget_type = StringProperty("addons") 

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = get_color_from_hex("#FAF0E6")
        self.opacity = 0
        self.elevation = 0

    def on_parent(self, instance, value):
        # Widget is now attached to the tree
        if value:
            # Animate appearance
            Animation(opacity=1, elevation=4, d=0.3).start(self)

class PlansInstallmentWidget(
    CommonElevationBehavior,
    RectangularRippleBehavior,
    ButtonBehavior,
    MDBoxLayout
):
    content_background_radius = ListProperty([ 8 , 8, 8 , 8 ])
    widget_type = StringProperty("addons") 

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = get_color_from_hex("#FAF0E6")
        self.opacity = 0
        self.elevation = 0

    def on_parent(self, instance, value):
        # Widget is now attached to the tree
        if value:
            # Animate appearance
            Animation(opacity=1, elevation=4, d=0.3).start(self)

class AdditionalPlanList(ScrollView):
    
    plan_list_container : MDBoxLayout = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    
    


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
        self.opacity = 0
        self.elevation = 0

    def on_parent(self, instance, value):
        # Widget is now attached to the tree
        if value:
            # Animate appearance
            Animation(opacity=1, elevation=4, d=0.3).start(self)
    
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
        self.opacity = 0
        self.elevation = 0

    def on_parent(self, instance, value):
        # Widget is now attached to the tree
        if value:
            # Animate appearance
            Animation(opacity=1, elevation=4, d=0.3).start(self)
    
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
        self.opacity = 0
        self.elevation = 0

    def on_parent(self, instance, value):
        # Widget is now attached to the tree
        if value:
            # Animate appearance
            Animation(opacity=1, elevation=4, d=0.3).start(self)

    def update_sizing(self, *args):
        width, height = self.size
        r = min(width, height) * 0.045
        self.content_background_radius = [r, r, r, r]


class ListOfPlans(ScrollView):
    container_layout : BoxLayout = ObjectProperty(None)




class AdditionalPlansList(MDBoxLayout):


    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)









class RouterLayout(MDBoxLayout):
    content_background_radius = ListProperty([ 8 , 8, 8 , 8 ])

    router_icon : section_icon.SectionIconLayout = ObjectProperty(None)
    selected_plan_layout : MDBoxLayout = ObjectProperty(None)
    additional_plans_list : AdditionalPlansList = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(size=self.update_sizing)
        Clock.schedule_once(self.update_sizing, 0.1)  # Delay to ensure size is ready

        Clock.schedule_once(self.setup_image, 1)
        Clock.schedule_once(self.open_selected_layout, 8)

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

    def open_selected_layout(self, *args):
        anime = Animation(height=180,  duration=0.3)
        anime.bind(on_complete=self.on_animation_complete)
        anime.start(self.selected_plan_layout)
    
    def on_animation_complete(self, *args):
        if len(self.selected_plan_layout.children) < 1:
            self.additional_plans_list = AdditionalPlansList()
            self.selected_plan_layout.add_widget(self.additional_plans_list)


kv_router_layout = '''
<RouterLayout>:
    orientation: "vertical"
    size_hint: 1, None
    adaptive_height: True

    router_icon : router_icon
    selected_plan_layout : selected_plan_layout

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
            font_size: 10
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

    
    MDBoxLayout:
        id: selected_plan_layout
        size_hint: 1, None
        height: 0


        # AdditionalPlansList:






<AdditionalPlansList>:
    size_hint: 1, None
    orientation: "vertical"
    height: 180
    
    Widget:
        size_hint: 1, 0.05

    BoxLayout:
        size_hint: 1, 0.10
        orientation: "horizontal"
        Widget:
            size_hint: 0.05, 1
        Label:
            size_hint: 0.95, 1
            font_name: "p_light"
            font_size: 8
            color: chex("#FFFFFF")
            text: "[font=p_bold]Selected Plan :[/font]   Home Plan"
            halign: "left"
            valign : "center"
            text_size: self.size
            markup: True
    
    Widget:
        size_hint: 1, 0.05

    BoxLayout:
        size_hint: 1, 0.7

        Widget:
            size_hint: 0.05, 1

        BoxLayout:
            size_hint: 0.44, 1
            orientation: "vertical"
            
            Label:
                size_hint: 1, 0.1
                font_name: "p_bold"
                font_size: 6
                color: chex("#FFFFFF")
                text: "Available Add-ons Plan"
                halign: "left"
                valign : "center"
                text_size: self.size
                markup: True
            
            Widget:
                size_hint: 1, 0.05

            AdditionalPlanList:
                size_hint: 1, 0.85


        Widget:
            size_hint: 0.02, 1

        BoxLayout:
            size_hint: 0.44, 1
            orientation: "vertical"

            Label:
                size_hint: 1, 0.1
                font_name: "p_bold"
                font_size: 6
                color: chex("#FFFFFF")
                text: "Available Add-ons Plan"
                halign: "left"
                valign : "center"
                text_size: self.size
                markup: True
            
            Widget:
                size_hint: 1, 0.05

            AdditionalPlanList:
                size_hint: 1, 0.85


        Widget:
            size_hint: 0.05, 1

    Widget:
        size_hint: 1, 0.1


<AdditionalPlanList>:
    do_scroll_x: False
    do_scroll_y: True
    bar_width: 0  # Optional: hide bar

    plan_list_container: plan_list_container

    MDBoxLayout:
        id: plan_list_container
        orientation: "vertical"
        size_hint: (1, None)
        adaptive_height: True
        spacing: 5

        PlansInstallmentWidget:
        PlansAddsOnsWidget:
        

<PlansAddsOnsWidget>:
    size_hint: 1, None
    adaptive_height: True
    orientation: "vertical"
    opacity: 0
    
    theme_elevation_level: "Custom"
    elevation_level: 2
    theme_shadow_offset: "Custom"
    shadow_offset: 0, -3
    theme_shadow_softness: "Custom"
    shadow_softness: 12
    shadow_radius: root.content_background_radius
    radius: root.content_background_radius
    padding: 15, 5

    Widget:
        size_hint: 1, None
        height: 7
    Label:
        size_hint_y: None
        text_size: self.width, None  # Enables wrapping
        height: self.texture_size[1]  # Auto height based on wrapped content
        font_name: "p_light"
        font_size: 8
        color: chex("#352F44")
        text: "Home Plan Add Ons"
        halign: "left"
        valign: "middle"
        markup: True

    Widget:
        size_hint: 1, None
        height: 5

    Label:
        size_hint_y: None
        text_size: self.width, None  # Enables wrapping
        height: self.texture_size[1]  # Auto height based on wrapped content
        font_name: "p_light"
        font_size: 8
        color: chex("#352F44")
        text: "[font=p_bold]Monthly:[/font] P 1,500"
        halign: "left"
        valign: "middle"
        markup: True

    Widget:
        size_hint: 1, None
        height: 7


<PlansInstallmentWidget>:
    size_hint: 1, None
    adaptive_height: True
    orientation: "vertical"
    
    theme_elevation_level: "Custom"
    elevation_level: 2
    theme_shadow_offset: "Custom"
    shadow_offset: 0, -3
    theme_shadow_softness: "Custom"
    shadow_softness: 12
    shadow_radius: root.content_background_radius
    radius: root.content_background_radius
    padding: 15, 5

    Widget:
        size_hint: 1, None
        height: 7
    Label:
        size_hint_y: None
        text_size: self.width, None  # Enables wrapping
        height: self.texture_size[1]  # Auto height based on wrapped content
        font_name: "p_light"
        font_size: 8
        color: chex("#352F44")
        text: "Home Plan Add Ons"
        halign: "left"
        valign: "middle"
        markup: True

    Widget:
        size_hint: 1, None
        height: 5

    Label:
        size_hint_y: None
        text_size: self.width, None  # Enables wrapping
        height: self.texture_size[1]  # Auto height based on wrapped content
        font_name: "p_light"
        font_size: 8
        color: chex("#352F44")
        text: "[font=p_bold]Monthly:[/font] P 1,500"
        halign: "left"
        valign: "middle"
        markup: True

    Widget:
        size_hint: 1, None
        height: 5

    Label:
        size_hint_y: None
        text_size: self.width, None  # Enables wrapping
        height: self.texture_size[1]  # Auto height based on wrapped content
        font_name: "p_light"
        font_size: 8
        color: chex("#352F44")
        text: "[font=p_bold]Months To Pay:[/font] 11"
        halign: "left"
        valign: "middle"
        markup: True

    Widget:
        size_hint: 1, None
        height: 5

    Label:
        size_hint_y: None
        text_size: self.width, None  # Enables wrapping
        height: self.texture_size[1]  # Auto height based on wrapped content
        font_name: "p_light"
        font_size: 8
        color: chex("#352F44")
        text: "[font=p_bold]Months Remaining[/font] 11"
        halign: "left"
        valign: "middle"
        markup: True

    Widget:
        size_hint: 1, None
        height: 5

    Label:
        size_hint_y: None
        text_size: self.width, None  # Enables wrapping
        height: self.texture_size[1]  # Auto height based on wrapped content
        font_name: "p_light"
        font_size: 8
        color: chex("#352F44")
        text: "[font=p_bold]Total Amount:[/font] P 1,500"
        halign: "left"
        valign: "middle"
        markup: True

    Widget:
        size_hint: 1, None
        height: 7


    

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
        pos_hint: {"center_x": 0.5,"center_y": 0.5}
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
                font_name: "p_light"
                font_size: 7
                color: chex("#352F44")
                text: "    [font=p_regular]Monthly:[/font] P 1,500"
                halign: "left"
                valign: "middle" 
                text_size: self.size
                markup: True
        
    PlanClickableImage:
        id: view_icon
        size_hint: None, None
        height: 13
        width: 13
        pos_hint: {"right": 0.95,"y": 0.05}
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