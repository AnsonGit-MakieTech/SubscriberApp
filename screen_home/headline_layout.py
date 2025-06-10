
from kivy.properties import ObjectProperty, NumericProperty, StringProperty , ListProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import Clock
from kivymd.app import MDApp 
import os

from screen_components import section_icon

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


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # self.bind(size=self.update_sizing)
        Clock.schedule_once(self.update_sizing, 0.1)  # Delay to ensure size is ready

        Clock.schedule_once(self.setup_image, 1)
    
    
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

    def update_sizing(self, *args): 
        width, height = self.size
        self.spacing = max(4, int(width * 0.03))  # 3% of width, with min fallback
        r = min(width, height) * 0.045  # You can change 0.05 to any fraction
        self.content_background_radius = [r, r, r, r]





kv_headline_layout = '''
<HeadlineLayout>:
    orientation: 'horizontal'
    size_hint: 1, None
    adaptive_height: True

    wallet_icon : wallet_icon
    ticket_icon : ticket_icon
    
    AppButton:
        orientation: 'vertical'
        size_hint: 0.5, None
        adaptive_height: True
        radius: root.content_background_radius
        md_bg_color: chex("#5C5470")
        # canvas.before:
        #     Color:
        #         rgba: 
        #     RoundedRectangle:
        #         pos: self.pos
        #         size: self.size
                
        
        Widget:
            size_hint: 1, None
            height: 5

        SectionIconLayout:
            id: wallet_icon
            size_hint: 1, None 

        Widget:
            size_hint: 1, None
            height: 10

        BoxLayout:
            size_hint: 1, None
            height: 15
            orientation: 'horizontal'

            Widget:
                size_hint: 0.2, 1
            
            Label:
                size_hint: 0.6, 1
                text: "UNPAID"
                font_name: 'p_bold'
                font_size: 7
                text_size: self.size
                halign: 'left'
                valign: 'middle'

        Label:
            size_hint: 1, None
            height: 20
            text: root.unpaid_balance
            font_name: 'p_bold'
            font_size: 13
            color: chex("#FAF0E6")

        Widget:
            size_hint: 1, None
            height: 5

        
        BoxLayout:
            size_hint: 1, None
            height: 15
            orientation: 'horizontal'

            Widget:
                size_hint: 0.2, 1
            
            Label:
                size_hint: 0.6, 1
                text: "WALLET"
                font_name: 'p_bold'
                font_size: 5
                text_size: self.size
                halign: 'left'
                valign: 'middle'

        Label:
            size_hint: 1, None
            height: 10
            text: root.wallet_balance
            font_name: 'p_bold'
            font_size: 7
            color: chex("#FAF0E6")

        Widget:
            size_hint: 1, None
            height: 15


        Widget:
            size_hint: 1, None
            height: 8




    
    AppButton:
        orientation: 'vertical'
        size_hint: 0.5, 1
        adaptive_height: True
        radius: root.content_background_radius
        md_bg_color: chex("#5C5470")
        # canvas.before:
        #     Color:
        #         rgba: chex("#5C5470")
        #     RoundedRectangle:
        #         pos: self.pos
        #         size: self.size
        #         radius: root.content_background_radius
        
        Widget:
            size_hint: 1, None
            height: 5

        SectionIconLayout:
            id: ticket_icon
            size_hint: 1, None 
    
        Widget:
            size_hint: 1, None
            height: 10

        BoxLayout:
            size_hint: 1, None
            height: 15
            orientation: 'horizontal'

            Widget:
                size_hint: 0.2, 1
            
            Label:
                size_hint: 0.6, 1
                text: root.ticket_status
                font_name: 'p_bold'
                font_size: 7
                text_size: self.size
                halign: 'left'
                valign: 'middle'
                opacity: 1 if root.has_pending_ticket else 0

        Label:
            size_hint: 1, None
            height: 20
            text: root.ticket_number
            font_name: 'p_bold'
            font_size: 13
            color: chex("#FAF0E6")
        
            
        Widget:
            size_hint: 1, None
            height: 35


        BoxLayout:
            size_hint: 1, None
            height: 10
            orientation: 'horizontal'

            Widget:
                size_hint: 0.1, 1
            
            Label:
                size_hint: 0.9, 1
                text: root.ticket_type
                font_name: 'p_bold'
                font_size: 6
                text_size: self.size
                halign: 'left'
                valign: 'middle'
                color: chex("#FAF0E6")
                opacity: 1 if root.has_pending_ticket else 0


        Widget:
            size_hint: 1, None
            height: 8










    
'''