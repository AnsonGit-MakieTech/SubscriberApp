from kivy.uix.boxlayout import BoxLayout
from .app_button import AppButton
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.clock import Clock

class HeaderButtons(BoxLayout):
    button_1 : AppButton = ObjectProperty()
    button_2 : AppButton = ObjectProperty()
    
    button_1_text : str = StringProperty("Login Account")
    button_2_text : str = StringProperty("Forgot Account")
    
    button_1_event = ObjectProperty(None)
    button_2_event = ObjectProperty(None)
    
    header_font_size = NumericProperty(14)

    def __init__(self, **kwargs):
        super(HeaderButtons, self).__init__(**kwargs)
    
    def on_parent(self, instance, value):
        if value:
            self.update_ui()
            
    def update_ui(self, *args):
        if self.button_1 is None or self.button_2 is None:
            Clock.schedule_once(self.update_ui, 0.1)
            return
        self.button_1.update_color("#5C5470")
        self.button_2.update_color("#5C5470")
    
    def update_sizing(self, *args):
        width, height = self.size
        self.header_font_size = int(width * 0.03)
        if self.header_font_size > 23:
            self.header_font_size = 23
        


kv_header_buttons = '''
<HeaderButtons>:
    button_1: button_1
    button_2: button_2

    orientation: 'horizontal'
    size_hint: 1, None
    height: 35
    
    Widget:
        size_hint: 0.05, 1
        
    AppButton:
        id: button_1
        size_hint: 0.35, 1
        on_release: root.button_1_event() if root.button_1_event else None
        
        Label:
            size_hint: 1, 1
            text: root.button_1_text
            font_name: "p_bold"
            font_size: root.header_font_size
            
        
    Widget:
        size_hint: 0.2, 1
    
    AppButton:
        id: button_2
        size_hint: 0.35, 1
        on_release: root.button_2_event() if root.button_2_event else None
    
        Label:
            size_hint: 1, 1
            text: root.button_2_text
            font_name: "p_bold"
            font_size: root.header_font_size
            
            
    Widget:
        size_hint: 0.05, 1


'''
