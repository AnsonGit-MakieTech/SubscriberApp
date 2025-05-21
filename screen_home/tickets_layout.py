from kivy.uix.actionbar import Button
from kivy.uix.actionbar import Label


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




class TicketList(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    



class TicketDetailsWidget(
    CommonElevationBehavior,
    RectangularRippleBehavior,
    ButtonBehavior,
    MDBoxLayout
):
    content_background_radius = ListProperty([ 8 , 8, 8 , 8 ])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = get_color_from_hex("#FAF0E6")


class TicketsLayout(MDBoxLayout):
    content_background_radius = ListProperty([ 8 , 8, 8 , 8 ])

    router_icon : section_icon.SectionIconLayout = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(size=self.update_sizing)
        Clock.schedule_once(self.update_sizing, 0.1)  # Delay to ensure size is ready

        Clock.schedule_once(self.setup_image, 1)

    def setup_image(self, *args):
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        self.router_icon.sec_icon = os.path.join(parent_dir, 'assets', 'ticket_icon.png')
        self.router_icon.display_additional = False
        self.router_icon.is_half_padding_left = True

    def update_sizing(self, *args):
        width, height = self.size
        self.spacing = max(4, int(width * 0.03))  # 3% of width, with min fallback
        r = min(width, height) * 0.035  # You can change 0.05 to any fraction
        self.content_background_radius = [r, r, r, r]

kv_tickets_layout = '''
<TicketsLayout>:
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
            size_hint: 0.4, 1
            font_size: 10
            color: chex("#FFFFFF")
            text: "List of Ticket"
            font_name: "p_bold"
            text_size: self.size
            halign: "left"
            valign: "center"

        Widget:
            size_hint: 0.2, None
        
        ClickableLabel:
            size_hint: 0.3, 1
            font_size: 10
            color: chex("#FFFFFF")
            text: "[u]+Add New Ticket[/u]"
            markup: True
            font_name: "p_regular"
            text_size: self.size
            halign: "right"
            valign: "center"

        Widget:
            size_hint: 0.05, 1

            

    BoxLayout:
        size_hint: 1, None
        height: 100
        orientation: "horizontal"

        Widget:
            size_hint: 0.1, 1

        Button:
            size_hint: 0.3, 1
        
        Widget:
            size_hint: 0.05, 1

        TicketDetailsWidget:
            size_hint: 0.45, 1

        Widget:
            size_hint: 0.1, 1
        

    
    Widget:
        size_hint: 1, None
        height: 5 


<TicketList>:



<TicketDetailsWidget>:
    orientation: "vertical" 

    theme_elevation_level: "Custom"
    elevation_level: 2
    theme_shadow_offset: "Custom"
    shadow_offset: 0, -3
    theme_shadow_softness: "Custom"
    shadow_softness: 12
    shadow_radius: root.content_background_radius
    radius: root.content_background_radius
    padding: 10, 10
    spacing: 4

    
    Label:
        size_hint: 1, 0.2
        font_name: "p_bold"
        font_size: 11
        color: chex("#5C5470")
        text: "Ticket Details"
        halign: "left"
        valign: "middle"
        markup: True
        text_size: self.size
    
        
    Label:
        size_hint: 1, 0.2
        font_name: "p_light"
        font_size: 9
        color: chex("#5C5470")
        text: "[font=p_regular]TICKET NO:[/font] 90DFENA6"
        halign: "left"
        valign: "middle"
        markup: True
        text_size: self.width - 20, None 
    
    Label:
        size_hint: 1, 0.2
        font_name: "p_light"
        font_size: 9
        color: chex("#5C5470")
        text: "[font=p_regular]STATUS:[/font] OPEN"
        halign: "left"
        valign: "middle"
        markup: True
        text_size: self.width - 20, None 

    Label:
        size_hint: 1, 0.2
        font_name: "p_light"
        font_size: 9
        color: chex("#5C5470")
        text: "[font=p_regular]TYPE:[/font] REPAIR"
        halign: "left"
        valign: "middle"
        markup: True
        text_size: self.width - 20, None 











'''