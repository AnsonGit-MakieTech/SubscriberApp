__version__ = "1.0.0"

from kivy.uix.accordion import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivy.lang.builder import Builder
from kivy.core.text import LabelBase
from kivy.utils import platform, get_color_from_hex

from variables import *
import os
import json

from kivy.config import Config
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.modalview import ModalView
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from communications  import Communications
from kivy.logger import Logger
from kivy.animation import Animation

if platform == "android": 
    from android.permissions import request_permissions, Permission, check_permission  # pylint: disable=import-error

if platform == "ios":
    pass

from kivy.core.window import Window
Window.show_cursor = True


# Set Window Size Before App Starts if platform is 
if platform == "win":
    Window.size = (320, 568)




from kivy.uix.image import Image
from kivy.uix.modalview import ModalView
from kivy.graphics import Color, Rectangle 

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
            Color(*get_color_from_hex('#ABCFE3'))  # Light blue background
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


class SubscriberApp(MDApp):
 
    communications : dict = None
    done_load_modal : ImageModal = ObjectProperty(None)
    root_screen_manager : ScreenHandler = ObjectProperty(None)


    def on_start(self):
        """ Check and request storage permission on Android """

        if platform == "android":
            if self.check_permissions():
                # print("✅ Storage permission already granted.")
                pass
            else:
                # print("❌ Storage permission NOT granted. Requesting now...")
                request_permissions([
                    Permission.INTERNET,
                    Permission.ACCESS_FINE_LOCATION,
                    Permission.ACCESS_COARSE_LOCATION,
                    Permission.READ_MEDIA_IMAGES,
                    Permission.READ_MEDIA_VIDEO,
                    Permission.READ_MEDIA_AUDIO,
                    Permission.READ_EXTERNAL_STORAGE,
                    Permission.WRITE_EXTERNAL_STORAGE,
                ])
        # Defer screen loading after UI is visible
        Clock.schedule_once(self.load_screens, 0.1)


    def check_permissions(self):
        """ Check if READ/WRITE storage permissions are granted """
        if platform == "android":
            perms = [
                Permission.INTERNET,
                Permission.ACCESS_FINE_LOCATION,
                Permission.ACCESS_COARSE_LOCATION,
                Permission.READ_MEDIA_IMAGES,
                Permission.READ_MEDIA_VIDEO,
                Permission.READ_MEDIA_AUDIO,
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE,
            ] 
            return all(check_permission(p) for p in perms)
        return True  # ✅ Assume granted on other platforms
    

    def on_stop(self):
        try:
            # Close communications
            self.communications.kill_all_threads()
        except Exception as e:
            # print(f"Error saving user data: {e}")
            pass

    def on_pause(self):
        Clock.schedule_once(self.show_welcome_popup, 0.1) 
        return super().on_pause()

    def build(self):
        self.theme_cls.primary_dark = get_color_from_hex("#352F44")

        # Set App Icon
        self.icon = os.path.join(os.path.dirname(__file__), 'assets', 'app_logo.png')
        splash_image = os.path.join(os.path.dirname(__file__), 'assets', 'splash.png')

        self.done_load_modal = ImageModal(splash_image)
        # Set App Communications
        self.communications = Communications()

        Builder.load_file("main.kv")
        sm = ScreenHandler()
        self.root_screen_manager = sm

        def change_to_login_screen(*args):
            print("this happen hehehee")
            # self.root_screen_manager.current = LOGIN_SCREEN
        Clock.schedule_once(self.show_welcome_popup, 0.5)
        Clock.schedule_once(change_to_login_screen, 1)
        return sm

    def show_welcome_popup(self, *args):
        self.done_load_modal.animate_opening()
        def close_popup(*args):
            self.done_load_modal.animate_closing()
        Clock.schedule_once(close_popup, 1)

    def load_screens(self, *args):
        pass

if __name__ == '__main__':
    # LabelBase.register(name="roboto_extrabolditalic", fn_regular=os.path.join(os.path.dirname(__file__), 'fonts', 'Roboto-ExtraBoldItalic.ttf'))
    try:
        SubscriberApp().run()
    except KeyboardInterrupt:
        print("KeyboardInterrupt detected. Exiting...")
    except Exception as e:
        print(f"Error: {e}")
    