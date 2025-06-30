
from kivy.properties import ObjectProperty, NumericProperty, StringProperty , ListProperty, BooleanProperty, DictProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.behaviors import BackgroundColorBehavior, CommonElevationBehavior
from kivymd.uix.widget import MDWidget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.uix.scrollview import ScrollView
from kivy.animation import Animation
from kivy.clock import Clock
import os


from screen_components import section_icon
from kivy.utils import get_color_from_hex

from kivy.uix.behaviors import ButtonBehavior

from kivymd.uix.behaviors import CommonElevationBehavior, RectangularRippleBehavior

from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivymd.app import MDApp 
from variables  import *

from kivy.core.window import Window




class PlansAddsOnsWidget(
    CommonElevationBehavior,
    RectangularRippleBehavior,
    ButtonBehavior,
    MDBoxLayout
):
    content_background_radius = ListProperty([ 8 , 8, 8 , 8 ])
    widget_type = StringProperty("addons") 

    widget_height_5 = NumericProperty(8)
    widget_height_7 = NumericProperty(8)
    widget_height_8 = NumericProperty(8)
    widget_height_15 = NumericProperty(8)

    plan_name = StringProperty("None")
    monthly = StringProperty("[font=p_bold]Monthly:[/font] P 0")
    plan_id = StringProperty("")


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = get_color_from_hex("#FAF0E6")
        self.opacity = 0
        self.elevation = 0

    def on_parent(self, instance, value):
        # Widget is now attached to the tree
        if value:
            # Animate appearance
            Animation(opacity=1, elevation=4, d=0.3).start(self)

    def update_sizing(self, *args):
        width, height = Window.size

        self.content_background_radius = [self.widget_height_5, self.widget_height_5, self.widget_height_5, self.widget_height_5]

        self.widget_height_5 = int(min( width, height) * 0.017)
        self.widget_height_7 = int(min( width, height) * 0.022)
        self.widget_height_8 = int(min( width, height) * 0.025)
        self.widget_height_15 = int(min( width, height) * 0.04)
        
        self.padding = [self.widget_height_15, self.widget_height_5]

class PlansInstallmentWidget(
    CommonElevationBehavior,
    RectangularRippleBehavior,
    ButtonBehavior,
    MDBoxLayout
):
    content_background_radius = ListProperty([ 8 , 8, 8 , 8 ])
    widget_type = StringProperty("addons") 
    total = StringProperty("[font=p_bold]Total Amount:[/font] P 0")
    remaining  = StringProperty("[font=p_bold]Months Remaining[/font] None")
    month2pay  = StringProperty("[font=p_bold]Months To Pay:[/font] None")
    monthly  = StringProperty("[font=p_bold]Monthly:[/font] P 0") 
    planname  = StringProperty("None")
    
    widget_height_5 = NumericProperty(8)
    widget_height_7 = NumericProperty(8)
    widget_height_8 = NumericProperty(8)
    widget_height_15 = NumericProperty(8)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = get_color_from_hex("#FAF0E6")
        self.opacity = 0
        self.elevation = 0

    def on_parent(self, instance, value):
        # Widget is now attached to the tree
        if value:
            # Animate appearance
            Animation(opacity=1, elevation=4, d=0.3).start(self)
    
    def update_sizing(self, *args):
        width, height = Window.size

        self.content_background_radius = [self.widget_height_5, self.widget_height_5, self.widget_height_5, self.widget_height_5]
        
        self.widget_height_5 = int(min( width, height) * 0.017)
        self.widget_height_7 = int(min( width, height) * 0.022)
        self.widget_height_8 = int(min( width, height) * 0.025)
        self.widget_height_15 = int(min( width, height) * 0.04)

        self.padding = [self.widget_height_15, self.widget_height_5]

class AdditionalPlanList(ScrollView):
    
    plan_list_container : MDBoxLayout = ObjectProperty(None)
    widget_height_5 = NumericProperty(8)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def clear_list_content(self, *args):
        if self.plan_list_container is not None:
            self.plan_list_container.clear_widgets()
        else:
            print("Plan list container is None")

    def update_sizing(self, *args):
        width, height = Window.size
        self.widget_height_5 = int(min( width, height) * 0.017)
        
        for widget in self.plan_list_container.children:
            widget.update_sizing()
     
    
    def display_plan_list(self, plan_widget = None):
        if plan_widget is not None and self.plan_list_container is not None:
             self.plan_list_container.add_widget(plan_widget)
         

class PlanClickableImage(ButtonBehavior, Image):
    pass


class PlanWidget(
    CommonElevationBehavior,
    RectangularRippleBehavior,
    ButtonBehavior,
    MDRelativeLayout
):
    content_background_radius = ListProperty([ 8 , 8, 8 , 8 ])
    plan_icon = StringProperty("")
    view_icon : PlanClickableImage = ObjectProperty(None)
    is_viewing = BooleanProperty(False)
    widget_type = StringProperty("plan")
    
    is_okey_to_cliked = BooleanProperty(True)
    is_selected = BooleanProperty(True) # it will revert into false

    widget_height_8 = NumericProperty(8)
    widget_height_10 = NumericProperty(0) 
    widget_height_13 = NumericProperty(0) 

    click_event_open = ObjectProperty(None)
    click_event_close = ObjectProperty(None)
    status = StringProperty("    None")
    planname = StringProperty("None")
    monthly = StringProperty("    [font=p_regular]Monthly:[/font] P 0")
    plan_id = StringProperty("")



    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_x = None
        self.md_bg_color = get_color_from_hex("#FAF0E6")
        
        Clock.schedule_once(self.update_image, 0.1)
        self.opacity = 0
        self.elevation = 0

        self.bind(on_release=self.update_image)

    

    def on_parent(self, instance, value):
        # Widget is now attached to the tree
        if value:
            # Animate appearance
            Animation(opacity=1, elevation=4, d=0.3).start(self)
            self.update_sizing()
    
    def update_image(self, *args):
        if not self.is_okey_to_cliked:
            return
        self.is_okey_to_cliked = False
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        self.is_selected = not self.is_selected
        if self.is_selected:
            self.view_icon.source = os.path.join(parent_dir, 'assets', 'plan_selected.png')
            if self.click_event_open is not None:
                self.click_event_open(self)
        else:
            self.view_icon.source = os.path.join(parent_dir, 'assets', 'plan_not_selected.png')
            if self.click_event_close is not None:
                self.click_event_close()
        def update(*args):
            self.is_okey_to_cliked = True
        Clock.schedule_once(update, 1)
        
        # for key, widget in self.ids.items():
        #     print(f"id: {key}, widget: {widget}")

    def open_image_plan(self, *args):
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        self.view_icon.source = os.path.join(parent_dir, 'assets', 'plan_selected.png')
        self.is_selected = True

    def close_image_plan(self, *args):
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        self.view_icon.source = os.path.join(parent_dir, 'assets', 'plan_not_selected.png')
        self.is_selected = False

    def update_sizing(self, *args):
        width, height = self.size 
        r = min(width, height) * 0.045
        self.content_background_radius = [r, r, r, r]

        self.width = int(self.height * 1.8)
    
        width, height = Window.size
        self.widget_height_8 = int(min( width, height) * 0.025)
        self.widget_height_10 = int(min( width, height) * 0.03) 
        self.widget_height_13 = int(min( width, height) * 0.04)


    def setup_ui(self, plan_name, plan_status, plan_monthly ):
        self.planname = str(plan_name) if plan_name is not None else "None"
        self.status = f"    {str(plan_status).title()}" if plan_status is not None else "    None"
        self.monthly = f"    [font=p_regular]Monthly:[/font] P{float(plan_monthly):,.2f}" if isinstance(plan_monthly, (int, float)) else f"    [font=p_regular]Monthly:[/font] P 0"
        

class AddPlanWidget(
    CommonElevationBehavior,
    RectangularRippleBehavior,
    ButtonBehavior,
    MDBoxLayout
):
    content_background_radius = ListProperty([ 8 , 8, 8 , 8 ])
    add_plan_icon = StringProperty("")
    widget_type = StringProperty("add_plan")
    
    widget_height_8 = NumericProperty(8) 
    widget_height_30 = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = get_color_from_hex("#FAF0E6") 

        Clock.schedule_once(self.update_sizing, 0.1)
        self.opacity = 0
        self.elevation = 0

    
    def on_parent(self, instance, parent):
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        self.add_plan_icon = os.path.join(parent_dir, 'assets', 'add_plan.png')
        
        # Widget is now attached to the tree
        if parent:
            # Animate appearance
            Animation(opacity=1, elevation=4, d=0.3).start(self)
            self.update_sizing()
            

    def update_sizing(self, *args):
        width, height = self.size 
        r = min(width, height) * 0.045
        self.content_background_radius = [r, r, r, r]
        self.width = int(self.height * 1.8)


        width, height = Window.size
        self.widget_height_8 = int(min( width, height) * 0.025) 
        self.widget_height_30 = int(min( width, height) * 0.1)

    def on_release(self):
        main_app  = MDApp.get_running_app()
        main_app.is_outside = False
        Clock.schedule_once(main_app.show_welcome_popup) 
        main_app.root_screen_manager.change_screen(ADD_PLAN_SCREEN)
        return super().on_release()


class EmptyPlanWidget(
    CommonElevationBehavior,
    RectangularRippleBehavior,
    ButtonBehavior,
    MDBoxLayout
):
    content_background_radius = ListProperty([8, 8, 8, 8])
    widget_type = StringProperty("empty_plan")

    widget_height_8 = NumericProperty(8) 

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = get_color_from_hex("#FAF0E6") 
        Clock.schedule_once(self.update_sizing, 0.1)
        self.opacity = 0
        self.elevation = 0

    def on_parent(self, instance, parent): 
        # Widget is now attached to the tree
        if parent:
            # Animate appearance
            Animation(opacity=1, elevation=4, d=0.3).start(self)
            self.update_sizing()

    def update_sizing(self, *args):
        width, height = self.size
        r = min(width, height) * 0.045
        self.content_background_radius = [r, r, r, r]
        self.width = int(self.height * 1.8)

        width, height = Window.size
        self.widget_height_8 = int(min( width, height) * 0.025) 
    
    def on_release(self):
        main_app  = MDApp.get_running_app()
        main_app.is_outside = False
        Clock.schedule_once(main_app.show_welcome_popup) 
        main_app.root_screen_manager.change_screen(ADD_PLAN_SCREEN)
        return super().on_release()




class ListOfPlans(ScrollView):
    container_layout : BoxLayout = ObjectProperty(None)
    plan_click_event_open = ObjectProperty(None)
    plan_click_event_close = ObjectProperty(None)

    def update_sizing(self, width , height):
        if self.container_layout is not None:
            self.container_layout.spacing = int(height * 0.02)
            vpad = int(height * 0.01)
            hpad = int(width * 0.01)
            self.container_layout.padding = [hpad , vpad , hpad * 10 , vpad]
        
            for widget in self.container_layout.children:
                print(f"widget: {widget} , widget.size: {widget.size}")
                widget.update_sizing()
    
    def test_adding_widget(self , *args):
        plan = PlanWidget()
        plan.update_sizing()
        plan.click_event_open = self.plan_click_event_open
        plan.click_event_close = self.plan_click_event_close

        self.container_layout.add_widget(plan)
        plan = PlanWidget()
        plan.update_sizing()
        plan.click_event_open = self.plan_click_event_open
        plan.click_event_close = self.plan_click_event_close
        self.container_layout.add_widget(plan)

        plan = PlanWidget()
        plan.update_sizing()
        plan.click_event_open = self.plan_click_event_open
        plan.click_event_close = self.plan_click_event_close
        self.container_layout.add_widget(plan)

        empty_plan = EmptyPlanWidget()
        empty_plan.update_sizing()
        self.container_layout.add_widget(empty_plan)
        add_plan = AddPlanWidget()
        add_plan.update_sizing()
        self.container_layout.add_widget(add_plan)

        width, height = Window.size
        self.update_sizing(width , height)
    

    def display_plans(self , plans_list : dict):
        
        self.container_layout.clear_widgets()

        for pkey, plan in plans_list.items():
            plan_widget = PlanWidget()
            plan_widget.click_event_open = self.plan_click_event_open
            plan_widget.click_event_close = self.plan_click_event_close
            self.container_layout.add_widget(plan_widget)
            plan_widget.update_sizing()
            plan_name = plan.get("planname", None)
            plan_status = plan.get("status", None)
            plan_monthly = plan.get("monthly", None)
            plan_widget.plan_id = str(plan.get("id", ""))
            plan_widget.setup_ui(plan_name, plan_status, plan_monthly)
        
  
        add_plan = AddPlanWidget()
        add_plan.update_sizing()
        self.container_layout.add_widget(add_plan)

    def close_all_plans(self):
        for widget in self.container_layout.children:
            if widget.widget_type == "plan":
                widget.close_image_plan()
        # self.plan_click_event_close()


class AdditionalPlansList(MDBoxLayout):

    selected_additional_plan_list : AdditionalPlanList = ObjectProperty(None)
    selected_installment_plan_list : AdditionalPlanList = ObjectProperty(None)
 
     
    widget_height_6 = NumericProperty(0) 
    widget_height_8 = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    
    def update_container(self , additional_plan_list = None , installment_plan_list = None):
        if self.selected_additional_plan_list is not None:
            self.selected_additional_plan_list.clear_list_content()
            print("Display the additional plans : ", additional_plan_list)
            for pkey , plan in additional_plan_list.items():
                plan_widget = PlansAddsOnsWidget()
                plan_widget.plan_name = plan.get("name", "None")
                plan_widget.plan_id = str(plan.get("id", "None"))
                plan_widget.monthly = f"[font=p_bold]Monthly:[/font] P {float(plan.get("monthly", 0)):,.2f}" 
                self.selected_additional_plan_list.display_plan_list(plan_widget)
                plan_widget.update_sizing()
        
        if self.selected_installment_plan_list is not None:
            self.selected_installment_plan_list.clear_list_content()
            print("Display the installment plans : ", installment_plan_list)
            for pkey , plan in installment_plan_list.items():
                plan_widget = PlansInstallmentWidget() 
                plan_widget.planname = plan.get("name", "None")
                plan_widget.monthly = f"[font=p_bold]Monthly:[/font] P {float(plan.get("monthly", 0)):,.2f}"
                plan_widget.remaining = f"[font=p_bold]Months Remaining:[/font] {plan.get('month_remaining', 0)}"
                plan_widget.month2pay = f"[font=p_bold]Months To Pay:[/font] {plan.get('month_to_pay', 0)}"
                plan_widget.total = f"[font=p_bold]Total Amount:[/font] P {float(plan.get('total_amount', 0)):,.2f}"
                self.selected_installment_plan_list.display_plan_list(plan_widget)
                plan_widget.update_sizing()
        
    
    def update_sizing(self, *args):
        width , height = Window.size 
        self.widget_height_6 = int(min( width, height) * 0.022)
        self.widget_height_8 = int(min( width, height) * 0.032)

        if self.selected_additional_plan_list is not None:
            self.selected_additional_plan_list.update_sizing()
        if self.selected_installment_plan_list is not None:
            self.selected_installment_plan_list.update_sizing()



 

class RouterLayout(MDBoxLayout):
    content_background_radius = ListProperty([ 8 , 8, 8 , 8 ])

    router_icon : section_icon.SectionIconLayout = ObjectProperty(None)
    selected_plan_layout : MDBoxLayout = ObjectProperty(None)
    additional_plans_list : AdditionalPlansList = ObjectProperty(None)
    plan_list : ListOfPlans = ObjectProperty(None)

    
    widget_height_5 = NumericProperty(0)
    widget_height_6 = NumericProperty(0)
    widget_height_8 = NumericProperty(0)
    widget_height_10 = NumericProperty(0) 
    widget_height_15 = NumericProperty(0) 
    widget_height_80 = NumericProperty(0)
    widget_height_180 = NumericProperty(0)

    plans_data = DictProperty({})
    selected_plan_data = DictProperty({})
    
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs) 

        # Clock.schedule_once(self.setup_image, 1)
        # Clock.schedule_once(self.open_selected_layout, 8)
      

    def setup_image(self, *args):
        if self.router_icon is None:
            Clock.schedule_once(self.setup_image, 0.3)
            return
        width , height = Window.size
        self.router_icon.update_sizing(width, height)
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        self.router_icon.sec_icon = os.path.join(parent_dir, 'assets', 'router_icon.png')
        self.router_icon.display_additional = False
        self.router_icon.is_half_padding_left = True


        self.plan_list.plan_click_event_open = self.open_selected_layout
        self.plan_list.plan_click_event_close = self.close_selected_layout
        # self.plan_list.test_adding_widget()

    def update_sizing(self, width = None, height = None):
        if width is not None and height is not None: 
            self.spacing = max(4, int(width * 0.03))  # 3% of width, with min fallback
            r = min(width, height) * 0.035  # You can change 0.05 to any fraction
            self.content_background_radius = [r, r, r, r]
        width , height = Window.size
        if self.router_icon is not None:
            self.router_icon.update_sizing(width, height)

        if self.plan_list is not None:
            width , height = Window.size
            self.plan_list.update_sizing(width, height)
        
        if self.additional_plans_list is not None:
            self.additional_plans_list.update_sizing()

         
        self.widget_height_5 = int(min( width, height) * 0.02)
        self.widget_height_6 = int(min( width, height) * 0.025)
        self.widget_height_8 = int(min( width, height) * 0.035)
        self.widget_height_10 = int(min( width, height) * 0.04) 
        self.widget_height_15 = int(min( width, height) * 0.055) 
        self.widget_height_80 = int(min( width, height) * 0.28)
        self.widget_height_180 = int(min( width, height) * 0.8)



    def open_selected_layout(self, selected_widget = None):
        anime = Animation(height=self.widget_height_180,  duration=0.3)
        # anime.bind(on_complete=self.on_selected_animation_complete)
        if selected_widget is not None and self.plan_list is not None:
            self.plan_list.close_all_plans()
            plan_id = selected_widget.plan_id
            selected_widget.open_image_plan()

            self.selected_plan_data = self.plans_data.get(plan_id, {})
            print("Selected Plan Data : ", self.selected_plan_data)

            anime.bind(on_complete=self.on_selected_animation_complete)

        anime.start(self.selected_plan_layout)

    
    def on_selected_animation_complete(self, *args):
        if len(self.selected_plan_layout.children) < 1:
            self.additional_plans_list = AdditionalPlansList()
            self.additional_plans_list.update_sizing()

            print("Setting up  selected layout using : ", self.selected_plan_data)
            # print()
            # print() 
            self.selected_plan_layout.add_widget(self.additional_plans_list)
            
        else:
            # Just update the content of the selected layout
            # print("Updating content of selected layout using : ", self.selected_plan_data)
            print()
            print()
            
        addons = self.selected_plan_data.get('addons', {})
        installments = self.selected_plan_data.get('installments', {})
        self.additional_plans_list.update_container(
            additional_plan_list = addons , 
            installment_plan_list = installments
        )
        self.update_sizing()

            
    
    def close_selected_layout(self, *args):
        anime = Animation(height=0,  duration=0.3)
        anime.bind(on_start=self.on_unselected_animation_complete)
        anime.start(self.selected_plan_layout)
    
    def on_unselected_animation_complete(self, *args): 
        self.selected_plan_layout.clear_widgets()
        self.selected_plan_data = {}
        print("Is this actully happen?")



    def setup_ui(self, data : dict):
        if self.plan_list is None:
            print("Plan list is not set")
            return
        
        for pkey, pdata in data.items(): 
            self.plans_data[str(pdata.get("id", ""))] = pdata
            print("Adding plan : ", pkey)
        self.plan_list.display_plans(data)










































# kv_router_layout = '''
# <RouterLayout>:
#     orientation: "vertical"
#     size_hint: 1, None
#     adaptive_height: True

#     router_icon : router_icon
#     selected_plan_layout : selected_plan_layout

#     canvas.before:
#         Color:
#             rgba: chex("#5C5470")
#         RoundedRectangle:
#             pos: self.pos
#             size: self.size
#             radius: root.content_background_radius
    
#     Widget:
#         size_hint: 1, None
#         height: 5

#     SectionIconLayout:
#         id: router_icon
#         size_hint: 1, None 
    
#     BoxLayout:
#         size_hint: 1, None
#         height: 15
#         orientation: "horizontal"

#         Widget:
#             size_hint: 0.05, 1

#         Label:
#             size_hint: 0.95, 1
#             font_size: 10
#             color: chex("#FFFFFF")
#             text: "All Plans Subscribed"
#             font_name: "p_bold"
#             text_size: self.size
#             halign: "left"
#             valign: "center"

#     BoxLayout:
#         size_hint: 1, None
#         height: 80

#         Widget:
#             size_hint: 0.05, 1

#         ListOfPlans:
#             size_hint: 0.95, 1
    
#     Widget:
#         size_hint: 1, None
#         height: 10

    
#     MDBoxLayout:
#         id: selected_plan_layout
#         size_hint: 1, None
#         height: 0


#         # AdditionalPlansList:






# <AdditionalPlansList>:
#     size_hint: 1, None
#     orientation: "vertical"
#     height: 180
    
#     Widget:
#         size_hint: 1, 0.05

#     BoxLayout:
#         size_hint: 1, 0.10
#         orientation: "horizontal"
#         Widget:
#             size_hint: 0.05, 1
#         Label:
#             size_hint: 0.95, 1
#             font_name: "p_light"
#             font_size: 8
#             color: chex("#FFFFFF")
#             text: "[font=p_bold]Selected Plan :[/font]   Home Plan"
#             halign: "left"
#             valign : "center"
#             text_size: self.size
#             markup: True
    
#     Widget:
#         size_hint: 1, 0.05

#     BoxLayout:
#         size_hint: 1, 0.7

#         Widget:
#             size_hint: 0.05, 1

#         BoxLayout:
#             size_hint: 0.44, 1
#             orientation: "vertical"
            
#             Label:
#                 size_hint: 1, 0.1
#                 font_name: "p_bold"
#                 font_size: 6
#                 color: chex("#FFFFFF")
#                 text: "Available Add-ons Plan"
#                 halign: "left"
#                 valign : "center"
#                 text_size: self.size
#                 markup: True
            
#             Widget:
#                 size_hint: 1, 0.05

#             AdditionalPlanList:
#                 size_hint: 1, 0.85


#         Widget:
#             size_hint: 0.02, 1

#         BoxLayout:
#             size_hint: 0.44, 1
#             orientation: "vertical"

#             Label:
#                 size_hint: 1, 0.1
#                 font_name: "p_bold"
#                 font_size: 6
#                 color: chex("#FFFFFF")
#                 text: "Available Add-ons Plan"
#                 halign: "left"
#                 valign : "center"
#                 text_size: self.size
#                 markup: True
            
#             Widget:
#                 size_hint: 1, 0.05

#             AdditionalPlanList:
#                 size_hint: 1, 0.85


#         Widget:
#             size_hint: 0.05, 1

#     Widget:
#         size_hint: 1, 0.1


# <AdditionalPlanList>:
#     do_scroll_x: False
#     do_scroll_y: True
#     bar_width: 0  # Optional: hide bar

#     plan_list_container: plan_list_container

#     MDBoxLayout:
#         id: plan_list_container
#         orientation: "vertical"
#         size_hint: (1, None)
#         adaptive_height: True
#         spacing: 5

#         PlansInstallmentWidget:
#         PlansAddsOnsWidget:
        

# <PlansAddsOnsWidget>:
#     size_hint: 1, None
#     adaptive_height: True
#     orientation: "vertical"
#     opacity: 0
    
#     theme_elevation_level: "Custom"
#     elevation_level: 2
#     theme_shadow_offset: "Custom"
#     shadow_offset: 0, -3
#     theme_shadow_softness: "Custom"
#     shadow_softness: 12
#     shadow_radius: root.content_background_radius
#     radius: root.content_background_radius
#     padding: 15, 5

#     Widget:
#         size_hint: 1, None
#         height: 7
#     Label:
#         size_hint_y: None
#         text_size: self.width, None  # Enables wrapping
#         height: self.texture_size[1]  # Auto height based on wrapped content
#         font_name: "p_light"
#         font_size: 8
#         color: chex("#352F44")
#         text: "Home Plan Add Ons"
#         halign: "left"
#         valign: "middle"
#         markup: True

#     Widget:
#         size_hint: 1, None
#         height: 5

#     Label:
#         size_hint_y: None
#         text_size: self.width, None  # Enables wrapping
#         height: self.texture_size[1]  # Auto height based on wrapped content
#         font_name: "p_light"
#         font_size: 8
#         color: chex("#352F44")
#         text: "[font=p_bold]Monthly:[/font] P 1,500"
#         halign: "left"
#         valign: "middle"
#         markup: True

#     Widget:
#         size_hint: 1, None
#         height: 7


# <PlansInstallmentWidget>:
#     size_hint: 1, None
#     adaptive_height: True
#     orientation: "vertical"
    
#     theme_elevation_level: "Custom"
#     elevation_level: 2
#     theme_shadow_offset: "Custom"
#     shadow_offset: 0, -3
#     theme_shadow_softness: "Custom"
#     shadow_softness: 12
#     shadow_radius: root.content_background_radius
#     radius: root.content_background_radius
#     padding: 15, 5

#     Widget:
#         size_hint: 1, None
#         height: 7
#     Label:
#         size_hint_y: None
#         text_size: self.width, None  # Enables wrapping
#         height: self.texture_size[1]  # Auto height based on wrapped content
#         font_name: "p_light"
#         font_size: 8
#         color: chex("#352F44")
#         text: "Home Plan Add Ons"
#         halign: "left"
#         valign: "middle"
#         markup: True

#     Widget:
#         size_hint: 1, None
#         height: 5

#     Label:
#         size_hint_y: None
#         text_size: self.width, None  # Enables wrapping
#         height: self.texture_size[1]  # Auto height based on wrapped content
#         font_name: "p_light"
#         font_size: 8
#         color: chex("#352F44")
#         text: "[font=p_bold]Monthly:[/font] P 1,500"
#         halign: "left"
#         valign: "middle"
#         markup: True

#     Widget:
#         size_hint: 1, None
#         height: 5

#     Label:
#         size_hint_y: None
#         text_size: self.width, None  # Enables wrapping
#         height: self.texture_size[1]  # Auto height based on wrapped content
#         font_name: "p_light"
#         font_size: 8
#         color: chex("#352F44")
#         text: "[font=p_bold]Months To Pay:[/font] 11"
#         halign: "left"
#         valign: "middle"
#         markup: True

#     Widget:
#         size_hint: 1, None
#         height: 5

#     Label:
#         size_hint_y: None
#         text_size: self.width, None  # Enables wrapping
#         height: self.texture_size[1]  # Auto height based on wrapped content
#         font_name: "p_light"
#         font_size: 8
#         color: chex("#352F44")
#         text: "[font=p_bold]Months Remaining[/font] 11"
#         halign: "left"
#         valign: "middle"
#         markup: True

#     Widget:
#         size_hint: 1, None
#         height: 5

#     Label:
#         size_hint_y: None
#         text_size: self.width, None  # Enables wrapping
#         height: self.texture_size[1]  # Auto height based on wrapped content
#         font_name: "p_light"
#         font_size: 8
#         color: chex("#352F44")
#         text: "[font=p_bold]Total Amount:[/font] P 1,500"
#         halign: "left"
#         valign: "middle"
#         markup: True

#     Widget:
#         size_hint: 1, None
#         height: 7


    

# <PlanWidget>:
#     size_hint: None, 1
#     width: 120

#     theme_elevation_level: "Custom"
#     elevation_level: 2
#     theme_shadow_offset: "Custom"
#     shadow_offset: 0, -3
#     theme_shadow_softness: "Custom"
#     shadow_softness: 12
#     shadow_radius: root.content_background_radius
#     radius: root.content_background_radius
 
#     view_icon : view_icon

#     BoxLayout:
#         size_hint: 1, 1
#         pos_hint: {"center_x": 0.5,"center_y": 0.5}
#         orientation: "vertical"

#         Label:
#             size_hint: 1, 0.2
#             font_name: "p_light"
#             font_size: 7
#             color: chex("#352F44")
#             text: "    Registering"
#             halign: "left"
#             valign: "middle" 
#             text_size: self.size
        
#         Widget:
#             size_hint: 1, 0.15
        
#         Label:
#             size_hint: 1, 0.3
#             font_name: "p_bold"
#             font_size: 10
#             color: chex("#352F44")
#             text: "Home Plan"

#         Widget:
#             size_hint: 1, 0.15

            
#         BoxLayout:
#             size_hint: 1, 0.2
#             orientation: "horizontal"

#             Label:
#                 size_hint: 1, 1
#                 font_name: "p_light"
#                 font_size: 7
#                 color: chex("#352F44")
#                 text: "    [font=p_regular]Monthly:[/font] P 1,500"
#                 halign: "left"
#                 valign: "middle" 
#                 text_size: self.size
#                 markup: True
        
#     PlanClickableImage:
#         id: view_icon
#         size_hint: None, None
#         height: 13
#         width: 13
#         pos_hint: {"right": 0.95,"y": 0.05}
#         opacity: 1 if not root.is_viewing else 0.7

#         on_release: root.is_viewing = True



    


# <AddPlanWidget>:
#     orientation: "vertical"
#     size_hint: None, 1
#     width: 120
#     theme_elevation_level: "Custom"
#     elevation_level: 2
#     theme_shadow_offset: "Custom"
#     shadow_offset: 0, -3
#     theme_shadow_softness: "Custom"
#     shadow_softness: 12
#     shadow_radius: root.content_background_radius
#     radius: root.content_background_radius
        


#     Widget:
#         size_hint: 1, 0.23

#     FloatLayout:
#         size_hint: 1, 0.3

#         Image:
#             pos_hint: {"center_x": 0.5,"center_y": 0.5}
#             source: root.add_plan_icon
#             allow_stretch: True
#             keep_ration: True
#             size_hint: None, 1
#             width: 30
        
#     Widget:
#         size_hint: 1, 0.05

#     Label:
#         size_hint: 1, 0.1
#         font_name: "p_extralight"
#         font_size: 8
#         color: chex("#352F44")
#         text: "Add New Plan"

#     Widget:
#         size_hint: 1, 0.22




        

# <EmptyPlanWidget>:
#     orientation: "vertical"
#     size_hint: None, 1
#     width: 120

#     theme_elevation_level: "Custom"
#     elevation_level: 2
#     theme_shadow_offset: "Custom"
#     shadow_offset: 0, -3
#     theme_shadow_softness: "Custom"
#     shadow_softness: 12
#     shadow_radius: root.content_background_radius
#     radius: root.content_background_radius
 

#     Widget:
#         size_hint: 1, 0.4

#     Label:
#         size_hint: 1, 0.1
#         font_name: "p_bold"
#         font_size: 8
#         color: chex("#352F44")
#         text: "No plan yet?"

#     Widget:
#         size_hint: 1, 0.05

#     Label:
#         size_hint: 1, 0.1
#         font_name: "p_extralight"
#         font_size: 8
#         color: chex("#352F44")
#         text: "[u]Apply now[/u]"
#         markup: True

#     Widget:
#         size_hint: 1, 0.35

    




# <ListOfPlans>:
#     do_scroll_x: True
#     do_scroll_y: False
#     bar_width: 0  # Optional: hide bar

#     container_layout : container_layout

#     BoxLayout:
#         id: container_layout
#         orientation: "horizontal"
#         size_hint: (None, 1)
#         width: self.minimum_width
#         spacing: 20  # space between cards
#         padding: 10, 5

#         PlanWidget:

#         EmptyPlanWidget:

#         AddPlanWidget:
        













# '''