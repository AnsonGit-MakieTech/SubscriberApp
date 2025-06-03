
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior


class LabelClickable(ButtonBehavior, Label):
    pass

kv_label_clickable = '''
<LabelClickable>:

'''

