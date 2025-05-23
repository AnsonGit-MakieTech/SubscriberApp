from kivy.uix.accordion import ObjectProperty, BooleanProperty
from kivy.uix.modalview import ModalView

from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
import os

from kivy.properties import ObjectProperty, NumericProperty, StringProperty

from kivy.graphics import PushMatrix, PopMatrix, Rotate, Translate



class CustomSpinner(Image):
    # process_image: str = StringProperty('')
    angle: float = NumericProperty(0)  # ✅ Required for animation
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.anim = None

        # parent_dir = os.path.dirname(os.path.dirname(__file__)) 
        # self.process_image = os.path.join(parent_dir, 'assets', 'loading_image.png')

        # Use canvas instructions to apply rotation
        self.bind(pos=self.update_canvas, size=self.update_canvas, angle=self.update_canvas)

    def start_spinner(self, *args):
        # self.source = self.process_image
        self.size_hint_x = 0.5
        self.size_hint_y = 0.5
        self.anim = Animation(angle=360, duration=1)
        self.anim += Animation(angle=0, duration=0)
        self.anim.repeat = True
        self.anim.start(self)
        

    def stop_success_spinner(self, *args):
        if self.anim:
            self.anim.cancel(self)

            # Animate shrink first
            anim = Animation(size_hint_x=0.0, size_hint_y=0.0, duration=0.5)
            anim.bind(on_complete=self.display_done)
            anim.start(self)
            

    def display_done(self, *args):
        # Update the image to success icon
        parent_dir = os.path.dirname(os.path.dirname(__file__)) 
        self.source = os.path.join(parent_dir, 'assets', 'success_icon.png')
        self.angle = 0 
        # Animate grow and fade out sequentially
        anim = (
            Animation(size_hint_x=0.5, size_hint_y=0.5, duration=0.5, t='out_back') 
        )
        anim.start(self)
    
    def stop_error_spinner(self, *args):
        if self.anim:
            self.anim.cancel(self)
            # Animate shrink first
            anim = Animation(size_hint_x=0.0, size_hint_y=0.0, duration=0.5)
            anim.bind(on_complete=self.display_error)
            anim.start(self)
            
    def display_error(self, *args):
        # Update the image to error icon
        parent_dir = os.path.dirname(os.path.dirname(__file__)) 
        self.source = os.path.join(parent_dir, 'assets', 'error_icon.png')
        self.angle = 0
        # Animate grow and fade out sequentially
        anim = (
            Animation(size_hint_x=0.5, size_hint_y=0.5, duration=0.5  ) 
        )
        anim.start(self)

    def update_canvas(self, *args):
        
        self.canvas.before.clear()
        with self.canvas.before:
            PushMatrix()
            Translate(self.center_x, self.center_y)
            Rotate(angle=self.angle, origin=(0, 0))
            Translate(-self.center_x, -self.center_y)
        self.canvas.after.clear()
        with self.canvas.after:
            PopMatrix()


class ProcessingLayout(ModalView):
    
    spinner : CustomSpinner = ObjectProperty(None)
    proccess_text : str = StringProperty('')
    is_open : bool = BooleanProperty(False)
    setup_font_size = NumericProperty(14)
    main_layout : BoxLayout = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_font_size = 14
        
        Clock.schedule_once(self.update_sizing, 0.1)
        # self.bind(size=self.update_sizing)
    
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
        self.setup_font_size = min(width, height) * 0.035
        
        padding_x = int(width * 0.08)
        padding_y = int(height * 0.05)
    
        # Set padding as (left, top, right, bottom)
        self.main_layout.padding = [padding_x, padding_y, padding_x, padding_y]
        self.main_layout.spacing = int(height * 0.005)
        
    
    def on_pre_open(self):
        self.auto_dismiss = False
        parent_dir = os.path.dirname(os.path.dirname(__file__)) 
        self.spinner.source = os.path.join(parent_dir, 'assets', 'loading_icon.png')
        return super().on_pre_open()
    def on_open(self):
        self.auto_dismiss = False
        self.spinner.start_spinner()
        self.proccess_text = "Please wait while we complete the process. Do not close the application until it is finished."
        self.is_open = True
        
        # Clock.schedule_once(self.display_success , 2)
        
        return super().on_open()

    def display_success(self, message = None):
        self.spinner.stop_success_spinner()
        self.proccess_text = "Process completed successfully!" if not message else message
        Clock.schedule_once(self.dismiss, 2) 
        self.is_open = False
    
    def display_error(self, message = None):
        self.spinner.stop_error_spinner()
        self.proccess_text = "An error occurred while processing the data." if not message else message
        self.auto_dismiss = True
        self.is_open = False
    

        
kv_process_modal = '''
<ProcessingLayout>: 
    size_hint: 1, 1
    auto_dismiss: False
    background: ""  # Removes default dim background
    background_color: 0, 0, 0, 0
    spinner : spinner
    main_layout : main_layout

    BoxLayout:
        id: main_layout
        orientation:"vertical"
        padding: 20
        spacing: 10
        size_hint: 0.85 , 0.3
        pos_hint: { "center_x": 0.5 , "center_y": 0.5 }  


        canvas.before:
            Color:
                rgba: chex("#F7EEDD")
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [10]
            Color:
                rgba: chex("#352F44")
            Line:
                width: 2
                rounded_rectangle: (*self.pos, *self.size, 10)


        RelativeLayout:
            size_hint: 1 , 0.7
            
            CustomSpinner:
                id: spinner
                size_hint: 0.5, 0.5
                pos_hint: {"center_x": .5, "center_y": .5}
                active: True # if check.active else False


        Label:
            size_hint: 1, None
            text: root.proccess_text
            text_size: self.width, None
            height: self.texture_size[1]
            valign: "middle"  # Or "center"
            halign: "center"  # "left", "right", or "center" depending on your goal
            font_name: "p_regular"
            font_size: root.setup_font_size
            color: chex("#014367")




'''