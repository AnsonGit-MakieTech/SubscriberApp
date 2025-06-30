 
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty , ListProperty, BooleanProperty, DictProperty
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout 
from kivy.animation import Animation
from kivy.uix.button import Button
from kivy.uix.image import Image
from types import MethodType  # ✅ Import MethodType
from kivy.clock import Clock
from kivy.utils import platform
from kivy.uix.screenmanager import SlideTransition, FadeTransition, SwapTransition, ScreenManager
from kivymd.app import MDApp 
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

from variables import *
import os

from screen_home import (
    headline_layout, account_layout,
    tickets_layout, router_layout
)


class TappableImage(ButtonBehavior, Image):
    button_event = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def on_press(self):
        print("Image tapped!") 
        if self.button_event:
            self.button_event()

class AccountHeader(FloatLayout):
    # edit_icon : TappableImage = ObjectProperty(None)
    logout_icon : TappableImage = ObjectProperty(None)
    refresh_icon : TappableImage = ObjectProperty(None)

    buttons_spacing = NumericProperty(0)
    account_image_size = NumericProperty(100)
    account_fname_font_size = NumericProperty(15)
    account_letter = StringProperty("")

    account_image_radius = ListProperty([0, 0, 0, 0])
 
    widget_15_height = NumericProperty(10)
    widget_25_height = NumericProperty(10)
    widget_30_height = NumericProperty(10)
    widget_35_height = NumericProperty(10)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs) 

    
    # def on_parent(self, instance, parent):
    #     main_app = MDApp.get_running_app()
    #     if parent is None:
    #         if self.update_sizing in main_app.on_size_events_of_all_widgets:
    #             main_app.on_size_events_of_all_widgets.remove(self.update_sizing)
    #     else:
    #         if self.update_sizing not in main_app.on_size_events_of_all_widgets:
    #             main_app.on_size_events_of_all_widgets.append(self.update_sizing)
            
    

    def on_kv_post(self, *args):
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        # self.edit_icon.source = os.path.join(parent_dir, 'assets', 'edit_icon.png')
        self.logout_icon.source = os.path.join(parent_dir, 'assets', 'logout_icon.png')
        self.refresh_icon.source = os.path.join(parent_dir, 'assets', 'refresh_icon.png')
        
    
    def update_sizing(self, width, height ):
        multiplier = 0.08
        # self.edit_icon.size = (width * multiplier, width * multiplier)
        self.logout_icon.size = (width * multiplier, width * multiplier)
        self.refresh_icon.size = (width * multiplier, width * multiplier)
        self.buttons_spacing = width * 0.01

        self.account_image_size = min(width, height) * 0.25

        self.account_fname_font_size = min(width, height) * 0.09

        rad = min(width, height) * 0.05
        # if rad > 16:
        #     rad = 16
        self.account_image_radius = [rad, rad, rad, rad]
 
        
        self.widget_15_height = int(min(width, height) * 0.05)
        self.widget_25_height = int(min(width, height) * 0.15)
        self.widget_30_height = int(min(width, height) * 0.08)
        self.widget_35_height = int(min(width, height) * 0.1)
        

class HomeScreen(Screen):
    
    account_header : AccountHeader = ObjectProperty(None)
    header_height : NumericProperty = NumericProperty(0)
     
    home_screen_spacing = NumericProperty(0)
    home_screen_radius = ListProperty([0, 0, 0, 0])
    home_screen_padding = ListProperty([0, 0, 0, 0])


    headline : headline_layout.HeadlineLayout = ObjectProperty(None)
    router : router_layout.RouterLayout = ObjectProperty(None)
    tickets : tickets_layout.TicketsLayout = ObjectProperty(None)
    account : account_layout.AccountLayout = ObjectProperty(None)

    is_all_loaded = BooleanProperty(False)

    has_server_error = BooleanProperty(False)
    refresh_counter = NumericProperty(5)
    refresh_hit_counter = NumericProperty(5)

    plans_data = DictProperty()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.opacity = 0


    def on_parent(self, instance, parent):
        main_app = MDApp.get_running_app()
        if parent is None:
            if self.update_sizing in main_app.on_size_events_of_all_widgets:
                main_app.on_size_events_of_all_widgets.remove(self.update_sizing)
        else:
            if self.update_sizing not in main_app.on_size_events_of_all_widgets:
                main_app.on_size_events_of_all_widgets.append(self.update_sizing)
            self.update_sizing() 

    
    def update_sizing(self, *args):
        width , height = self.size
        self.header_height = min(width, height) * 0.5

        if self.account_header is not None:
            self.account_header.update_sizing(width=width, height=height)
        
        self.home_screen_spacing = min(width, height) * 0.05

        hrad = min(width, height) * 0.05
        if hrad > 16:
            hrad = 16
        self.home_screen_radius = [hrad, hrad, 0 , 0]
        hpad = min(width, height) * 0.06
        if hpad > 20:
            hpad = 20
        self.home_screen_padding = [hpad, hpad, hpad, hpad]
        
        
        if self.headline is not None:
            self.headline.update_sizing(width=width, height=height)
        
        if self.account is not None:
            self.account.update_sizing(width=width, height=height)
        
        if self.router is not None:
            self.router.update_sizing(width=width, height=height) 

        if self.tickets is not None:
            self.tickets.update_sizing(width=width, height=height)


    def on_pre_enter(self, *args):
        self.is_all_loaded = False
        return super().on_pre_enter(*args)
    
    def on_enter(self, *args):
        main_app  = MDApp.get_running_app() 
        anim = Animation(opacity=1, duration=1)
        anim.bind( on_start= main_app.on_window_resize, on_complete=self.remove_outside_screens)
        anim.start(self)
        # print("entering logoin")
        self.account_header.logout_icon.button_event = main_app.logout_modal.open
        # self.account_header.edit_icon.button_event = main_app.add_ticket_modal.open
        # self.account_header.refresh_icon.button_event = main_app.process_modal.open

        Clock.schedule_once(self.load_all_connected_screen)
 
        return super().on_enter(*args)
 
    
    def remove_outside_screens(self, *args): 
        main_app  = MDApp.get_running_app() 
        main_app.close_welcome_popup()

    def on_leave(self, *args):
        self.opacity = 0
        return super().on_leave(*args)
    
    def load_all_connected_screen(self, *args):
        main_app  = MDApp.get_running_app()
        main_app.is_outside = False

        
        self.headline.setup_image()
        self.account.setup_image()
        self.router.setup_image()
        self.tickets.setup_image()
        
        if not main_app.root_screen_manager.does_screen_exist(ADD_PLAN_SCREEN): 
            main_app.root_screen_manager.builder_load_screen('screen_add_plan', 'screen_add_plan.kv', ADD_PLAN_SCREEN )
            main_app.root_screen_manager.add_handler_screen(ADD_PLAN_SCREEN)

        self.is_all_loaded = True

        
        self.fetch_all_data()


    def fetch_all_data(self, *args):
        self.has_server_error = False
        self.refresh_counter = 0
        self.fetch_account_data()
        self.fetch_ticket_data()
        self.fetch_wallet_data()
        self.fetch_my_plans_data()


 

    def fetch_my_plans_data(self, *args):
        if not self.is_all_loaded:
            print("Widgets not loaded yet")
            return
        
        main_app  = MDApp.get_running_app()
        key = "get_plans"
        action = "get_plans"
        need_data = {}
        main_app.communications.get_data_action(need_data , key, action)
         

        def check_response(*args):
            com_data = main_app.communications.get_and_remove(key)
            if com_data is None: 
                print("No data received")
                return True
            
            if not com_data.get('result'):
                print(f'Error: {com_data.get("message", None)}')  
                if not self.has_server_error:
                    self.has_server_error = True
                    main_app.process_modal.open()
                    main_app.process_modal.proccess_text = "Checking server problem . . ."
                    def display_error(*args):
                        main_app.process_modal.display_error(com_data.get('message', None))
                    Clock.schedule_once(display_error, 1)
                self.refresh_counter = self.refresh_counter + 1
                return False  
            data = com_data.get('data', {}) 
            self.plans_data = com_data.get('data', {})
             
            if self.router is not None:
                self.router.setup_ui(data)
             
            if self.tickets is not None and self.headline is not None:
                for _ , plan in data.items():
                    tplan = {
                        'id' : str(plan.get('id', "None")),
                        'name' : plan.get('planname', "None"),
                    }
                    self.tickets.available_plans[str(plan.get('id', "None"))] = tplan.copy()
                    self.headline.available_plans[str(plan.get('id', "None"))] = tplan.copy()

            self.refresh_counter = self.refresh_counter + 1
            return False
         
        Clock.schedule_interval(check_response, 1)



    def fetch_wallet_data(self, *args):
        if not self.is_all_loaded:
            print("Widgets not loaded yet")
            return
        
        main_app  = MDApp.get_running_app()
        key = "get_wallet"
        action = "get_wallet"
        need_data = {}
        main_app.communications.get_data_action(need_data , key, action)
         

        def check_response(*args):
            com_data = main_app.communications.get_and_remove(key)
            if com_data is None: 
                print("No data received")
                return True
            
            if not com_data.get('result'):
                print(f'Error: {com_data.get("message", None)}')  
                if not self.has_server_error:
                    self.has_server_error = True
                    main_app.process_modal.open()
                    main_app.process_modal.proccess_text = "Checking server problem . . ."
                    def display_error(*args):
                        main_app.process_modal.display_error(com_data.get('message', None))
                    Clock.schedule_once(display_error, 1)
                self.refresh_counter = self.refresh_counter + 1
                return False  
            data = com_data.get('data', {})
            if data:
                unpaid_balance = data.get('unpaid', 0)
                wallet_balance = data.get('wallet', 0)
                self.headline.setup_wallet_ui( wallet_balance, unpaid_balance)
                
            self.refresh_counter = self.refresh_counter + 1
            return False
         
        Clock.schedule_interval(check_response, 1)



    def fetch_ticket_data(self, *args):
        if not self.is_all_loaded:
            print("Widgets not loaded yet")
            return
        
        main_app  = MDApp.get_running_app()
        key = "get_tickets"
        action = "get_tickets"
        need_data = {}
        main_app.communications.get_data_action(need_data , key, action)
         

        def check_response(*args):
            com_data = main_app.communications.get_and_remove(key)
            if com_data is None: 
                print("No data received")
                return True
            
            if not com_data.get('result'):
                print(f'Error: {com_data.get("message", None)}')  
                if not self.has_server_error:
                    self.has_server_error = True
                    main_app.process_modal.open()
                    main_app.process_modal.proccess_text = "Checking server problem . . ."
                    def display_error(*args):
                        main_app.process_modal.display_error(com_data.get('message', None))
                    Clock.schedule_once(display_error, 1)
                self.refresh_counter = self.refresh_counter + 1
                return False  
            data = com_data.get('data', {})
            if self.tickets is not None:
                self.tickets.setup_ui(data)
            if self.headline is not None:
                if data:
                    for ticket in data:
                        self.headline.setup_ticket_ui(
                            ticket_number = data[ticket].get('ticketnum', None),
                            ticket_type = data[ticket].get('ticketstatus', None),
                            ticket_status = data[ticket].get('type', None),
                        )
                        self.headline.has_pending_ticket = True
                        break
                else:
                    self.headline.setup_ticket_ui(
                            ticket_number = None,
                            ticket_type = None,
                            ticket_status = None,
                        )
                    self.headline.has_pending_ticket = False
            self.refresh_counter = self.refresh_counter + 1
            return False
         
        Clock.schedule_interval(check_response, 1)


    def fetch_account_data(self, *args):
        if not self.is_all_loaded:
            print("Widgets not loaded yet")
            return
        
        main_app  = MDApp.get_running_app()
        key = "get_account_info"
        action = "get_account_info"
        need_data = {}
        main_app.communications.get_data_action(need_data , key, action)
         

        def check_response(*args):
            com_data = main_app.communications.get_and_remove(key)
            if com_data is None: 
                print("No data received")
                return True
            
            if not com_data.get('result'):
                print(f'Error: {com_data.get("message", None)}')  
                if not self.has_server_error:
                    self.has_server_error = True
                    main_app.process_modal.open()
                    main_app.process_modal.proccess_text = "Checking server problem . . ."
                    def display_error(*args):
                        main_app.process_modal.display_error(com_data.get('message', None))
                    Clock.schedule_once(display_error, 1)
                self.refresh_counter = self.refresh_counter + 1
                return False  
            
            data = com_data.get('data', {})
            if self.account is not None:
                self.account.setup_ui(data)
            if self.account_header is not None:
                name = data.get('name', None)
                if name is not None:
                    if isinstance(name, str):
                        self.account_header.account_letter = name[0].upper() if len(name) > 0 else ""
                        
            self.refresh_counter = self.refresh_counter + 1
            return False
         
        Clock.schedule_interval(check_response, 1)

