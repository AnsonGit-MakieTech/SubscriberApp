from kivy.uix.accordion import Animation
from kivy.uix.actionbar import Button
 
from kivymd.uix.label import MDIcon   
from kivy.properties import ObjectProperty, NumericProperty, StringProperty , BooleanProperty 
from kivy.metrics import  sp  
from kivy.uix.textinput import TextInput
from kivy.uix.modalview import ModalView 
from kivy_garden.mapview import MapView
import os
from kivy.clock import Clock
from kivy.uix.modalview import ModalView
from kivy_garden.mapview import MapView, MapSource 
from kivy.properties import ObjectProperty, NumericProperty, DictProperty

from kivy.utils import get_color_from_hex as chex 
from kivy.utils import platform
# from utils.app_utils import is_valid_latlon 
from kivymd.app  import MDApp

if platform == "android":
    from plyer import gps 
from kivy import platform
import os

if platform == "win":
    from plyer import filechooser
if platform == "android":
    from android.storage import app_storage_path
    from androidstorage4kivy import SharedStorage, Chooser
 
from kivy_garden.mapview import MapView, MapSource  # Make sure mapview is installed

# Optional: Custom tile server or use default
# map_source = MapSource(url="http://c.tile.openstreetmap.org/{z}/{x}/{y}.png",
#                        cache_key="osm",
#                        tile_size=256,
#                        image_ext="png")
map_source = MapSource(
    url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    cache_key="satellite",
    tile_size=256,
    image_ext="jpg",  # Esri tiles are usually JPG
    attribution="Tiles © Esri — Source: Esri, Earthstar Geographics"
)











class UserVerificationMapModal(ModalView):
    map_obj = ObjectProperty(None)
    lat : str = StringProperty('[font=p_bold]Latitude :[/font] [font=p_light]0[/font]')
    lon : str = StringProperty('[font=p_bold]Longitude :[/font] [font=p_light]0[/font]')
    lon_data : float = NumericProperty(0)
    lat_data : float = NumericProperty(0)
    location_input : TextInput = ObjectProperty(None)
    is_valid_location : bool = BooleanProperty(False)

    parent_event : object = ObjectProperty(None)

    layout_spacing = NumericProperty(10)
    map_input_height = NumericProperty(100)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.opacity = 0
        self.mapview = None  # 👈 store MapView instance
    
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
        width, height = self.size

        self.map_input_height = width * 0.4
        if self.map_input_height > 100:
            self.map_input_height = 100

    def on_kv_post(self, base_widget):
        # Ensure location_input is set and bind an event
        if self.location_input:
            # self.location_input.bind(text=self.on_location_change)
            pass


    def on_location_change(self, instance, value):
        # print(f"📍 Location input changed to: {value}")
        if is_valid_latlon(value):
            self.is_valid_location = True 
            lat_str, lon_str = value.split(",")
            lat = float(lat_str.strip())
            lon = float(lon_str.strip())
            self.go_to_location(lat, lon)
        else:
            self.is_valid_location = False

    def on_open(self, *args):
        anim = Animation(opacity=1, duration=0.3)
        anim.bind(on_start=self.update_sizing)
        anim.start(self)


        # if platform == "android":
        #     try:
        #         gps.configure(on_location=self.gps_callback, on_status=self.gps_status)
        #         gps.start(minTime=1000, minDistance=1)
        #     except NotImplementedError:
        #         print("GPS not implemented on this platform")
        #         self.go_to_location(12.367796960, 123.62151820)
        #     except Exception as e:
        #         print(f"Error starting GPS: {e}")
        #         self.go_to_location(12.367796960, 123.62151820)
        # else:
        #     self.go_to_location(12.367796960, 123.62151820)  # fallback

    def gps_status(self, status_type, status):
        # print(f"GPS Status → {status_type}: {status}")
        pass
    
    def gps_callback(self, **kwargs):
        self.lat_data = float(kwargs.get('lat', 0))
        self.lon_data = float(kwargs.get('lon', 0))
        # print(f"📡 GPS location received → Lat: {self.lat_data}, Lon: {self.lon_data}")
        self.go_to_location(self.lat_data, self.lon_data)
        gps.stop()  # Stop after getting one location fix

    def load_map(self, *args): 
        print("Loading map...")
        if self.map_obj is None:
            print("Map object is None, scheduling load_map again...")
            Clock.schedule_once(self.load_map, 0.3)
            return

        if not self.ids.map.children:
            try:
                # if not has_internet():
                #     return
                
                self.mapview = MapView(lat=12.367796960, lon=123.62151820, zoom=25,
                                map_source=map_source,
                                size_hint=(1, 1),
                                pos_hint={"center_x": 0.5, "center_y": 0.5})
                # Optional: bind to map position updates
                self.mapview.bind(lat=self.on_map_move, lon=self.on_map_move)

                self.map_obj.add_widget(self.mapview)
                marker_icon = MDIcon(icon="home-map-marker",
                                    font_size=sp(58), 
                                    theme_text_color="Custom",
                                    text_color=chex("#B71E1E"),
                                    pos_hint={"center_x": 0.5, "center_y": 0.5}
                                    )
                self.map_obj.add_widget(marker_icon)
            except Exception as e:
                print(f"Error loading map: {e}")
                pass

    def on_map_move(self, *args):
        """ Called when user pans the map. """
        if self.mapview:
            self.lat_data = self.mapview.lat
            self.lon_data = self.mapview.lon 
            # print(f"📍 Map center updated → Lat: {self.lat_data}, Lon: {self.lon_data}")
            self.parent_event(lat_data = self.lat_data, lon_data = self.lon_data)
            lat = f"{round(self.lat_data, 10)}.." if len(str(self.lat_data)) > 10 else self.lat_data
            lon = f"{round(self.lon_data, 10)}.." if len(str(self.lon_data)) > 10 else self.lon_data
            self.lat = f"[font=p_bold]Latitude :[/font] [font=p_light]{lat}[/font]"
            self.lon = f"[font=p_bold]Longitude :[/font] [font=p_light]{lon}[/font]"
            
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


kv_verify_user_location_modal = '''

<UserVerificationMapModal>:

    # map_obj : map_obj
    # location_input : location_input

    size_hint: 1, 1
    auto_dismiss: True
    background: ""
    background_color: 0, 0, 0, 0

    canvas.before:
        Color:
            rgb: chex("#5C5470")
            a: 0.5
        Rectangle:
            pos: self.pos
            size: self.size

    
    BoxLayout:
        orientation:'vertical' 
        spacing: root.layout_spacing
        size_hint: 0.85 , 0.9
        pos_hint: { 'center_x': 0.5 , 'center_y': 0.5 }  
        
        Button:
            size_hint: 1, None
            height: root.map_input_height

        Button:
            size_hint: 1, 1
            
        

        



'''