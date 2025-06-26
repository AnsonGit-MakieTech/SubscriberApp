

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty , ListProperty, DictProperty, BooleanProperty
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout 
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.animation import Animation
from kivy.uix.button import Button
from kivy.uix.image import Image
from types import MethodType  # ✅ Import MethodType
from kivy.clock import Clock
from kivy.utils import platform
from kivy.uix.screenmanager import SlideTransition, FadeTransition, SwapTransition, ScreenManager
from kivymd.app import MDApp 
from kivy.uix.widget import Widget
from kivy.uix.dropdown import DropDown
from kivy.utils import get_color_from_hex 

import os

from screen_components import text_input
from variables import *
from screen_components import app_button, top_form_buttons, text_input
from utils.app_utils import *


from kivy import platform
import os
import shutil
if platform == "win":
    from plyer import filechooser
if platform == "android":
    from android.storage import app_storage_path
    from androidstorage4kivy import SharedStorage, Chooser



class CityDropdownButton(app_button.AppButton):
    text = StringProperty("Select City")
    text_font_size = NumericProperty(16)
    value = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = get_color_from_hex("#352F44")
        self.opacity = 0
        self.elevation = 0
 
    
    def update_sizing(self, *args):
        width, height = self.size
        self.text_font_size = int(min(width, height) * 0.3)

class AccountRegistrationFormLayout(
    MDBoxLayout
):
    
    h1_font_size = NumericProperty(14)
    h2_font_size = NumericProperty(14)
    h3_font_size = NumericProperty(13)
    h4_font_size = NumericProperty(10)
    valid_id_image_width = NumericProperty(250)
    checkbox_size = ListProperty([35, 35])
    
    first_name_input: text_input.OneLineInput = ObjectProperty(None)
    last_name_input: text_input.OneLineInput = ObjectProperty(None)
    middle_name_input: text_input.OneLineInput = ObjectProperty(None)
    email_input: text_input.OneLineInput = ObjectProperty(None)
    street_input : text_input.OneLineInput = ObjectProperty(None)
    barangay_input: text_input.OneLineInput = ObjectProperty(None)
    city_input: text_input.OneLineInput = ObjectProperty(None)
    phone1_input: text_input.OneLineInput = ObjectProperty(None)
    phone2_input: text_input.OneLineInput = ObjectProperty(None)
    phone3_input: text_input.OneLineInput = ObjectProperty(None)
    username_input: text_input.OneLineInput = ObjectProperty(None)
    password_input: text_input.OneLineInput = ObjectProperty(None)
    confirm_password_input: text_input.OneLineInput = ObjectProperty(None)
    date_of_birth_input: app_button.AppButton = ObjectProperty(None)
    
    picker = ObjectProperty(None)

    selected_city = StringProperty("Select City")
    valid_id_image_source = StringProperty("")

    is_selecting_file = BooleanProperty(False)
    
    widget_8_height = NumericProperty(0) 
    widget_15_height = NumericProperty(10)
    widget_25_height = NumericProperty(10)
    widget_30_height = NumericProperty(10)
    widget_35_height = NumericProperty(10)
    widget_125_height = NumericProperty(10)
    parent_size = ListProperty([0, 0])

    register_event = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opacity = 0
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        self.valid_id_image_source = os.path.join(parent_dir, 'assets', 'add_id_image.png')

        self.dropdown = DropDown(max_height=150)



        # Bind button from KV to open dropdown
        self.dropdown.bind(on_select=self.on_select)

    def on_select(self, instance, value):
        self.selected_city = value.text
        print(f"Selected option: {value.text}")
        print(value)
        pass

    def customized_ui(self, *args):
        self.city_input.bind(on_release=self.dropdown.open)
        self.first_name_input.costumized_input( hint_text = "First Name . . ." )
        self.last_name_input.costumized_input( hint_text = "Last Name . . ." )
        self.middle_name_input.costumized_input( hint_text = "Middle Name . . ." )
        self.email_input.costumized_input( hint_text = "Email . . ." )
        self.street_input.costumized_input( hint_text = "Street . . ." )
        self.barangay_input.costumized_input( hint_text = "Barangay . . ." )
        self.city_input.update_color("#5C5470")
        self.phone1_input.costumized_input( hint_text = "Primary Phone Number (required)" )
        self.phone2_input.costumized_input( hint_text = "Additional Phone Number (optional)" )
        self.phone3_input.costumized_input( hint_text = "Additional Phone Number (optional)" )
        self.username_input.costumized_input( hint_text = "Username . . .", is_password = False )
        self.password_input.costumized_input( hint_text = "Password . . .", is_password = True )
        self.confirm_password_input.costumized_input( hint_text = "Confirm Password . . .", is_password = True )
    
    def update_sizing_inputs(self, *args): 
        self.first_name_input.setup_layout()
        self.last_name_input.setup_layout()
        self.middle_name_input.setup_layout()
        self.email_input.setup_layout()
        self.street_input.setup_layout()
        self.barangay_input.setup_layout() 
        self.phone1_input.setup_layout()
        self.phone2_input.setup_layout()
        self.phone3_input.setup_layout()
        self.username_input.setup_layout()
        self.password_input.setup_layout()
        self.confirm_password_input.setup_layout()
        self.first_name_input.setup_layout()
        width, height = self.parent_size
        self.update_sizing(width, height)
        print("update_sizing_inputs")


    def update_sizing(self, width, height): 
        self.parent_size = [width, height]
        self.h1_font_size = int(width * 0.043)
        # if self.h1_font_size > 18:
        #     self.h1_font_size = 18
        self.h2_font_size = int(width * 0.038)
        # if self.h2_font_size > 16:
        #     self.h2_font_size = 16
        
        self.valid_id_image_width = int(width * 0.9)
        # if self.valid_id_image_width > 250:
        #     self.valid_id_image_width = 250
        
        self.h3_font_size = int(width * 0.035)
        # if self.h3_font_size > 14:
        #     self.h3_font_size = 14
        
        self.h4_font_size = int(width * 0.032)
        # if self.h4_font_size > 12:
        #     self.h4_font_size = 12

        self.widget_8_height = int(min(width , height) * 0.03 )
        self.widget_15_height = int(min(width, height) * 0.05)
        self.widget_25_height = int(min(width, height) * 0.15)
        self.widget_30_height = int(min(width, height) * 0.08)
        self.widget_35_height = int(min(width, height) * 0.1) 
        self.widget_125_height = int(min(width, height) * 0.5)

        self.dropdown.max_height = self.widget_125_height 

        # print(f"width: {width}, height: {height}, h4_font_size: {self.h4_font_size}")
        
        cwidth = width * 0.03
        cheight = width * 0.03
        self.checkbox_size = [cwidth, cheight]
        # if cwidth > 35 or cheight > 35:
        #     self.checkbox_size = [35, 35]
        print(f"widget_125_height: {self.widget_125_height}")
        print(f"width: {width}, height: {height}, cwidth: {cwidth}, cheight: {cheight}")
 

    def select_date(self, *args):
        
        from kivymd.uix.pickers import MDDatePicker
        self.picker  = MDDatePicker()
        self.picker.pos_hint = {"center_x": .5, "center_y": .5}
        self.picker.size_hint = [.9, .6]
        self.picker.open()
    
    def on_date_chosen(self, *args):
        print("Result : ", args)

    def upload_image(self):
        
        if self.is_selecting_file:
            return
        self.is_selecting_file = True
        
        def reset_selecting(*args):
            self.is_selecting_file = False

        Clock.schedule_once( reset_selecting  , 1)

        if platform == "win":
            filechooser.open_file(on_selection=self.handle_selection)
        elif platform == "android":
            # SharedStorage().choose_file(mime_type="image/*", callback=self.on_image_selected)
            self.chooser = Chooser(self.on_image_selected)
            self.chooser.choose_content('image/*', multiple=False)

    def handle_selection(self, selection):
        
        if selection:
            image_path = selection[0]  
            if not is_image(image_path): 
                return
            self.valid_id_image_source = image_path
            self.is_selecting_file = False
        else:
            self.is_selecting_file = False

    def on_image_selected(self, uri_list):
        
        if uri_list:
            uri = uri_list[0]
            ss = SharedStorage()

            # ✅ Copy file from shared storage to app cache
            private_file_path = ss.copy_from_shared(uri)
            if private_file_path: 
                Clock.schedule_once(lambda dt: self.on_image_loaded_path(private_file_path))
            else: 
                self.is_selecting_file = False
        else:
            self.is_selecting_file = False

    def on_image_loaded_path(self, private_file_path):
        filename = os.path.basename(private_file_path)

        # ✅ Check if it's an image
        if not is_image_ext(filename): 
            self.is_selecting_file = False
            return
        save_dir = os.path.join(self.get_save_path(), "selected_images")
        os.makedirs(save_dir, exist_ok=True) 
        image_path = os.path.join(save_dir, filename) 
        shutil.copy(private_file_path, image_path) 
        self.valid_id_image_source = image_path
        self.is_selecting_file = False 

    def get_save_path(self):
        # Return a writable path depending on the platform
        if platform == "android": 
            return app_storage_path()
        else:
            return os.path.expanduser("~")

    def register_account(self, *args):
        if self.register_event is not None:
            self.register_event() 

class CreateAccountScreen(Screen): 
    login_logo = StringProperty("")
    create_account_logo = StringProperty("")
    
    info_title_font_size = NumericProperty(14)
    info_content_font_size = NumericProperty(10)
    adaptive_radius = ListProperty([ 0, 0, 24, 24])
    
    create_account_title_font_size = NumericProperty(14)
    create_account_content_font_size = NumericProperty(10)
    
    header_buttons : top_form_buttons.HeaderButtons = ObjectProperty(None)
    find_my_location_button : app_button.AppButton = ObjectProperty(None)
    
    find_my_location_button_font_size = NumericProperty(14)
    
    h1_font_size = NumericProperty(14)
    h2_font_size = NumericProperty(14)

    
    registration_form : BoxLayout = ObjectProperty(None)

    widget_15_height = NumericProperty(10)
    widget_25_height = NumericProperty(10)
    widget_30_height = NumericProperty(10)
    widget_35_height = NumericProperty(10)
    login_logo_height = NumericProperty(10)

    is_creating_account = BooleanProperty(False)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.opacity = 0
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        self.login_logo = os.path.join(parent_dir, 'assets', 'login_info.png')
        self.create_account_logo = os.path.join(parent_dir, 'assets', 'create_account_logo.png')

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
        self.info_title_font_size = int(min( width, height) * 0.03)
        self.info_content_font_size = int(min( width, height) * 0.02)
        r = min(width, height) * 0.05  # You can change 0.05 to any fraction
        self.adaptive_radius = [0, 0, r, r] 
        
        self.create_account_title_font_size = int(width* 0.05)
        self.create_account_content_font_size = int(width  * 0.03)
        # if self.create_account_title_font_size > 27:
        #     self.create_account_title_font_size = 27
        # if self.create_account_content_font_size > 25:
        #     self.create_account_content_font_size = 25
        self.h1_font_size = int(width * 0.04)
        # if self.h1_font_size > 17:
        #     self.h1_font_size = 17
        self.h2_font_size = int(width * 0.03)
        # if self.h2_font_size > 15:
        #     self.h2_font_size = 15
        self.find_my_location_button_font_size = int(width * 0.03)
        # if self.find_my_location_button_font_size > 19:
        #     self.find_my_location_button_font_size = 19
        
        self.widget_15_height = int(min(width, height) * 0.05)
        self.widget_25_height = int(min(width, height) * 0.15)
        self.widget_30_height = int(min(width, height) * 0.08)
        self.widget_35_height = int(min(width, height) * 0.1)
        self.login_logo_height = int(min(width, height) * 0.7)
        
        if self.registration_form is not None:
            if len(self.registration_form.children) > 0:
                self.registration_form.children[0].update_sizing(width , height)
        
        if self.header_buttons is not None:
            self.header_buttons.update_sizing(width=width, height=height)
            

    def on_enter(self, *args):
        main_app  = MDApp.get_running_app() 
        
        Clock.schedule_once(self.display_registration_form, 1) # Used to display the registration form

        self.find_my_location_button.update_color("#352F44")
        anim = Animation(opacity=1, duration=0.5)
        anim.bind(on_start= main_app.on_window_resize, on_complete = main_app.close_welcome_popup)
        anim.start(self) 

        create_data = main_app.app_data.get(CREATE_KEY, {})
        if create_data.get("is_applying", False):
            self.header_buttons.customized_ui(button_text_1="Select Plan", button_text_2="Go To Login")
            self.header_buttons.button_1_event = self.go_back_to_showcase
        else:
            self.header_buttons.customized_ui(button_text_1="", button_text_2="Go To Login" , display_button_1=False)
            
         
        self.header_buttons.button_2_event = self.go_back_to_login

        Clock.schedule_once(self.load_connected_screen)
         
        return super().on_enter(*args)

    def on_leave(self, *args):
        self.opacity = 0
        return super().on_leave(*args)

    def display_registration_form(self, *args):
        if not self.registration_form:
            Clock.schedule_once(self.display_registration_form, 0.1)
            return


        if len(self.registration_form.children) < 1:
            registration = AccountRegistrationFormLayout()
            registration.register_event = self.register_account
            self.registration_form.add_widget(registration) 
            self.update_sizing()

            def on_complete(*args):
                self.update_sizing()
                registration.update_sizing_inputs()
                self.update_sizing()
            
            def display_registration_form(*args): 
                registration.customized_ui()
                anim = Animation(opacity=1, duration=0.5)
                # anim.bind(on_progress=registration.update_sizing_inputs)
                anim.bind(on_complete=on_complete)
                anim.start(registration)
                        # Create dropdown options
                for option in ["Click Here To Select", "Option 1", "Option 2", "Option 3", "Option 4"]:
                    widget = Widget(size_hint_y=None,height=registration.widget_8_height)
                    registration.dropdown.add_widget(widget)
                    btn = CityDropdownButton(size_hint_y=None, height=self.widget_35_height)
                    btn.text = option
                    btn.value = option
                    btn.update_sizing()
                    btn.bind(on_release=lambda btn: registration.dropdown.select(btn))
                    registration.dropdown.add_widget(btn)
            
            Clock.schedule_once(display_registration_form, 0.2)


    def find_my_location(self, *args):
        
        main_app = MDApp.get_running_app()
        if main_app.user_map_verification_modal is not None:
            main_app.user_map_verification_modal.open() 
    
    def go_back_to_login(self, *args):
        main_app  = MDApp.get_running_app() 
        if main_app.app_data.get(CREATE_KEY, None): 
            del main_app.app_data[CREATE_KEY]
        Clock.schedule_once(main_app.show_welcome_popup)  
        main_app.root_screen_manager.change_screen(LOGIN_SCREEN)
        
    def go_back_to_showcase(self, *args):
        main_app  = MDApp.get_running_app()
        Clock.schedule_once(main_app.show_welcome_popup)  
        main_app.root_screen_manager.change_screen(PRODUCT_SHOWCASE_SCREEN)
    
    def load_connected_screen(self, *args):
        main_app = MDApp.get_running_app()
        main_app.load_user_map_verification_modal()
        main_app.user_map_verification_modal.load_map()
        main_app.load_all_registrations_modal() 

        main_app.on_window_resize()



    def register_account(self, *args):
        if self.is_creating_account:
            return
        self.is_creating_account = True

        main_app = MDApp.get_running_app()
        key = "all_plan_products"
        action = "fetch_all_plan_products"
        need_data = {}
        main_app.communications.post_data_action(need_data , key, action)

        import random
        type_of_account = random.choice(["New", "Existing"])

        def check_response(*args):
            com_data = main_app.communications.get_and_remove(key)
            if com_data is None: 
                print("No data received")
                return True
            
            # if not com_data.get('result'):
            #     print(f'Error: {com_data.get("message", None)}') 
                # main_app.process_modal.open()
                # main_app.process_modal.proccess_text = ""
                # Clock.schedule_once(lambda x : main_app.process_modal.display_error(com_data.get('message', None)), 0.5)
                # self.is_logging_in = False
                # return False
            
            data = com_data.get('data', None)
            print(f'data: {data}')

            if type_of_account == "New": 
                main_app.next_step_modal.open()
                def button_action_for_payment(*args):
                    print("Link to payment redirecting")
                main_app.next_step_modal.button_action_for_online = button_action_for_payment
                main_app.next_step_modal.button_action_for_visit = main_app.application_number_modal.open
            else:
                main_app.activate_account_modal.open()

            self.is_creating_account = False
            return False
        
        Clock.schedule_interval(check_response, 1)








        
