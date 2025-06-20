 


from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, NumericProperty, StringProperty , ListProperty, BooleanProperty
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior


class CustomClickableLabel(ButtonBehavior, Label):
    pass

class ClickableImage(FloatLayout):
    main_text = StringProperty("+Add New Ticket")
    adaptable_font_size = NumericProperty(0)
    has_comming_soon = BooleanProperty(True)
    additional_event = ObjectProperty(None)
    set_angle = NumericProperty(0)
    clickable_label :  CustomClickableLabel = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.adaptable_font_size = 5
     

    

class SectionIconLayout(BoxLayout):
    sec_icon = StringProperty("")
    clickable_image : ClickableImage = ObjectProperty(None)
    display_additional = BooleanProperty(True)
    is_half_padding_left = BooleanProperty(False)
    image_size = NumericProperty(100)

    def setup_additional(self, main_text , additional_event, has_comming_soon):
        if main_text:
            self.clickable_image.main_text = f"[u]{main_text}[/u]"
        if additional_event:
            self.clickable_image.additional_event = additional_event  
        self.clickable_image.has_comming_soon = has_comming_soon
        self.clickable_image.set_angle = -45 if has_comming_soon else 0

    
    def update_sizing(self, width, height):
        
        self.height = int(min(width, height) * 0.1)
        self.image_size = int(self.height * 0.75)

        if self.clickable_image is not None:
            self.clickable_image.adaptable_font_size = int(min(width, height) * 0.014)

















































# kv_section_layout = '''
# <SectionIconLayout>:
#     height: 30
#     clickable_image : clickable_image

#     Widget:
#         size_hint: (0.1, 1) if not root.is_half_padding_left else (0.05 , 1)
    
#     Image:
#         source: root.sec_icon
#         allow_stretch: True
#         keep_ration: True
#         size_hint: None, 1
#         width: 20
    
#     Widget:
#         size_hint: (0.8, 1) if not root.is_half_padding_left else (0.85 , 1)

#     ClickableImage:
#         id: clickable_image
#         size_hint: None, 1
#         width: 40
#         opacity: 1 if root.display_additional else 0
    
#     Widget:
#         size_hint: 0.1, 1


# <ClickableImage>:
#     clickable_label : clickable_label

#     Label:
#         pos_hint: {'center_x': 0.5,'center_y': 0.5}
#         size_hint: 1, 1
#         font_size: root.adaptable_font_size
#         font_name: "p_bold"
#         text: root.main_text
#         markup: True
#         opacity: 0.7 if root.has_comming_soon else 1
    
#     CustomClickableLabel:
#         id : clickable_label
#         pos_hint: {'center_x': 0.5,'center_y': 0.5}
#         size_hint: 1, 1
#         font_size: root.adaptable_font_size
#         font_name: "p_bold"
#         text: "comming soon"
#         opacity: 1 if root.has_comming_soon else 0

#         on_release: root.additional_event() if root.additional_event else None


#         canvas.before:
#             PushMatrix
#             Rotate:
#                 angle: root.set_angle
#                 origin: self.center
#         canvas.after:
#             PopMatrix


# '''