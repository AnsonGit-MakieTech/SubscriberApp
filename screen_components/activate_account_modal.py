
from kivy.uix.modalview import ModalView
 
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout

import os
 
from kivy.uix.behaviors import ButtonBehavior
from kivymd.app import MDApp

from kivy.properties import ObjectProperty, NumericProperty, StringProperty , ListProperty, BooleanProperty
from kivymd.uix.behaviors import CommonElevationBehavior, RectangularRippleBehavior
from kivymd.uix.boxlayout import MDBoxLayout 
from kivy.utils import get_color_from_hex


class ActivateAccountModal(ModalView):
    content_background_radius = ListProperty([ 8 , 8, 8 , 8 ])



kv_activate_account_modal = '''



'''





