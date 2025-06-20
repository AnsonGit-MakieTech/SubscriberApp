from kivy.uix.actionbar import Label

from kivy.uix.dropdown import ScrollView


from kivy.properties import ObjectProperty, NumericProperty, StringProperty , ListProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.behaviors import BackgroundColorBehavior, CommonElevationBehavior
from kivymd.uix.widget import MDWidget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp 

from kivy.clock import Clock
import os


from screen_components import section_icon
from kivy.utils import get_color_from_hex

from kivy.uix.behaviors import ButtonBehavior

from kivymd.uix.behaviors import CommonElevationBehavior, RectangularRippleBehavior

from kivy.uix.image import Image 


class AccountInfoWidget(
    CommonElevationBehavior,
    RectangularRippleBehavior,
    ButtonBehavior,
    MDBoxLayout
):
    content_background_radius = ListProperty([ 8 , 8, 8 , 8 ])

    info_1 = StringProperty("[font=p_regular]Account No. :[/font] 10638899")
    info_2 = StringProperty("[font=p_regular]Account No. :[/font] 10638899")
    info_3 = StringProperty("[font=p_regular]Account No. :[/font] 1063889sdfasdffffffff fffffffffffffffffff ffffffffffffffffffffff9")
    info_4 = StringProperty("[font=p_regular]Account No. :[/font] 10638899")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = get_color_from_hex("#FAF0E6")


    
class CostumeSectionIconLayout(BoxLayout):
    sec_icon = StringProperty("")
    clickable_image : section_icon.ClickableImage = ObjectProperty(None)
    display_additional = BooleanProperty(True)
    is_half_padding_left = BooleanProperty(False) 

    def setup_additional(self, main_text , additional_event, has_comming_soon):
        if main_text:
            self.clickable_image.main_text = f"[u]{main_text}[/u]"
        if additional_event:
            self.clickable_image.additional_event = additional_event  
        self.clickable_image.has_comming_soon = has_comming_soon
        self.clickable_image.set_angle = -45 if has_comming_soon else 0

class AccountLayout(MDBoxLayout):
    content_background_radius = ListProperty([ 8 , 8, 8 , 8 ])

    account_icon : section_icon.SectionIconLayout = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Clock.schedule_once(self.update_sizing, 0.1)  # Delay to ensure size is ready

        # Clock.schedule_once(self.setup_image, 1)
    
    
    def on_parent(self, instance, parent):
        main_app = MDApp.get_running_app()
        if parent is None:
            if self.update_sizing in main_app.on_size_events_of_all_widgets:
                main_app.on_size_events_of_all_widgets.remove(self.update_sizing)
        else:
            if self.update_sizing not in main_app.on_size_events_of_all_widgets:
                main_app.on_size_events_of_all_widgets.append(self.update_sizing)
            self.update_sizing()

    def setup_image(self, *args): 
        if self.account_icon is None:
            print(f"Account icon is None")
            # self.account_icon = self.ids.account_icon
            print(f"Ids : {self.ids}")
            Clock.schedule_once(self.setup_image, 0.3)
            return
        print(f"Account icon is not None")
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        self.account_icon.sec_icon = os.path.join(parent_dir, 'assets', 'account_icon.png')
        self.account_icon.display_additional = False
        self.account_icon.is_half_padding_left = True

    def update_sizing(self, *args):
        width, height = self.size
        r = min(width, height) * 0.035  # You can change 0.05 to any fraction
        self.content_background_radius = [r, r, r, r]



kv_account_layout = '''
<AccountLayout>:
    orientation: "vertical"
    size_hint: 1, None
    adaptive_height: True

    account_icon : account_icon

    canvas.before:
        Color:
            rgba: chex("#5C5470")
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: root.content_background_radius
    
    Widget:
        size_hint: 1, None
        height: 15

    CostumeSectionIconLayout:
        id: account_icon
        size_hint: 1, None  
        height: 30
        clickable_image : clickable_image

        Widget:
            size_hint: (0.1, 1) if not self.parent.is_half_padding_left else (0.05 , 1)
        
        Image:
            source: self.parent.sec_icon
            allow_stretch: True
            keep_ration: True
            size_hint: None, 1
            width: 20
        
        Widget:
            size_hint: (0.8, 1) if not self.parent.is_half_padding_left else (0.85 , 1)

        ClickableImage:
            id: clickable_image
            size_hint: None, 1
            width: 40
            opacity: 1 if self.parent.display_additional else 0
        
        Widget:
            size_hint: 0.1, 1
    
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
            text: "Account Information"
            font_name: "p_bold"
            text_size: self.size
            halign: "left"
            valign: "center"

    Widget:
        size_hint: 1, None
        height: 10

    MDBoxLayout:
        size_hint: 1, None
        orientation: 'horizontal'
        adaptive_height: True
        # md_bg_color: chex("#FFFFFF")

        Widget:
            size_hint: 0.1, None
            height: 60
            
        AccountInfoWidget:
            size_hint: 0.8, None

        Widget:
            size_hint: 0.1, None
            height: 60


    Widget:
        size_hint: 1, None
        height: 8
        
    MDBoxLayout:
        size_hint: 1, None
        orientation: 'horizontal'
        adaptive_height: True
        # md_bg_color: chex("#FFFFFF")

        Widget:
            size_hint: 0.1, None
            height: 60
            
        AccountInfoWidget:
            size_hint: 0.8, None

        Widget:
            size_hint: 0.1, None
            height: 60
            
    Widget:
        size_hint: 1, None
        height: 8








<AccountInfoWidget>:
    orientation: "vertical" 
    
    adaptive_height: True

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
        size_hint_y: None
        text_size: self.width, None  # Enables wrapping
        height: self.texture_size[1]  # Auto height based on wrapped content
        font_name: "p_light"
        font_size: 9
        color: chex("#352F44")
        text: root.info_1
        halign: "left"
        valign: "middle"
        markup: True
    
    
    Label:
        size_hint_y: None
        text_size: self.width, None  # Enables wrapping
        height: self.texture_size[1]  # Auto height based on wrapped content
        font_name: "p_light"
        font_size: 9
        color: chex("#352F44")
        text: root.info_2
        halign: "left"
        valign: "middle"
        markup: True
    
        
    Label:
        size_hint_y: None
        text_size: self.width, None  # Enables wrapping
        height: self.texture_size[1]  # Auto height based on wrapped content
        font_name: "p_light"
        font_size: 9
        color: chex("#352F44")
        text: root.info_3
        halign: "left"
        valign: "middle"
        markup: True
    
        
    Label:
        size_hint_y: None
        text_size: self.width, None  # Enables wrapping
        height: self.texture_size[1]  # Auto height based on wrapped content
        font_name: "p_light"
        font_size: 9
        color: chex("#352F44")
        text: root.info_4
        halign: "left"
        valign: "middle"
        markup: True
    

'''