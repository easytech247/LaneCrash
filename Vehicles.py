'''
Created on Jan 7, 2016

@author: shaibujnr
'''
from kivy.app import App
from kivy.graphics import Rotate
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation,AnimationTransition
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.lang import Builder
import random
from kivy.utils import get_random_color
from kivy.properties import (StringProperty,
                             NumericProperty,
                             ObjectProperty,
                             ListProperty,
                             BooleanProperty)

from functools import partial
import time

Builder.load_string("""
<Car>:
    canvas.before:
        PushMatrix:
        Rotate:
            angle: root.angle
            origin: root.center

        Rectangle:
            size: root.size
            pos: root.pos
            source: root.source

            
    canvas.after:
        PopMatrix:

""")


class Car(ButtonBehavior,Widget):
    angle = NumericProperty(0)
    source = StringProperty("imgs/ycar.png")
    brake_sound = StringProperty()
    moving_sound = StringProperty()
    run_sound = StringProperty()
    set = BooleanProperty()
    speed = NumericProperty()
    car_list = ListProperty(["imgs/ycar.png"])
    #background_color = ListProperty()
    come_from = StringProperty()
    position = StringProperty()
    
    def update(self,*args):
        if self.come_from=="rhl":
            pass
        elif self.come_from == "rvl":
            self.source = random.choice(self.car_list)
        elif self.come_from == "lvl":
            pass
        elif self.come_from == "lhl":
            pass


            

            


        

class vehicleApp(App):
    def build(self):
        car = Car()
        car.angle = 90
        return car
    
if __name__ == "__main__":
    vehicleApp().run()
