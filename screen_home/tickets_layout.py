from kivy.uix.actionbar import Button
from kivy.uix.actionbar import Label


from kivy.properties import ObjectProperty, NumericProperty, StringProperty , ListProperty, BooleanProperty, DictProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.behaviors import BackgroundColorBehavior, CommonElevationBehavior
from kivymd.uix.widget import MDWidget
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.animation import Animation
from kivy.clock import Clock
from kivymd.app import MDApp 
import os


from screen_components import section_icon
from kivy.utils import get_color_from_hex

from kivy.uix.behaviors import ButtonBehavior

from kivymd.uix.behaviors import CommonElevationBehavior, RectangularRippleBehavior

from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

from kivy.core.window import Window


class TicketWidget(
    CommonElevationBehavior,
    RectangularRippleBehavior,
    ButtonBehavior,
    MDBoxLayout
    ):
    
    content_background_radius = ListProperty([ 16 , 16, 16 , 16 ])
    ticket_number = StringProperty("123456789")
    ticket_id = StringProperty("")

    click_event = ObjectProperty(None)
    widget_height_10 = NumericProperty(0) 
    is_selected = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = get_color_from_hex("#FAF0E6")
        
        Clock.schedule_once(self.update_sizing, 0.1)
        self.opacity = 0
        self.elevation = 0

    def update_sizing(self, *args):
        
        width, height = Window.size
        self.height = int(min( width, height) * 0.1)
        self.widget_height_10 = int(min( width, height) * 0.035) 


        width, height = self.size
        r = min(width, height) * 0.2  # You can change 0.05 to any fraction
        self.content_background_radius = [r, r, r, r]

    
    def on_press(self , *args): 
        if self.click_event:
            self.click_event(ticket_id = self.ticket_id, ticketwidget=self)
        
        return super().on_press()

    def on_parent(self, instance, value):
        # Widget is now attached to the tree
        if value:
            # Animate appearance
            Animation(opacity=1, elevation=4, d=0.3).start(self)

class TicketList(ScrollView):

    ticket_container : MDBoxLayout = ObjectProperty(None)

    widget_height_5 = NumericProperty(0) 


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def update_sizing(self, *args):
        width, height = Window.size

        self.widget_height_5 = int(min( width, height) * 0.02) 
        for child in self.ticket_container.children:
            child.update_sizing()
    
    def setup_ui(self, data, click_event):
        first_ticket = None
        self.ticket_container.clear_widgets()
        for tkey , ticket in data.items():
            ticket_widget = TicketWidget()
            ticket_widget.ticket_number = str(ticket.get("ticketnum", "None"))
            ticket_widget.ticket_id = str(ticket.get("id", "None"))
            ticket_widget.click_event = click_event
            self.ticket_container.add_widget(ticket_widget)

            if first_ticket is None:
                first_ticket = ticket_widget

        self.update_sizing()
        if first_ticket is not None:
            first_ticket.click_event(first_ticket.ticket_id, first_ticket)
            
    
    def refresh_widget(self , *args):
        for child in self.ticket_container.children:
            child.is_selected = False



class TicketDetailsWidget(
    CommonElevationBehavior,
    RectangularRippleBehavior,
    ButtonBehavior,
    MDBoxLayout
):
    content_background_radius = ListProperty([ 8 , 8, 8 , 8 ])


    widget_height_4 = NumericProperty(0) 
    widget_height_9 = NumericProperty(0) 
    widget_height_10 = NumericProperty(0) 
    widget_height_11 = NumericProperty(0)  

    ticketstatus_text = StringProperty("[font=p_regular]STATUS:[/font] None")
    tickettype_text = StringProperty("[font=p_regular]TYPE:[/font] None")
    ticketnum_text = StringProperty("[font=p_regular]TICKET NO:[/font] None")



    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = get_color_from_hex("#FAF0E6")

    def update_sizing(self, *args):
        width, height = Window.size

        self.widget_height_4 = int(min( width, height) * 0.02)
        self.widget_height_9 = int(min( width, height) * 0.028)
        self.widget_height_10 = int(min( width, height) * 0.035)
        self.widget_height_11 = int(min( width, height) * 0.037)


        self.padding = [ self.widget_height_10, self.widget_height_10]
        self.spacing = self.widget_height_4
 

        width, height = self.size
        r = min(width, height) * 0.04 # You can change 0.05 to any fraction
        self.content_background_radius = [r, r, r, r]

    def setup_ui(self, tstatus = None, ttype = None, tnum = None):
        self.ticketnum_text = "[font=p_regular]TICKET NO:[/font] " + str(tnum) if tnum else "None"
        self.ticketstatus_text = "[font=p_regular]STATUS:[/font] " + str(tstatus).upper() if tstatus else "None"
        self.tickettype_text = "[font=p_regular]TYPE:[/font] " + str(ttype).upper() if ttype else "None"


class TicketsLayout(MDBoxLayout):
    content_background_radius = ListProperty([ 8 , 8, 8 , 8 ])

    router_icon : section_icon.SectionIconLayout = ObjectProperty(None)
    ticket_list: TicketList = ObjectProperty(None)
    ticket_details : TicketDetailsWidget = ObjectProperty(None)

    widget_height_5 = NumericProperty(0) 
    widget_height_8 = NumericProperty(0)
    widget_height_10 = NumericProperty(0) 
    widget_height_15 = NumericProperty(0) 
    widget_height_100 = NumericProperty(0)

    tickets_data = DictProperty({})
    selected_ticket = DictProperty({})
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs) 
 
    def setup_image(self, *args):
        if self.router_icon is None: 
            Clock.schedule_once(self.setup_image, 0.3)
            return
        width , height = Window.size
        self.router_icon.update_sizing(width, height)
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        self.router_icon.sec_icon = os.path.join(parent_dir, 'assets', 'ticket_icon.png')
        self.router_icon.display_additional = False
        self.router_icon.is_half_padding_left = True
        print("Ticket is ")     

    def update_sizing(self, width, height):
        
        r = min(width, height) * 0.035  # You can change 0.05 to any fraction
        self.content_background_radius = [r, r, r, r]
        
        width , height = Window.size
        if self.router_icon is not None:
            self.router_icon.update_sizing(width, height)
        
        if self.ticket_list is not None:
            self.ticket_list.update_sizing()
        
        if self.ticket_details is not None:
            self.ticket_details.update_sizing()

        self.widget_height_5 = int(min( width, height) * 0.02) 
        self.widget_height_8 = int(min( width, height) * 0.03)
        self.widget_height_10 = int(min( width, height) * 0.04) 
        self.widget_height_15 = int(min( width, height) * 0.055)  
        self.widget_height_100 = int(min( width, height) * 0.4) 


    def click_event(self, ticket_id , ticketwidget):
        print("Ticket is ", ticket_id)
        self.selected_ticket = self.tickets_data.get(ticket_id, {})
        self.ticket_details.setup_ui(
            tstatus=self.selected_ticket.get("ticketstatus", "None"),
            ttype=self.selected_ticket.get("type", "None"),
            tnum=self.selected_ticket.get("ticketnum", "None")
        )
        self.ticket_list.refresh_widget()
        ticketwidget.is_selected = True


    def setup_ui(self, data):

        if self.ticket_details is None or self.ticket_list is None or not data:
            print("Ticket is None or Widget is not loaded")
            return

        for key, value in data.items():
            self.tickets_data[str(key)] = value
        self.ticket_list.setup_ui(data , self.click_event)

        
    def add_new_ticket(self, *args):
        print("Adding new ticket")
        main_app  = MDApp.get_running_app() 
        main_app.add_ticket_modal.open()













































# kv_tickets_layout = '''
# <TicketsLayout>:
#     orientation: "vertical"
#     size_hint: 1, None
#     adaptive_height: True

#     router_icon : router_icon

#     canvas.before:
#         Color:
#             rgba: chex("#5C5470")
#         RoundedRectangle:
#             pos: self.pos
#             size: self.size
#             radius: root.content_background_radius
    
#     Widget:
#         size_hint: 1, None
#         height: 15

#     SectionIconLayout:
#         id: router_icon
#         size_hint: 1, None 
 
#     Widget:
#         size_hint: 1, None
#         height: 5
           
#     BoxLayout:
#         size_hint: 1, None
#         height: 15
#         orientation: "horizontal"

#         Widget:
#             size_hint: 0.05, 1

#         Label:
#             size_hint: 0.4, 1
#             font_size: 10
#             color: chex("#FFFFFF")
#             text: "List of Ticket"
#             font_name: "p_bold"
#             text_size: self.size
#             halign: "left"
#             valign: "center"

#         Widget:
#             size_hint: 0.2, None
        
#         CustomClickableLabel:
#             size_hint: 0.3, 1
#             font_size: 10
#             color: chex("#FFFFFF")
#             text: "[u]+Add New Ticket[/u]"
#             markup: True
#             font_name: "p_regular"
#             text_size: self.size
#             halign: "right"
#             valign: "center"

#         Widget:
#             size_hint: 0.05, 1

#     Widget:
#         size_hint: 1, None
#         height: 15

#     BoxLayout:
#         size_hint: 1, None
#         height: 100
#         orientation: "horizontal"

#         Widget:
#             size_hint: 0.1, 1

#         TicketList:
#             size_hint: 0.3, 1
        
#         Widget:
#             size_hint: 0.05, 1

#         TicketDetailsWidget:
#             size_hint: 0.45, 1

#         Widget:
#             size_hint: 0.1, 1
        

    
#     Widget:
#         size_hint: 1, None
#         height: 15 


# <TicketWidget>:
#     size_hint: 1, None
#     height: 20
    
#     theme_elevation_level: "Custom"
#     elevation_level: 2
#     theme_shadow_offset: "Custom"
#     shadow_offset: 0, -3
#     theme_shadow_softness: "Custom"
#     shadow_softness: 12
#     shadow_radius: root.content_background_radius
#     radius: root.content_background_radius

#     Label:
#         size_hint: 1, 1
#         text : root.ticket_number
#         font_name: "p_bold"
#         font_size: 10
#         color: chex("#5C5470")
        
        

# <TicketList>:
#     do_scroll_x: False
#     do_scroll_y: True
#     bar_width: 0  # Optional: hide bar

#     MDBoxLayout:
#         orientation: "vertical"
#         size_hint: (1, None)
#         adaptive_height: True
#         spacing: 5
        
#         TicketWidget:
        
#         TicketWidget:
        
            



# <TicketDetailsWidget>:
#     orientation: "vertical" 

#     theme_elevation_level: "Custom"
#     elevation_level: 2
#     theme_shadow_offset: "Custom"
#     shadow_offset: 0, -3
#     theme_shadow_softness: "Custom"
#     shadow_softness: 12
#     shadow_radius: root.content_background_radius
#     radius: root.content_background_radius
#     padding: 10, 10
#     spacing: 4

    
#     Label:
#         size_hint: 1, 0.2
#         font_name: "p_bold"
#         font_size: 11
#         color: chex("#5C5470")
#         text: "Ticket Details"
#         halign: "left"
#         valign: "middle"
#         markup: True
#         text_size: self.size
    
        
#     Label:
#         size_hint: 1, 0.2
#         font_name: "p_light"
#         font_size: 9
#         color: chex("#5C5470")
#         text: "[font=p_regular]TICKET NO:[/font] 90DFENA6"
#         halign: "left"
#         valign: "middle"
#         markup: True
#         text_size: self.width - 20, None 
    
#     Label:
#         size_hint: 1, 0.2
#         font_name: "p_light"
#         font_size: 9
#         color: chex("#5C5470")
#         text: "[font=p_regular]STATUS:[/font] OPEN"
#         halign: "left"
#         valign: "middle"
#         markup: True
#         text_size: self.width - 20, None 

#     Label:
#         size_hint: 1, 0.2
#         font_name: "p_light"
#         font_size: 9
#         color: chex("#5C5470")
#         text: "[font=p_regular]TYPE:[/font] REPAIR"
#         halign: "left"
#         valign: "middle"
#         markup: True
#         text_size: self.width - 20, None 











# '''