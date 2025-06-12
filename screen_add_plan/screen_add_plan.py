

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty , ListProperty
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

from kivy_garden.mapview import MapView, MapSource  # Make sure mapview is installed

# Optional: Custom tile server or use default
map_source_labeled = MapSource(url="http://c.tile.openstreetmap.org/{z}/{x}/{y}.png",
                       cache_key="osm",
                       tile_size=256,
                       image_ext="png")
map_source_satlite = MapSource(
    url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    cache_key="satellite",
    tile_size=256,
    image_ext="jpg",  # Esri tiles are usually JPG
    attribution="Tiles © Esri — Source: Esri, Earthstar Geographics",
    max_zoom = 17, 
    min_zoom = 5
)



class ScreenAddPlan(Screen):
    pass
