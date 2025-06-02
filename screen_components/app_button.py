
from kivy.properties import  StringProperty , ListProperty
from kivymd.uix.behaviors import CommonElevationBehavior 
from kivymd.uix.boxlayout import MDBoxLayout 
from kivy.animation import Animation 

 
from kivy.utils import get_color_from_hex

from kivy.uix.behaviors import ButtonBehavior

from kivymd.uix.behaviors import CommonElevationBehavior, RectangularRippleBehavior
 
from kivy.uix.behaviors import ButtonBehavior 

class AppButton(
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

    def update_color(self, color):
        self.md_bg_color = get_color_from_hex(color)

kv_app_button = '''
<AppButton>:
    opacity: 0
    theme_elevation_level: "Custom"
    elevation_level: 2
    theme_shadow_offset: "Custom"
    shadow_offset: 0, -3
    theme_shadow_softness: "Custom"
    shadow_softness: 12
    shadow_radius: root.content_background_radius
    radius: root.content_background_radius


'''