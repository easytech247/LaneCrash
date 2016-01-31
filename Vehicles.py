'''
Created on Jan 7, 2016

@author: shaibujnr
'''
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation,AnimationTransition
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.utils import get_random_color
from kivy.properties import (StringProperty,
                             NumericProperty,
                             ObjectProperty,
                             ListProperty,
                             BooleanProperty)

from functools import partial
import time

Builder.load_string("""
<Vehicle>:
    canvas.before:
        Color:
            rgba: root.background_color
        Rectangle:
            size: root.size
            pos: root.pos

""")


class Vehicle(Button):
    set = BooleanProperty()
    speed = NumericProperty()
    #background_color = ListProperty()
    come_from = StringProperty()
    position = StringProperty()


            

            


        
        
class vehicleApp(App):
    def build(self):
        return Vehicle()
    
if __name__ == "__main__":
    vehicleApp().run()