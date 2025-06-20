
from kivy.properties import ObjectProperty, NumericProperty, StringProperty , ListProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import Clock
from kivymd.app import MDApp 
import os

from screen_components import section_icon
from kivy.core.window import Window

class HeadlineLayout(MDBoxLayout):
    content_background_radius = ListProperty([ 8 , 8, 8 , 8 ])

    ticket_icon : section_icon.SectionIconLayout = ObjectProperty(None)
    wallet_icon : section_icon.SectionIconLayout = ObjectProperty(None)
    has_pending_ticket = BooleanProperty(False)

    ticket_number = StringProperty("It's Empty!")
    ticket_type = StringProperty("EMPTY")
    ticket_status = StringProperty("EMPTY")
    wallet_balance = StringProperty("P 0.00")
    unpaid_balance = StringProperty("P 0.00")

    widget_height_5 = NumericProperty(0)
    widget_height_7 = NumericProperty(0)
    widget_height_8 = NumericProperty(0)
    widget_height_10 = NumericProperty(0)
    widget_height_13 = NumericProperty(0)
    widget_height_15 = NumericProperty(0)
    widget_height_20 = NumericProperty(0)
    widget_height_35 = NumericProperty(0)

 


    def __init__(self, **kwargs):
        super().__init__(**kwargs) 
     
    
    def setup_image(self, *args):
        
        if self.ticket_icon is None:
            Clock.schedule_once(self.setup_image, 0.3)
            return
        if self.wallet_icon is None:
            Clock.schedule_once(self.setup_image, 0.3)
            return
        
        
        width , height = Window.size
        self.ticket_icon.update_sizing(width, height)
        self.wallet_icon.update_sizing(width, height)
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        self.ticket_icon.sec_icon = os.path.join(parent_dir, 'assets', 'ticket_icon.png')
        self.wallet_icon.sec_icon = os.path.join(parent_dir, 'assets', 'wallet_icon.png')
        # for key, widget in self.ids.items():
        #     print(f"id: {key}, widget: {widget}")

        def additional_event(*args):
            print("hello rverny")

        self.wallet_icon.setup_additional(
            main_text= "+Add Credit",
            additional_event= None,
            has_comming_soon=True
        )

        self.ticket_icon.setup_additional(
            main_text= "+Add Ticket",
            additional_event= additional_event,
            has_comming_soon=False
        )

    def update_sizing(self, width, height):  
        self.spacing = max(4, int(min(width, height) * 0.02))  # 3% of width, with min fallback
        r = min(width, height) * 0.025  # You can change 0.05 to any fraction
        self.content_background_radius = [r, r, r, r]
        print(f"width: {width}, height: {height}, spacing")

        width , height = Window.size
        if self.ticket_icon is not None:
            self.ticket_icon.update_sizing(width, height) 
        if self.wallet_icon is not None:
            self.wallet_icon.update_sizing(width, height)
        
        self.widget_height_5 = int(min( width, height) * 0.02)
        self.widget_height_7 = int(min( width, height) * 0.03)
        self.widget_height_8 = int(min( width, height) * 0.035)
        self.widget_height_10 = int(min( width, height) * 0.04)
        self.widget_height_13 = int(min( width, height) * 0.05)
        self.widget_height_15 = int(min( width, height) * 0.055)
        self.widget_height_20 = int(min( width, height) * 0.07)
        self.widget_height_35 = int(min( width, height) * 0.13)
 














































# kv_headline_layout = '''
# <HeadlineLayout>:
#     orientation: 'horizontal'
#     size_hint: 1, None
#     adaptive_height: True

#     wallet_icon : wallet_icon
#     ticket_icon : ticket_icon
    
#     AppButton:
#         orientation: 'vertical'
#         size_hint: 0.5, None
#         adaptive_height: True
#         radius: root.content_background_radius
#         md_bg_color: chex("#5C5470")
#         # canvas.before:
#         #     Color:
#         #         rgba: 
#         #     RoundedRectangle:
#         #         pos: self.pos
#         #         size: self.size
                
        
#         Widget:
#             size_hint: 1, None
#             height: 5

#         SectionIconLayout:
#             id: wallet_icon
#             size_hint: 1, None 

#         Widget:
#             size_hint: 1, None
#             height: 10

#         BoxLayout:
#             size_hint: 1, None
#             height: 15
#             orientation: 'horizontal'

#             Widget:
#                 size_hint: 0.2, 1
            
#             Label:
#                 size_hint: 0.6, 1
#                 text: "UNPAID"
#                 font_name: 'p_bold'
#                 font_size: 7
#                 text_size: self.size
#                 halign: 'left'
#                 valign: 'middle'

#         Label:
#             size_hint: 1, None
#             height: 20
#             text: root.unpaid_balance
#             font_name: 'p_bold'
#             font_size: 13
#             color: chex("#FAF0E6")

#         Widget:
#             size_hint: 1, None
#             height: 5

        
#         BoxLayout:
#             size_hint: 1, None
#             height: 15
#             orientation: 'horizontal'

#             Widget:
#                 size_hint: 0.2, 1
            
#             Label:
#                 size_hint: 0.6, 1
#                 text: "WALLET"
#                 font_name: 'p_bold'
#                 font_size: 5
#                 text_size: self.size
#                 halign: 'left'
#                 valign: 'middle'

#         Label:
#             size_hint: 1, None
#             height: 10
#             text: root.wallet_balance
#             font_name: 'p_bold'
#             font_size: 7
#             color: chex("#FAF0E6")

#         Widget:
#             size_hint: 1, None
#             height: 15


#         Widget:
#             size_hint: 1, None
#             height: 8




    
#     AppButton:
#         orientation: 'vertical'
#         size_hint: 0.5, 1
#         adaptive_height: True
#         radius: root.content_background_radius
#         md_bg_color: chex("#5C5470")
#         # canvas.before:
#         #     Color:
#         #         rgba: chex("#5C5470")
#         #     RoundedRectangle:
#         #         pos: self.pos
#         #         size: self.size
#         #         radius: root.content_background_radius
        
#         Widget:
#             size_hint: 1, None
#             height: 5

#         SectionIconLayout:
#             id: ticket_icon
#             size_hint: 1, None 
    
#         Widget:
#             size_hint: 1, None
#             height: 10

#         BoxLayout:
#             size_hint: 1, None
#             height: 15
#             orientation: 'horizontal'

#             Widget:
#                 size_hint: 0.2, 1
            
#             Label:
#                 size_hint: 0.6, 1
#                 text: root.ticket_status
#                 font_name: 'p_bold'
#                 font_size: 7
#                 text_size: self.size
#                 halign: 'left'
#                 valign: 'middle'
#                 opacity: 1 if root.has_pending_ticket else 0

#         Label:
#             size_hint: 1, None
#             height: 20
#             text: root.ticket_number
#             font_name: 'p_bold'
#             font_size: 13
#             color: chex("#FAF0E6")
        
            
#         Widget:
#             size_hint: 1, None
#             height: 35


#         BoxLayout:
#             size_hint: 1, None
#             height: 10
#             orientation: 'horizontal'

#             Widget:
#                 size_hint: 0.1, 1
            
#             Label:
#                 size_hint: 0.9, 1
#                 text: root.ticket_type
#                 font_name: 'p_bold'
#                 font_size: 6
#                 text_size: self.size
#                 halign: 'left'
#                 valign: 'middle'
#                 color: chex("#FAF0E6")
#                 opacity: 1 if root.has_pending_ticket else 0


#         Widget:
#             size_hint: 1, None
#             height: 8










    
# '''