
from kivy.properties import ObjectProperty, NumericProperty, StringProperty , ListProperty
from kivy.uix.boxlayout import BoxLayout 


class HeadlineLayout(BoxLayout):
    pass

kv_headline_layout = '''
<HeadlineLayout>:
    orientation: 'horizontal'
    spacing: 5
    
    BoxLayout:
        size_hint: 0.5, 1
        
    
    
    BoxLayout:
        size_hint: 0.5, 1
    
    
    
'''