from kivy.uix.accordion import ObjectProperty
from kivy.uix.accordion import BooleanProperty
from kivy.uix.behaviors.touchripple import Color
from kivy.uix.accordion import ListProperty

from kivymd.uix.boxlayout import MDBoxLayout 

from kivy.utils import get_color_from_hex

from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty, ListProperty, ObjectProperty
from kivymd.app import MDApp




class OneLineInput(MDBoxLayout):
    
    setup_font_size = NumericProperty(14)
    background_radius = ListProperty([8, 8, 8, 8]) 
    text_tab_px = NumericProperty(10)
    is_password = BooleanProperty(False)
    hint_text = StringProperty("This is a hint")

    # text_input : TextInput = ObjectProperty(None)
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self.md_bg_color = get_color_from_hex("#5C5470") 
    #     Clock.schedule_once(self.setup_layout, 0.1)

    # def on_parent(self, instance, parent):
    #     if parent:
    #         Clock.schedule_once(self.setup_layout, 0.1)

    # def customized(self, color):
    #     self.md_bg_color = get_color_from_hex(color)

    # def on_parent(self, instance, parent):
    #     main_app = MDApp.get_running_app()
        
    #     if parent is None:
    #         if self.update_sizing in main_app.on_size_events_of_all_widgets:
    #             main_app.on_size_events_of_all_widgets.remove(self.update_sizing)
    #     else:
    #         if self.update_sizing not in main_app.on_size_events_of_all_widgets:
    #             main_app.on_size_events_of_all_widgets.append(self.update_sizing)
    #         self.update_sizing()

    # This will be auto-populated via kv binding:
    text_input: TextInput = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Give the background a color so we can see it:
        self.md_bg_color = get_color_from_hex("#5C5470")
        # Schedule layout adjustments once (after kv is applied)
        # Clock.schedule_once(self.setup_layout, 0)
        self.bind(size=self.setup_layout)
    
    def get_text(self):
        return self.text_input.text

    def costumized_input(self, bgcolor = None, hint_text = None, is_password = None):
        if bgcolor:
            self.md_bg_color = get_color_from_hex(bgcolor)
        if hint_text:
            self.hint_text = hint_text
        if is_password is not None:
            self.is_password = is_password

    def setup_layout(self, *args):
        # Make sure our child TextInput actually exists
        ti = self.text_input 
        if not ti:
            # If it isn’t yet set, try again next frame 
            return

        # Now the widget tree is ready, so we can compute:
        w, h = self.size

        # 1) Font size = 40% of the smaller dimension (you can tweak as needed)
        self.setup_font_size = int(min(w, h) * 0.4)

        # 2) Calculate vertical padding:
        line_h = ti.line_height or ti.font_size  # fallback if line_height isn’t ready
        vpad = max(0, (h - line_h) / 2)

        # 3) Apply padding: [left, top, right, bottom]
        ti.padding = [self.text_tab_px, vpad, self.text_tab_px, vpad]

        # 4) Update the radius of the background
        r = min(w, h) * 0.2
        self.background_radius = [r, r, r, r]

        # 5) Force a redraw of the text inside TextInput
        ti._refresh_text(ti.text)  # no argument needed




text_input_kv = '''

<OneLineInput>:
    # This line “hooks” the id into the ObjectProperty
    text_input: text_input
    radius: root.background_radius
    orientation: "vertical"

    TextInput:
        id: text_input
        size_hint: 1, 1
        pos_hint: {"center_x": .5, "center_y": .5}
        multiline: False
        background_normal: ""
        background_active: ""
        background_color: 0, 0, 0, 0
        foreground_color: 1, 1, 1, 1
        cursor_color: 1, 1, 1, 1
        hint_text_color: 1, 1, 1, 0.6
        font_size: root.setup_font_size
        # valign does nothing here—remove it
        # valign: "middle"
        text_size: self.size  # this can stay if you want horizontal alignment
        hint_text: root.hint_text
        password: root.is_password

'''



