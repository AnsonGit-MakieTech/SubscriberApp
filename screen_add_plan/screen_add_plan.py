

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty , ListProperty, BooleanProperty
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
if platform == "android":
    from plyer import gps 

from kivy_garden.mapview import MapView, MapSource , MapMarker # Make sure mapview is installed

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

class SingleMarkerMapView(MapView):
    current_marker : MapMarker = ObjectProperty(None)
    current_marker_size : int = NumericProperty(20)

    is_map_clicked_not_colliding = ObjectProperty(None)
    

    def on_touch_up(self, touch): 
        if self.collide_point(*touch.pos) and self.is_map_clicked_not_colliding():
            # convert screen xy → lat, lon
            lat, lon = self.get_latlon_at(*touch.pos)

            # remove existing marker
            if self.current_marker:
                self.remove_widget(self.current_marker)
            
            parent_dir = os.path.dirname(os.path.dirname(__file__))

            # add a new one
            self.current_marker = MapMarker(
                lat=lat,
                lon=lon,
                source=os.path.join(parent_dir, 'assets', 'map_marker.png'),
                size_hint=(None, None),
            )
            self.current_marker.height = self.current_marker_size
            self.current_marker.width = self.current_marker_size
            self.add_widget(self.current_marker)

            # print out the chosen coords
            print(f"Selected location → lat: {lat:.6f}, lon: {lon:.6f}")
            return True

        return super().on_touch_up(touch)


class AddPlanScreen(Screen):
    
    holder = ObjectProperty(None)
    map_view = ObjectProperty(None)
    is_map_labeled = BooleanProperty(True)

    button_timeout = NumericProperty(2)
    is_okey_to_click = BooleanProperty(True)

    header_button_padding = NumericProperty(5)
    header_button_spacing = NumericProperty(5)
    header_height = NumericProperty(30)

    home_icon = StringProperty('')
    city_icon = StringProperty('')
    question_icon = StringProperty('')
    bag_icon = StringProperty('')
    change_map_icon = StringProperty('')

    selected_city = StringProperty('Click here to select available city')
    header_font_size = NumericProperty(12)
    selected_plan = StringProperty('Find the best plan for you')
    
    is_map_clicked_not_colliding = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(AddPlanScreen, self).__init__(**kwargs)
        self.opacity = 0

        parent_dir = os.path.dirname(os.path.dirname(__file__))
        self.home_icon = os.path.join(parent_dir, 'assets', 'house_icon.png')
        self.city_icon = os.path.join(parent_dir, 'assets', 'city_icon.png')
        self.question_icon = os.path.join(parent_dir, 'assets', 'q_a_icon.png')
        self.bag_icon = os.path.join(parent_dir, 'assets', 'bag_icon.png')
        self.change_map_icon = os.path.join(parent_dir, 'assets', 'change_map_icon.png')

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

        self.header_font_size = int(min( width, height) * 0.03)
        if self.header_font_size > 15:
            self.header_font_size = 15

        self.header_height = int(min( width, height) * 0.08)
        if self.header_height > 30:
            self.header_height = 30
        

        # print(f"width: {width}, height: {height}, header_height: {self.header_height}")



    def on_touch_down(self, touch):
        self.is_map_clicked_not_colliding = True
        if self.mapview and self.mapview.collide_point(*touch.pos):
            # 2) …give each overlaid widget a shot at it 
            for child in self.holder.children:
                if child is not self.mapview and child.collide_point(*touch.pos):
                    self.is_map_clicked_not_colliding = False
                    
        return super().on_touch_down(touch)

    

    def on_enter(self, *args):
        main_app  = MDApp.get_running_app() 
        anim = Animation(opacity=1, duration=0.5)
        anim.bind( on_start= main_app.on_window_resize)
        anim.start(self)
        Clock.schedule_once(self.load_map_view, 0.1)

        return super().on_enter(*args)


    def check_is_map_clicked_not_colliding(self, *args):
        return self.is_map_clicked_not_colliding

    def load_map_view(self, *args):
        if self.holder is None:
            Clock.schedule_once(self.load_map_view, 0.2)
            return
        
        if self.map_view is None:
            self.mapview = SingleMarkerMapView(
                lat=DEFAULT_LAT, 
                lon=DEFAULT_LON, 
                zoom=25,
                map_source=map_source_labeled,
                size_hint=(1, 1),
                pos_hint={"center_x": 0.5, "center_y": 0.5}
            ) 
            self.mapview.is_map_clicked_not_colliding = self.check_is_map_clicked_not_colliding
            self.mapview.bind(lat=self.on_map_move, lon=self.on_map_move)
            self.holder.add_widget(self.mapview, index=len(self.holder.children))

            if platform == "android":
                try:
                    gps.configure(on_location=self.gps_callback, on_status=self.gps_status)
                    gps.start(minTime=1000, minDistance=1)
                except NotImplementedError:
                    print("GPS not implemented on this platform")
                    self.go_to_location(DEFAULT_LAT, DEFAULT_LON)
                except Exception as e:
                    print(f"Error starting GPS: {e}")
                    self.go_to_location(DEFAULT_LAT, DEFAULT_LON)
            else:
                self.go_to_location(DEFAULT_LAT, DEFAULT_LON)

            # Clock.schedule_interval(self.change_map_source, 1)

    def change_map_source(self, *args):
        if self.mapview is None:
            return
        
        if self.is_okey_to_click == False:
            return 
        
        self.is_okey_to_click = False
        Clock.schedule_once( self.update_is_okey_to_click , self.button_timeout)
        # self.mapview.pause_on_action = False
        if self.is_map_labeled:
            self.mapview.map_source = map_source_satlite
            self.is_map_labeled = False
            
        else:
            self.mapview.map_source = map_source_labeled
            self.is_map_labeled = True
        self.mapview.remove_all_tiles()
        self.mapview.trigger_update(full=True)  #– this tells MapView “please re‐build everything” :contentReference[oaicite:1]{index=1}
        print("change_map_source")
        # self.mapview.pause_on_action = True  # (optionally) restore original behavior
        # new_zoom = max(self.mapview.min_zoom, self.mapview.zoom - 1)
        # self.mapview.zoom = new_zoom


    def update_is_okey_to_click(self, *args):
        self.is_okey_to_click = True
        

    def on_map_move(self, *args):
        """ Called when user pans the map. """
        if self.mapview:
            self.lat_data = self.mapview.lat
            self.lon_data = self.mapview.lon  
            lat = f"{round(self.lat_data, 25)}.." if len(str(self.lat_data)) > 25 else self.lat_data
            lon = f"{round(self.lon_data, 25)}.." if len(str(self.lon_data)) > 25 else self.lon_data 
            print(f"📍 Map center updated → Lat: {lat}, Lon: {lon}")


    def get_center_coords(self):
        """ Call this when you want to access the map center directly. """
        if self.mapview:
            return self.mapview.lat, self.mapview.lon
        return None, None

    def go_to_location(self , new_lat , new_lon): 
        self.lat_data = new_lat
        self.lon_data = new_lon
        try:
            if self.mapview:
                self.mapview.center_on(new_lat, new_lon)
                self.mapview.zoom = 16  # Optional: adjust zoom for better clarity
                self.mapview.min_zoom = 1
                self.mapview.max_zoom = 17
            else:
                Clock.schedule_once(self.load_map, 0.3)
                Clock.schedule_once( lambda *args: self.go_to_location(new_lat, new_lon), 0.3)
        except Exception as e:
            # print(f"Error: {e}")
            pass



















