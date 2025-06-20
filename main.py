 
__version__ = "1.0.0"
from kivy.core.window import Window

Window.keyboard_anim_args = {"d": 0.2, "t": "in_out_expo"}
Window.softinput_mode = "below_target"


from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivy.lang.builder import Builder
from kivy.core.text import LabelBase
from kivy.utils import platform, get_color_from_hex
from kivy.properties import StringProperty, NumericProperty, ListProperty, BooleanProperty, ObjectProperty, DictProperty

from variables import *
import os
import json
import shutil
 
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.modalview import ModalView
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from communications  import Communications 
from kivy.animation import Animation

from kivy.uix.image import Image
from kivy.uix.modalview import ModalView
from kivy.graphics import Color, Rectangle 


if platform == "android": 
    from android.permissions import request_permissions, Permission, check_permission  # pylint: disable=import-error

if platform == "ios":
    pass

Window.show_cursor = True


if platform == "win":
    # Simulate a mid-sized Android phone
    Window.size = (360, 780)


from screen_components import (
    text_input, process_modal ,
    section_icon, logout_modal, 
    add_ticket_modal, app_button, 
    label_clickable, top_form_buttons, 
    verify_user_location_modal, next_step_modal,
    application_number_modal, activate_account_modal
)
from screen_home import headline_layout, router_layout, account_layout, tickets_layout 
from screen_create_account.screen_create_account import CreateAccountScreen
from screen_forgot.screen_forgot import ForgotAccountScreen
from screen_login.screen_login import LoginScreen 
from screen_first_time.screen_first_time import FirstTimeScreen
from screen_product_showcase.screen_product_showcase import ProductShowcaseScreen
from screen_home.screen_home import HomeScreen
from screen_add_plan.screen_add_plan import AddPlanScreen

class TappableImage(Image):
    def __init__(self, modal_ref, **kwargs):
        super().__init__(**kwargs)
        self.modal_ref = modal_ref

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.modal_ref.animate_closing()
            return True
        return super().on_touch_down(touch)


class ImageModal(ModalView):
    def __init__(self, image_path, **kwargs):
        super().__init__(**kwargs)
        self.auto_dismiss = False
        self.background_color = (0, 0, 0, 0)  # Transparent modal background
        self.opacity = 0

        # Main container with canvas background
        self.container = BoxLayout()
        with self.container.canvas.before:
            Color(*get_color_from_hex('#352F44'))  # Light blue background
            self.bg_rect = Rectangle(pos=self.container.pos, size=self.container.size)

        # Update rectangle when container resizes or moves
        self.container.bind(pos=self.update_bg_rect, size=self.update_bg_rect)

        # Add image inside the BoxLayout
        self.image_widget = TappableImage(
            source=image_path,
            allow_stretch=True,
            keep_ratio=True,
            modal_ref=self
        )

        self.container.add_widget(self.image_widget)
        self.add_widget(self.container)

    def update_bg_rect(self, *args):
        self.bg_rect.pos = self.container.pos
        self.bg_rect.size = self.container.size
 
    def animate_opening(self): 
        animation = Animation(opacity= 1, duration=0.3)
        animation.start(self)
        self.open()


    def animate_closing(self):
        animation = Animation(opacity= 0, duration=0.3)
        animation.bind(on_complete=self.dismiss)
        animation.start(self) 



class ScreenHandler(BoxLayout):  # Acts as ScreenManager
    handler : MDScreenManager = ObjectProperty(None)
    handler_screen_names : list = ListProperty([])

    def does_screen_exist(self, screen_name):
        return screen_name in self.handler_screen_names
    

    def builder_load_screen(self, folder , file_name, screen_name):
        if not self.does_screen_exist(screen_name): 
            
 
            if screen_name == HOME_SCREEN:
                Builder.load_string(headline_layout.kv_headline_layout) 
                Builder.load_string(router_layout.kv_router_layout)
                Builder.load_string(account_layout.kv_account_layout)
                Builder.load_string(tickets_layout.kv_tickets_layout)


            screen_kv = os.path.join(os.path.dirname(__file__), folder, file_name)
            Builder.load_file(screen_kv)
 
    def add_handler_screen(self, screen_name):
        print(f"Adding screen: {screen_name}")
        if screen_name not in self.handler_screen_names:
            if screen_name == LOGIN_SCREEN:
                self.handler.add_widget(LoginScreen(name=screen_name))
            elif screen_name == FIRST_TIME_SCREEN:
                self.handler.add_widget(FirstTimeScreen(name=screen_name))
            elif screen_name == PRODUCT_SHOWCASE_SCREEN:
                self.handler.add_widget(ProductShowcaseScreen(name=screen_name))
            elif screen_name == CREATE_ACCOUNT_SCREEN:
                self.handler.add_widget(CreateAccountScreen(name=screen_name))
            elif screen_name == FORGOT_ACCOUNT_SCREEN:
                self.handler.add_widget(ForgotAccountScreen(name=screen_name))
            elif screen_name == HOME_SCREEN:
                self.handler.add_widget(HomeScreen(name=screen_name))
            elif screen_name == ADD_PLAN_SCREEN:
                self.handler.add_widget(AddPlanScreen(name=screen_name)) 
            self.handler_screen_names.append(screen_name)



            print(f"Screen added: {screen_name}")
        else:
            print(f"Screen already exists: {screen_name}")
    
    def change_screen(self, screen_name):
        if screen_name not in self.handler_screen_names:
            return
        self.handler.current = screen_name

    def remove_screen(self, screen_name):
        if screen_name in self.handler.screen_names:
            self.handler.remove_widget(self.handler.get_screen(screen_name))
            print(f"{screen_name} screen removed.")

class SubscriberApp(MDApp):
 
    communications : dict = None
    done_load_modal : ImageModal = ObjectProperty(None)
    root_screen_manager : ScreenHandler = ObjectProperty(None)
    process_modal = ObjectProperty(None)
    logout_modal = ObjectProperty(None)
    add_ticket_modal = ObjectProperty(None)
    user_map_verification_modal = ObjectProperty(None)
    next_step_modal = ObjectProperty(None)
    application_number_modal = ObjectProperty(None)
    activate_account_modal = ObjectProperty(None)

    on_size_events_of_all_widgets = ListProperty([])
    _resize_scheduled = False

    user_data = DictProperty({})

    def on_start(self):
        """ Check and request storage permission on Android """ 
        # Defer screen loading after UI is visible
        Clock.schedule_once(self.load_screens, 0.1)
        Clock.schedule_once(self.on_window_resize, 1) 
        # self.process_modal.open()

    def on_stop(self):
        try:
            # Close communications
            self._clear_cache_folder()
            self.communications.kill_all_threads()
        except Exception as e:
            # print(f"Error saving user data: {e}")
            pass

    def on_pause(self):
        Clock.schedule_once(self.show_welcome_popup, 0.1)
        Clock.schedule_once(self.close_welcome_popup, 0.7)
        return super().on_pause()

    def build(self):
        self.theme_cls.primary_dark = get_color_from_hex("#352F44")

        # Set App Icon
        self.icon = os.path.join(os.path.dirname(__file__), 'assets', 'app_logo.png')
        splash_image = os.path.join(os.path.dirname(__file__), 'assets', 'splash.png')

        # Load Splash Image
        self.done_load_modal = ImageModal(splash_image)
        
        # Set App Communications
        self.communications = Communications()

        Builder.load_file("main.kv")
        sm = ScreenHandler()
        self.root_screen_manager = sm


        # Important Component Desigm
        Builder.load_string(section_icon.kv_section_layout)
        Builder.load_string(text_input.text_input_kv)
        Builder.load_string(app_button.kv_app_button)
        Builder.load_string(label_clickable.kv_label_clickable)
        Builder.load_string(top_form_buttons.kv_header_buttons)

        
        Builder.load_string(process_modal.kv_process_modal)
        self.process_modal = process_modal.ProcessingLayout()  

        Clock.schedule_once(self.show_welcome_popup)
        
        try:
            user_data_path = os.path.join(os.path.dirname(__file__), 'user_data.json')
            with open(user_data_path, 'r') as f:
                user_data = json.load(f)
        except Exception as e:
            print(f"Error loading user data: {e}")
            user_data = {}
        
        
        has_account = user_data.get('has_account')
        if has_account:
            # First Load the Login Screen
            starting_kv_path = os.path.join(os.path.dirname(__file__), 'screen_login', 'screen_login.kv')
            Builder.load_file(starting_kv_path)
            self.root_screen_manager.add_handler_screen(LOGIN_SCREEN)
            self.root_screen_manager.change_screen(LOGIN_SCREEN)
        else:
            starting_kv_path = os.path.join(os.path.dirname(__file__), 'screen_first_time', 'screen_first_time.kv')
            Builder.load_file(starting_kv_path)
            self.root_screen_manager.add_handler_screen(FIRST_TIME_SCREEN)
            self.root_screen_manager.change_screen(FIRST_TIME_SCREEN)


        Window.bind(size=self.on_window_resize) # bind the on_window_resize method to the window size event
        return sm

    def show_welcome_popup(self, *args):
        self.done_load_modal.animate_opening()  
    
    def close_welcome_popup(self, *args):
        self.done_load_modal.animate_closing()

    def load_screens(self, *args):  
        # try:
        #     user_data_path = os.path.join(os.path.dirname(__file__), 'user_data.json')
        #     with open(user_data_path, 'r') as f:
        #         user_data = json.load(f)
        # except Exception as e:
        #     print(f"Error loading user data: {e}")
        #     user_data = {}
        
        # has_account = user_data.get('has_account')
        # if has_account:
        #     # First Load the Login Screen
        #     starting_kv_path = os.path.join(os.path.dirname(__file__), 'screen_login', 'screen_login.kv')
        #     Builder.load_file(starting_kv_path)
        #     self.root_screen_manager.add_handler_screen(LOGIN_SCREEN)
        #     self.root_screen_manager.change_screen(LOGIN_SCREEN)
        # else:
        #     starting_kv_path = os.path.join(os.path.dirname(__file__), 'screen_first_time', 'screen_first_time.kv')
        #     Builder.load_file(starting_kv_path)
        #     self.root_screen_manager.add_handler_screen(FIRST_TIME_SCREEN)
        #     self.root_screen_manager.change_screen(FIRST_TIME_SCREEN)
        pass





    def load_user_map_verification_modal(self, *args):
        Builder.load_string(verify_user_location_modal.kv_verify_user_location_modal)
        self.user_map_verification_modal = verify_user_location_modal.UserVerificationMapModal()

    def load_all_registrations_modal(self, *args): 
        Builder.load_string(next_step_modal.kv_next_step_modal)
        Builder.load_string(application_number_modal.kv_application_number_modal)
        Builder.load_string(activate_account_modal.kv_activate_account_modal)

        self.next_step_modal = next_step_modal.NextStepModal()
        self.application_number_modal = application_number_modal.ApplicationNumberModal()
        self.activate_account_modal = activate_account_modal.ActivateAccountModal()


    def load_all_home_screen_modal(self, *args):
        Builder.load_string(logout_modal.kv_logout_modal)
        Builder.load_string(add_ticket_modal.kv_add_ticket_modal)

        self.logout_modal = logout_modal.LogoutModal()
        self.add_ticket_modal = add_ticket_modal.AddTicketModal()





    def on_window_resize(self, *args):
        if not self._resize_scheduled:
            self._resize_scheduled = True
            Clock.schedule_once(self._run_resize_events, 0.1)  # debounce: 100ms

    def _run_resize_events(self, *args):
        for event in self.on_size_events_of_all_widgets:
            try:
                event()
            except Exception as e:
                print(f"Resize event error: {e}")
        print("Window resized to: ", Window.size)
        self._resize_scheduled = False

    def _clear_cache_folder(self):
        cache_dir = os.path.join(os.path.dirname(__file__), 'cache')
        if os.path.isdir(cache_dir):
            try:
                # delete everything inside “cached”
                shutil.rmtree(cache_dir)
                # recreate empty folder so your code never breaks on next run
                os.makedirs(cache_dir, exist_ok=True)
                print("Cache cleared.")
            except Exception as e:
                # silently ignore or log
                print("Failed to clear cache:", e)
        else:
            print("Cache directory does not exist.")



if __name__ == '__main__':
    LabelBase.register(name="p_extrabold", fn_regular=os.path.join(os.path.dirname(__file__), 'fonts', 'Poppins-ExtraBold.ttf'))
    LabelBase.register(name="p_bold", fn_regular=os.path.join(os.path.dirname(__file__), 'fonts', 'Poppins-Bold.ttf'))
    LabelBase.register(name="p_extralight", fn_regular=os.path.join(os.path.dirname(__file__), 'fonts', 'Poppins-ExtraLight.ttf'))
    LabelBase.register(name="p_regular", fn_regular=os.path.join(os.path.dirname(__file__), 'fonts', 'Poppins-Regular.ttf'))
    LabelBase.register(name="p_light", fn_regular=os.path.join(os.path.dirname(__file__), 'fonts', 'Poppins-Light.ttf'))
    LabelBase.register(name="p_medium", fn_regular=os.path.join(os.path.dirname(__file__), 'fonts', 'Poppins-Medium.ttf'))
    LabelBase.register(name="p_italic", fn_regular=os.path.join(os.path.dirname(__file__), 'fonts', 'Poppins-Italic.ttf'))
    LabelBase.register(name="p_mediumitalic", fn_regular=os.path.join(os.path.dirname(__file__), 'fonts', 'Poppins-MediumItalic.ttf'))
    LabelBase.register(name="p_semibold", fn_regular=os.path.join(os.path.dirname(__file__), 'fonts', 'Poppins-SemiBold.ttf'))
    
    
    try:
        SubscriberApp().run()
    except KeyboardInterrupt:
        print("KeyboardInterrupt detected. Exiting...")
    except Exception as e:
        print(f"Error: {e}")
    