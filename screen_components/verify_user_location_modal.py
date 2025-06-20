

 
from kivymd.uix.label import MDIcon   
from kivy.properties import ObjectProperty, NumericProperty, StringProperty , BooleanProperty , ListProperty
from kivy.metrics import  sp  
from kivy.uix.textinput import TextInput
from kivy.uix.modalview import ModalView 
from kivy_garden.mapview import MapView
from kivy.uix.image import Image
import os
from kivy.clock import Clock
from kivy.uix.modalview import ModalView
from kivy_garden.mapview import MapView, MapSource 
from kivy.properties import ObjectProperty, NumericProperty, DictProperty

from kivy.utils import get_color_from_hex as chex 
from kivy.utils import platform
# from utils.app_utils import is_valid_latlon 
from kivymd.app  import MDApp
from kivy.animation import Animation

if platform == "android":
    from plyer import gps 

from kivy import platform
import os
from screen_components import text_input 
from variables import *

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
    attribution="Tiles © Esri — Source: Esri, Earthstar Geographics",
    max_zoom = 17, 
    min_zoom = 5
)











class UserVerificationMapModal(ModalView):
    map_obj = ObjectProperty(None)
    lat : str = StringProperty('[font=p_bold]Latitude :[/font] [font=p_light]0[/font]')
    lon : str = StringProperty('[font=p_bold]Longitude :[/font] [font=p_light]0[/font]')
    lon_data : float = NumericProperty(0)
    lat_data : float = NumericProperty(0)
    location_input : text_input.OneLineInput  = ObjectProperty(None)
    is_valid_location : bool = BooleanProperty(False)
    mapview : MapView = ObjectProperty(None)

    parent_event : object = ObjectProperty(None)

    layout_spacing = NumericProperty(10)
    layout_padding = ListProperty([10, 10, 10, 10])
    map_input_height = NumericProperty(100)
    layout_radius = ListProperty([10, 10, 10, 10])

    h4_font_size = NumericProperty(18)
    h2_font_size = NumericProperty(18) 

    map_marker = ObjectProperty(None)



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
        # if self.map_input_height > 100:
        #     self.map_input_height = 100
        
        r = int(min(width, height) * 0.03)  # You can change 0.05 to any fraction
        self.layout_radius = [r, r, r, r]
        cpad = int(min(width, height) * 0.03)
        self.layout_padding = [cpad, cpad, cpad, cpad]

        self.h4_font_size = int(min(width, height) * 0.03)
        # if self.h4_font_size > 12:
        #     self.h4_font_size = 12
        self.h2_font_size = int(min(width, height) * 0.04)
        # if self.h2_font_size > 17:
        #     self.h2_font_size = 17
        
        map_icon_size = int(min(width, height) * 0.06)
        # if map_icon_size > 30:
        #     map_icon_size = 30
        self.map_marker.size = (map_icon_size, map_icon_size)
        print(f"📍 map_icon_size: {self.map_marker.size}")

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

    def on_dismiss(self):
        self.opacity = 0
        return super().on_dismiss()

    def on_open(self, *args):
        self.location_input.costumized_input(hint_text="Enter Your Copied Location", halign="center")
        anim = Animation(opacity=1, duration=0.3)
        anim.bind(on_start=self.update_sizing, on_progress=self.location_input.setup_layout)
        anim.start(self)

        # if platform == "android":
        #     try:
        #         gps.configure(on_location=self.gps_callback, on_status=self.gps_status)
        #         gps.start(minTime=1000, minDistance=1)
        #     except NotImplementedError:
        #         print("GPS not implemented on this platform")
        #         self.go_to_location(DEFAULT_LAT, DEFAULT_LON)
        #     except Exception as e:
        #         print(f"Error starting GPS: {e}")
        #         self.go_to_location(DEFAULT_LAT, DEFAULT_LON)
        # else:
        #     self.go_to_location(DEFAULT_LAT, DEFAULT_LON)  # fallback

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
        if len(self.map_obj.children) == 0:
            try:
                # if not has_internet():
                #     return
                
                self.mapview = MapView(lat=DEFAULT_LAT, lon=DEFAULT_LON, zoom=25,
                                map_source=map_source,
                                size_hint=(1, 1),
                                pos_hint={"center_x": 0.5, "center_y": 0.5})
                # Optional: bind to map position updates
                self.mapview.bind(lat=self.on_map_move, lon=self.on_map_move)

                self.map_obj.add_widget(self.mapview)
                
                parent_dir = os.path.dirname(os.path.dirname(__file__))  
                self.map_marker = marker_icon = Image(
                    source=os.path.join(parent_dir, 'assets', 'map_house.png'),
                    keep_ratio=True,
                    allow_stretch=True,
                    size_hint = (None, None),
                    size=(20 , 20), 
                    pos_hint={"center_x": 0.5, "center_y": 0.5}
                    )
                self.map_obj.add_widget(self.map_marker)
            except Exception as e:
                print(f"Error loading map: {e}")
                pass

    def on_map_move(self, *args):
        """ Called when user pans the map. """
        if self.mapview:
            self.lat_data = self.mapview.lat
            self.lon_data = self.mapview.lon 
            # print(f"📍 Map center updated → Lat: {self.lat_data}, Lon: {self.lon_data}")
            if self.parent_event is not None:
                self.parent_event(lat_data = self.lat_data, lon_data = self.lon_data)
            lat = f"{round(self.lat_data, 25)}.." if len(str(self.lat_data)) > 25 else self.lat_data
            lon = f"{round(self.lon_data, 25)}.." if len(str(self.lon_data)) > 25 else self.lon_data
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

    map_obj : map_obj
    location_input : location_input

    size_hint: 1, 1
    auto_dismiss: True
    background: ""
    background_color: 0, 0, 0, 0
    overlay_color : 0, 0, 0, 0

    canvas.before:
        Color:
            rgb: chex("#B9B4C7")
            a: 0.5
        Rectangle:
            pos: self.pos
            size: self.size

    
    BoxLayout:
        orientation:"vertical" 
        spacing: root.layout_spacing
        size_hint: 0.85 , 0.9
        pos_hint: { "center_x": 0.5 , "center_y": 0.5 }  
        
        MDBoxLayout:
            size_hint: 1, None
            height: root.map_input_height
            md_bg_color: chex("#352F44")
            radius: root.layout_radius
            orientation: 'vertical'
            padding : root.layout_padding

            Label:
                size_hint: 1, 0.6 
                font_size: root.h4_font_size
                halign: "center"
                valign: "middle" 
                text_size: self.size
                font_name: "p_light"
                text: "If the map below is not loading, paste the location you copied from Google Maps instead."
                color: chex("#FFFFFF")
    
            OneLineInput:
                id: location_input
                size_hint: 1, 0.4

        
        MDBoxLayout:
            size_hint: 1, 1
            md_bg_color: chex("#352F44")
            radius: root.layout_radius
            padding : root.layout_padding
            orientation: 'vertical'

            Label:
                size_hint: 1, 0.1
                font_size: root.h4_font_size
                halign: "center"
                valign: "middle" 
                text_size: self.size
                font_name: "p_bold"
                text: "Drag the map to position the marker over your current location."
                color: chex("#FFFFFF")

                            
                        
            Widget:
                size_hint: 1, 0.05

            FloatLayout:
                id: map_obj
                size_hint: 1, 0.5
            
                
                # canvas.before:
                #     Color:
                #         rgb: chex("#A30000")
                #         a: 0.5
                #     Rectangle:
                #         pos: self.pos
                #         size: self.size
            
            Label:
                size_hint: 1, 0.1
                font_size: root.h4_font_size
                halign: "center"
                valign: "middle" 
                text_size: self.size
                font_name: "p_regular"
                text: "These are the latitude and longitude of your selected location."
                color: chex("#FFFFFF")


            Label:
                size_hint: 1, 0.05
                font_size: root.h4_font_size
                halign: "left"
                valign: "middle" 
                text_size: self.size
                font_name: "p_light"
                # text: "Latitude : 13.00"
                text: root.lat
                color: chex("#FFFFFF")
                markup: True


            Label:
                size_hint: 1, 0.05
                font_size: root.h4_font_size
                halign: "left"
                valign: "middle" 
                text_size: self.size
                font_name: "p_light"
                # text: "Latitude : 13.00"
                text: root.lon
                color: chex("#FFFFFF")
                markup: True




            Widget:
                size_hint: 1, 0.02

            BoxLayout:
                size_hint: 1, 0.06
                
                AppButton: 
                    size_hint: 0.4, 1 
                    md_bg_color: chex("#A30000")
                    Label:
                        text: "Cancel"
                        font_size: root.h2_font_size
                        font_name: "p_bold"
                        color: chex("#FFFFFF")
                
                Widget:
                    size_hint: 0.2, 1
            
                AppButton: 
                    size_hint: 0.4, 1 
                    md_bg_color: chex("#05B51A")
                    Label:
                        text: "Submit"
                        font_size: root.h2_font_size
                        font_name: "p_bold"
                        color: chex("#FFFFFF")

            Widget:
                size_hint: 1, 0.02
            
            
            
        

        



'''