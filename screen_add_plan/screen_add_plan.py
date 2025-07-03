

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
from kivymd.uix.boxlayout import MDBoxLayout  
from kivy.utils import get_color_from_hex
from kivymd.uix.behaviors import CommonElevationBehavior, RectangularRippleBehavior
from kivy.core.text import Label as CoreLabel
from kivy.uix.label import Label
from variables import *
from kivy.uix.widget import Widget
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


class AddPlanInformation(
    CommonElevationBehavior, 
    MDBoxLayout
):
    content_background_radius = ListProperty([ 8 , 8, 0 , 0 ])
    button_background_radius = ListProperty([ 8 , 8, 0 , 0 ])

    header_font_size = NumericProperty(20)
    content_font_size = NumericProperty(15)

    bag_icon = StringProperty("")

    plan_name_label : Label = ObjectProperty(None)
    plan_monthly_label : Label = ObjectProperty(None)
    plan_speed_label : Label = ObjectProperty(None)


    max_content_font_size = NumericProperty(11)
    min_content_font_size = NumericProperty(1)
    padding_x = NumericProperty(5)
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs) 
        self.md_bg_color = get_color_from_hex('#FFFFFF')
        
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        self.bag_icon = os.path.join(parent_dir, 'assets', 'bag_black_icon.png')
 
    def setup_ui(self, plan_name, plan_monthly, plan_speed):
        self.plan_name_label.text = plan_name
        self.plan_monthly_label.text = plan_monthly
        self.plan_speed_label.text = plan_speed
        

    def update_sizing(self, *args):
        width , height = self.size 
        rad = int(min(width, height) * 0.10)
        self.content_background_radius = [rad, rad, 0, 0]

        rad = int(min(width, height) * 0.03)
        self.button_background_radius = [rad, rad, rad, rad]

        self.header_font_size = int( width  * 0.04)
        if self.header_font_size > 13:
            self.header_font_size = 13

        if self.plan_name_label is not None:
            self.update_content_font_size(self.plan_name_label) 
        if self.plan_monthly_label is not None:
            self.update_content_font_size(self.plan_monthly_label)
        if self.plan_speed_label is not None:
            self.update_content_font_size(self.plan_speed_label)


    def update_content_font_size(self, widget_label ):
        width , height = self.size 
        if widget_label is not None:
            # 1) start with your old “responsive” guess
            fs = int(width * 0.03)
            fs = min(fs, self.max_content_font_size)
            fs = max(fs, self.min_content_font_size)

            # 2) now shrink until the text actually fits
            text = widget_label.text or ""
            avail = max(width - 2 * self.padding_x, 0)

            while fs > self.min_content_font_size:
                # measure via CoreLabel
                probe = CoreLabel(
                    text=text,
                    font_name=widget_label.font_name,
                    font_size=fs,
                )
                probe.refresh()
                text_w, _ = probe.texture.size
                if text_w <= avail:
                    break
                fs -= 1

            # 3) apply your finally chosen size
            self.content_font_size = fs

            # (optional) force the label to reflow
            widget_label.texture_update()

 
    def proceed_to_payment(self, *args):
        main_app  = MDApp.get_running_app()  
        if main_app.next_step_modal is not None: 
            main_app.next_step_modal.open()
            def button_action_for_payment(*args):
                print("Link to payment redirecting")
            main_app.next_step_modal.button_action_for_online = button_action_for_payment
            main_app.next_step_modal.button_action_for_visit = main_app.application_number_modal.open 


class SingleMarkerMapView(MapView):
    current_marker : MapMarker = ObjectProperty(None)
    current_marker_size : int = NumericProperty(20)

    check_is_map_clicked_not_colliding = ObjectProperty(None)
    

    def on_touch_up(self, touch): 
        print("Is colliding", self.collide_point(*touch.pos))
        print("Is colliding next step", self.check_is_map_clicked_not_colliding())
        print()
        print()
        print()
        if self.collide_point(*touch.pos) and self.check_is_map_clicked_not_colliding():
            # convert screen xy → lat, lon
            lat, lon = self.get_latlon_at(*touch.pos)

            # remove existing marker
            if self.current_marker:
                self.remove_custom_marker()
            
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

    def remove_custom_marker(self, *args):
        if isinstance(self.current_marker, MapMarker):
            self.remove_widget(self.current_marker)
            self.current_marker = Widget()


class AddPlanScreen(Screen):
    
    holder = ObjectProperty(None)

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
    selected_plan_text = StringProperty('Find the best plan for you')
    
    is_map_clicked_not_colliding = BooleanProperty(False)

    map_view : SingleMarkerMapView = ObjectProperty(None)
    has_map = BooleanProperty(False)
    lat_data = NumericProperty(0)
    lon_data = NumericProperty(0)

    add_plan_information : AddPlanInformation = ObjectProperty(None)
    footer_height  = NumericProperty(200)


    selected_plan = DictProperty({})
    
    is_verified = BooleanProperty(False)

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
         
        if self.add_plan_information is not None:
            self.add_plan_information.update_sizing()

        # print(f"width: {width}, height: {height}, header_height: {self.header_height}")

    def on_touch_down(self, touch):
        self.is_map_clicked_not_colliding = True
        if self.map_view and self.map_view.collide_point(*touch.pos):
            # 2) …give each overlaid widget a shot at it 
            for child in self.holder.children:
                if child is not self.map_view and child.collide_point(*touch.pos):
                    self.is_map_clicked_not_colliding = False
                    print(f"Colliding with {child}")
                
        print(f"on_touch_down : is_map_clicked_not_colliding: {self.is_map_clicked_not_colliding}")
        return super().on_touch_down(touch)

    
    def on_leave(self, *args):
        self.opacity = 0
        self.is_verified = False

        return super().on_leave(*args)

    def on_enter(self, *args):
        self.is_map_clicked_not_colliding = True
        main_app  = MDApp.get_running_app() 
        anim = Animation(opacity=1, duration=0.5)
        anim.bind( on_start= main_app.on_window_resize , on_complete = main_app.close_welcome_popup)
        anim.start(self)
        Clock.schedule_once(self.load_map_view, 0.1)

        Clock.schedule_once(self.load_connected_screen)

        self.selected_plan = main_app.app_data.get(APP_DATA_PLAN_KEY, {})
        self.display_selected_plan()
        return super().on_enter(*args)

    def display_selected_plan(self, *args):
        plan_name = self.selected_plan.get('name', "None")
        plan_monthly = f"{float(self.selected_plan.get('monthly', 0)):,.2f}" if self.selected_plan.get('monthly', 0) > 0 else "None"
        plan_speed = str(self.selected_plan.get('speed', "None"))
        self.add_plan_information.setup_ui(
            plan_name, 
            plan_monthly, 
            plan_speed
        )
        self.selected_plan_text = self.selected_plan.get('name', "Find the best plan for you")

    def load_connected_screen(self, *args):
        main_app  = MDApp.get_running_app()
        main_app.load_all_registrations_modal()
        main_app.on_window_resize()
        
        
        if not main_app.root_screen_manager.does_screen_exist(PRODUCT_SHOWCASE_SCREEN):
            main_app.root_screen_manager.builder_load_screen('screen_product_showcase', 'screen_product_showcase.kv', PRODUCT_SHOWCASE_SCREEN )
            main_app.root_screen_manager.add_handler_screen(PRODUCT_SHOWCASE_SCREEN)

    def select_available_plan(self, *args):
        main_app  = MDApp.get_running_app()
        Clock.schedule_once(main_app.show_welcome_popup)
        main_app.root_screen_manager.change_screen(PRODUCT_SHOWCASE_SCREEN)
    
    def go_to_home(self, *args):
        self.map_view.remove_custom_marker()
        main_app  = MDApp.get_running_app()
        Clock.schedule_once(main_app.show_welcome_popup) 
        main_app.app_data[APP_DATA_PLAN_KEY] = {}
        main_app.root_screen_manager.change_screen(HOME_SCREEN)


    def check_is_map_clicked_not_colliding(self, *args):
        print(f"is_map_clicked_not_colliding: {self.is_map_clicked_not_colliding}")
        return self.is_map_clicked_not_colliding

    def load_map_view(self, *args):
        if self.holder is None:
            Clock.schedule_once(self.load_map_view, 0.2)
            return
        
        if self.has_map:
            print("Already loaded map view")
            return
        print("Loading map view <=====================")
        self.map_view = SingleMarkerMapView(
            lat=DEFAULT_LAT, 
            lon=DEFAULT_LON, 
            zoom=25,
            map_source=map_source_labeled,
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        ) 
        self.map_view.check_is_map_clicked_not_colliding = self.check_is_map_clicked_not_colliding
        self.map_view.bind(lat=self.on_map_move, lon=self.on_map_move)
        self.holder.add_widget(self.map_view, index=len(self.holder.children))
        self.has_map = True
        print("Mapview object : ", self.map_view)

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
        if not self.map_view or not self.is_okey_to_click:
            return 
        self.is_okey_to_click = False
        Clock.schedule_once( self.update_is_okey_to_click , self.button_timeout)
        # self.map_view.pause_on_action = False
        if self.is_map_labeled:
            new_src = map_source_satlite
        else:
            new_src = map_source_labeled
        self.is_map_labeled = not self.is_map_labeled

        # swap and clamp zoom
        self.map_view.map_source = new_src
        z = self.map_view.zoom
        z = max(new_src.min_zoom, min(new_src.max_zoom, z))
        self.map_view.zoom = z

        self.map_view.remove_all_tiles()
        self.map_view.trigger_update(full=True)
        print("change_map_source")



    def update_is_okey_to_click(self, *args):
        self.is_okey_to_click = True
        

    def on_map_move(self, *args):
        """ Called when user pans the map. """
        if self.map_view:
            self.lat_data = self.map_view.lat
            self.lon_data = self.map_view.lon  
            lat = f"{round(self.lat_data, 25)}.." if len(str(self.lat_data)) > 25 else self.lat_data
            lon = f"{round(self.lon_data, 25)}.." if len(str(self.lon_data)) > 25 else self.lon_data 
            print(f"📍 Map center updated → Lat: {lat}, Lon: {lon}")


    def get_center_coords(self):
        """ Call this when you want to access the map center directly. """
        if self.map_view:
            return self.map_view.lat, self.map_view.lon
        return None, None

    def go_to_location(self , new_lat , new_lon): 
        self.lat_data = new_lat
        self.lon_data = new_lon
        try:
            if self.map_view:
                self.map_view.center_on(new_lat, new_lon)
                self.map_view.zoom = 16  # Optional: adjust zoom for better clarity
                self.map_view.min_zoom = 1
                self.map_view.max_zoom = 17
            else:
                Clock.schedule_once(self.load_map, 0.3)
                Clock.schedule_once( lambda *args: self.go_to_location(new_lat, new_lon), 0.3)
        except Exception as e:
            # print(f"Error: {e}")
            pass



















