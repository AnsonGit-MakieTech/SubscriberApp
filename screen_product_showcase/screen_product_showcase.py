 
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty , ListProperty, BooleanProperty, DictProperty
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout 
from kivy.animation import Animation
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from types import MethodType  # ✅ Import MethodType
from kivy.clock import Clock
from kivy.utils import platform
from kivy.uix.screenmanager import SlideTransition, FadeTransition, SwapTransition, ScreenManager
from kivymd.app import MDApp 
from kivy.utils import get_color_from_hex
from kivymd.uix.boxlayout import MDBoxLayout

import os

from screen_components import text_input
from variables import *
from screen_components import app_button, top_form_buttons, text_input, label_clickable
 
from kivy.uix.widget import Widget
from kivy.properties import ListProperty
from kivy.graphics import Color, Ellipse 
from kivy.uix.behaviors import ButtonBehavior

class AdaptiveCircle(Widget):
    color = ListProperty(get_color_from_hex("#5C5470"))  # default: opaque red

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # draw the circle once
        with self.canvas:
            Color(rgba=self.color)
            # placeholder for the ellipse instruction
            self._ellipse = Ellipse(pos=self.pos, size=self.size)

        # whenever pos/size/color changes, update the ellipse
        self.bind(pos=self._update_graphics,
                  size=self._update_graphics,
                  color=self._update_color)

    def _update_graphics(self, *args):
        # keep the Ellipse in sync
        self._ellipse.pos = self.pos
        self._ellipse.size = self.size

    def _update_color(self, instance, value):
        # redraw the Color instruction
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=value)
        # note: if you want the circle to be behind other canvas ops,
        # you could put this in canvas.before instead of canvas.



class ProductShowcaseCategory(Label):
    widget_type = StringProperty('category')


    def update_sizing(self, width, height):
        self.height = min( width, height) * 0.08
        self.font_size = int( min( width, height) * 0.03) 
        



class ProductShowcaseProduct( 
    ButtonBehavior,
    MDBoxLayout):
    widget_type = StringProperty('product')
    is_selected = BooleanProperty(False)
    category = StringProperty('Recommended for you')
    border_width = NumericProperty(1)
    border_radius = NumericProperty(1)
    
    additional_height = NumericProperty(0.20)
    original_height = NumericProperty(0)

    product_name : Label = ObjectProperty(None)
    plan_font_size = NumericProperty(0)
    additional_plan_font_size = NumericProperty(0.10)
    original_plan_font_size = NumericProperty(0)

    select_icon_size = NumericProperty(0)
    selected_icon = StringProperty('')

    parent_event = ObjectProperty(None)
    plan_id = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        self.selected_icon = os.path.join(parent_dir, 'assets', 'selected_icon.png')

    def update_sizing(self, width, height):
        self.height = min( width, height) * 0.13
        self.original_height = min( width, height) * 0.13
        # 2% of the smaller edge for border thickness
        bw = min(self.width, self.height) * 0.2
        self.border_width = max(bw, 1)
        # 10% of the smaller edge for corner radius
        br = min(self.width, self.height) * 0.10
        self.border_radius = max(br, 1) 
        self.canvas.ask_update()

        self.plan_font_size = int(min(width, height) * 0.03)
        self.original_plan_font_size = int(min(width, height) * 0.03)

        self.select_icon_size = int(min(width, height) * 0.05)
        # print(f"width: {width}, height: {height}, select_icon_size: {self.select_icon_size}")
        



    
    def click_event(self, *args):
        print("clicked") 
        if self.parent_event:
            self.parent_event(self)


    def select(self , *args): 
        if self.is_selected:
            anim = Animation(
                height=(self.height + (self.height * self.additional_height)), duration=0.2)
            anim.start(self)

            if self.product_name:
                anim = Animation(font_size=self.plan_font_size + (self.plan_font_size * self.additional_plan_font_size), duration=0.2)
                anim.start(self.product_name)

    def unselect(self, *args):
        if not self.is_selected:
            anim = Animation(height=self.original_height, duration=0.2)
            anim.start(self)

            if self.product_name:
                anim = Animation(font_size=self.original_plan_font_size, duration=0.2)
                anim.start(self.product_name)



class ProductShowcaseScreen(Screen): 
    circle_widget = ObjectProperty(None)

    h1_font_size = NumericProperty(30)
    h2_font_size = NumericProperty(20)
    h3_font_size = NumericProperty(16)
    h4_font_size = NumericProperty(14)
    h5_font_size = NumericProperty(12)

    subscribe_spacing  = NumericProperty(10) 
    subscribe_icon_size = NumericProperty(20)
    cart_subscribe_icon = StringProperty('')
    product_subscribe_icon = StringProperty('')

    product_list : MDBoxLayout = ObjectProperty(None)

    login_text = StringProperty("[u]Have an account? Tap here.")

    

    category_text = StringProperty('')
    plan_name = StringProperty('')
    plan_description = StringProperty('')
    plan_price = StringProperty('')
    plan_speed = StringProperty('')
    additional_text = StringProperty('')
    additional_1_text = StringProperty('')

    subscribe_button : app_button.AppButton = ObjectProperty(None)
    alternate_button : label_clickable.LabelClickable = ObjectProperty(None)


    products_data = DictProperty({})
    selected_product = DictProperty({})


    
    def __init__(self, **kwargs):
        super().__init__(**kwargs) 
        self.opacity = 0
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        self.cart_subscribe_icon = os.path.join(parent_dir, 'assets', 'cart_subscribe_icon.png') 
        self.product_subscribe_icon = os.path.join(parent_dir, 'assets', 'product_icon.png')
        

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

        if self.circle_widget is not None:
            circle_size = min(width, height) * 1.52
            self.circle_widget.size = (circle_size, circle_size)
        
        self.h1_font_size = min(width, height) * 0.04
        self.h2_font_size = min(width, height) * 0.03
        self.h3_font_size = min(width, height) * 0.025
        self.h4_font_size = min(width, height) * 0.02
        self.h5_font_size = min(width, height) * 0.015

        rad = min(width, height) * 0.01
        if rad > 10:
            rad = 10
        self.subscribe_spacing = rad * 2 
        self.subscribe_icon_size = min(width, height) * 0.05

        if self.subscribe_button is not None:
            self.subscribe_button.content_background_radius = [rad , rad, rad, rad]

        if self.product_list is not None:
            for child in self.product_list.children:
                child.update_sizing(width, height)

    def on_enter(self, *args):
        main_app  = MDApp.get_running_app()
        if main_app.is_outside:
            self.login_text = "[u]Have an account? Tap here."
        else:
            self.login_text = "[u]Go Back? Tap here."
        
        anim = Animation(opacity=1, duration=0.5)
        anim.bind(on_start= main_app.on_window_resize , on_complete = main_app.close_welcome_popup)
        anim.start(self)

        Clock.schedule_once(self.load_connected_screen)

        self.subscribe_button.opacity = 0 # set opacity to 0 because it will be shown later
        return super().on_enter(*args)

    def on_leave(self, *args):
        self.opacity = 0
        self.subscribe_button.opacity = 0
        self.alternate_button.opacity = 0

        return super().on_leave(*args)
    

    def goto_login_screen(self, *args):
        main_app  = MDApp.get_running_app()
        Clock.schedule_once(main_app.show_welcome_popup)
        if main_app.is_outside: 
            main_app.root_screen_manager.change_screen(LOGIN_SCREEN)
        else:
            main_app.root_screen_manager.change_screen(ADD_PLAN_SCREEN)

        
    def goto_create_screen(self, *args):
        main_app  = MDApp.get_running_app() 
        Clock.schedule_once(main_app.show_welcome_popup) 
        if main_app.is_outside: 
            main_app.root_screen_manager.change_screen(CREATE_ACCOUNT_SCREEN)
        else:
            main_app.root_screen_manager.change_screen(ADD_PLAN_SCREEN)

    
    def load_connected_screen(self, *args):
        
        self.fetch_all_plan_products() # fetch all products from server

        main_app  = MDApp.get_running_app()
        

        if not main_app.root_screen_manager.does_screen_exist(LOGIN_SCREEN) and main_app.is_outside:
            main_app.root_screen_manager.builder_load_screen('screen_login', 'screen_login.kv', LOGIN_SCREEN )
            main_app.root_screen_manager.add_handler_screen(LOGIN_SCREEN)
        
        
        if not main_app.root_screen_manager.does_screen_exist(CREATE_ACCOUNT_SCREEN) and main_app.is_outside:
            main_app.root_screen_manager.builder_load_screen('screen_create_account', 'screen_create_account.kv', CREATE_ACCOUNT_SCREEN )
            main_app.root_screen_manager.add_handler_screen(CREATE_ACCOUNT_SCREEN)
 

        if not main_app.root_screen_manager.does_screen_exist(ADD_PLAN_SCREEN) and not main_app.is_outside: 
            main_app.root_screen_manager.builder_load_screen('screen_add_plan', 'screen_add_plan.kv', ADD_PLAN_SCREEN )
            main_app.root_screen_manager.add_handler_screen(ADD_PLAN_SCREEN) 

        
    def display_product(self, selected_widget = None): 

        self.selected_product = self.products_data.get(selected_widget.plan_id, None)
        print(f"Selected product: {self.selected_product}")
        if self.selected_product is None:
            print("Product not found")
            return
        
        self.category_text = self.selected_product.get('category', 'unknown')
        self.plan_name = self.selected_product.get('name', 'unknown')
        self.plan_description = self.selected_product.get('description', 'unknown')
        self.plan_price = f"Monthly : [font=p_extralight]{self.selected_product.get('monthly_text', 'unknown')}"
        self.plan_speed = f"Speed : [font=p_extralight]{self.selected_product.get('speed_text', 'unknown')}"
        

        additional_text = self.selected_product.get('additional_text', None)
        self.additional_text = ''
        if isinstance(additional_text, list):
            if len(additional_text ) == 2:
                self.additional_text = f"{additional_text[0]}: [font=p_extralight]{additional_text[1]}"
        additional_1_text = self.selected_product.get('additional_1_text', None)
        self.additional_1_text = ''
        if isinstance(additional_1_text, list):
            if len(additional_1_text) == 2:
                self.additional_1_text = f"{additional_1_text[0]} [font=p_extralight]{additional_1_text[1]}"

        self.subscribe_button.opacity = 1 
        self.alternate_button.opacity = 1

        if not selected_widget.is_selected:

            for child in self.product_list.children:
                if child.widget_type == "product":
                    child.is_selected = False
                    child.unselect()
        
            selected_widget.is_selected = True
            selected_widget.select()



    def fetch_all_plan_products(self, *args):
        main_app  = MDApp.get_running_app()
        key = "all_plan_products"
        action = "get_product_showcase"
        need_data = {}
        main_app.communications.get_data_action(need_data , key, action)
        
        main_app.process_modal.open()
        main_app.process_modal.proccess_text = "Please wait while we fetch our products"

        def check_response(*args):
            com_data = main_app.communications.get_and_remove(key)
            if com_data is None: 
                print("No data received")
                return True
            
            if not com_data.get('result'):
                print(f'Error: {com_data.get("message", None)}')  
                main_app.process_modal.display_error(com_data.get('message', None))
                return False
            
            data = com_data.get('data', None)
            self.product_list.clear_widgets()
            self.products_data = {}
            self.selected_product =  {} 
            first_product = None

            if len(data) < 1:
                print("No products found")
                main_app.process_modal.dismiss()
                return False
            
            for product in data:
                ptitle = product.get('title', None)
                pdata = product.get('products', {})

                ptwidget = ProductShowcaseCategory()
                ptwidget.text = ptitle

                self.product_list.add_widget(ptwidget) 

                for pdkey, pdvalue in pdata.items(): 
                    pdwidget = ProductShowcaseProduct()
                    pdwidget.product_name.text = pdvalue.get('name', 'Unknown')
                    pdwidget.parent_event = self.display_product
                    pdwidget.plan_id = str(pdkey)
                    self.product_list.add_widget(pdwidget)
                    pdvalue['category'] = ptitle 
                    self.products_data[str(pdkey)] = pdvalue
                    
                    if not first_product: 
                        first_product = pdwidget
 
            
            # print(f'all data : f{self.products_data}')
            print(f'selected product: {self.selected_product}')
            self.update_sizing()
            self.display_product(first_product)
            # main_app.process_modal.display_success(com_data.get('message', None))
            # Clock.schedule_once(main_app.process_modal.dismiss, 1.5)
            main_app.process_modal.dismiss()
            return False
        
        print(f'fetch_all_plan_products')
        Clock.schedule_interval(check_response, 1)












