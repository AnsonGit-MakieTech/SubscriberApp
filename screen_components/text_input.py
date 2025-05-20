from kivy.uix.behaviors.touchripple import Color
from kivy.uix.accordion import ListProperty



from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty, ListProperty





class OneLineInput(TextInput):
    
    setup_font_size = NumericProperty(14)
    background_radius = ListProperty([8, 8, 8, 8]) 
    text_tab_px = NumericProperty(8)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
  
        self.bind(size=self.setup_layout)

    def on_parent(self, instance, parent):
        if parent:
            Clock.schedule_once(self.setup_layout, 0.1)


    def on_kv_post(self, base_widget):
        Clock.schedule_once(self.setup_layout, 0.1)
    
    def setup_layout(self, *args):
        width, height = self.size

        # Adapt font size based on height (safe fallback to 14)
        self.setup_font_size = int(min(width, height) * 0.4)

        # Protect padding from going negative
        vpad = max(0, (height - self.line_height) / 2)
        self.padding = [self.text_tab_px, vpad, self.text_tab_px, vpad]  # Left, Top, Right, Bottom

        # Radius based on smallest side
        r = min(width, height) * 0.2  # You can tweak 0.2 for rounder edges
        self.background_radius = [r, r, r, r]
        self._refresh_text(self.text)



text_input_kv = '''

<OneLineInput>:
    multiline: False 
    background_normal: ''
    background_active: ''
    background_color: (0 , 0 , 0 , 0)
    foreground_color: 1, 1, 1, 1
    cursor_color: 1, 1, 1, 1
    hint_text_color: 1, 1, 1, 0.6
    font_size: root.setup_font_size
    halign: 'left'
    valign: 'middle' 
    text_size: self.size
    canvas.before:
        Color:
            rgba: chex("#5C5470")
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: root.background_radius
        Color:
            rgba: chex("#FFFFFF") 

'''



