'''
Created on Jan 17, 2016

@author: shaibujnr
'''
from kivy.app import App
from kivy.utils import get_random_color
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from Vehicles import Vehicle
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.clock import Clock
from kivy.gesture import Gesture,GestureDatabase
from kivy.core.window import Window
from kivy.core.audio import Sound,SoundLoader

from gs import up_swipe,down_swipe,left_swipe,right_swipe
import random
from highscore import HighScore
from functools import partial
from kivy.properties import (StringProperty,
                             NumericProperty,
                             ListProperty,
                             BooleanProperty,
                             ObjectProperty)

import random
import math
from kivy.uix.behaviors import ButtonBehavior


#-------------------------------------
hsff = HighScore
gdb = GestureDatabase()
swipe_up = gdb.str_to_gesture(up_swipe)
swipe_up.name = "swipe_up"
swipe_down = gdb.str_to_gesture(down_swipe)
swipe_down.name = "swipe_down"
swipe_left = gdb.str_to_gesture(left_swipe)
swipe_left.name = "swipe_left"
swipe_right = gdb.str_to_gesture(right_swipe)
swipe_right.name = "swipe_right"
gdb.add_gesture(swipe_up)
gdb.add_gesture(swipe_down)
gdb.add_gesture(swipe_down)
gdb.add_gesture(swipe_left)
gdb.add_gesture(swipe_right)
#--------------------------------------------

class Root(ScreenManager):
    game_screen = ObjectProperty()
    hs = ObjectProperty()

class Cbutton(ButtonBehavior,Widget):#Menu Button
    src = StringProperty()
    
class TutImage(Widget):#Images in the how to play screen
    src = StringProperty()
    
        
        
class HighScoreScreen(Screen):
    mw = ObjectProperty()

    
class HighScoreWidget(Widget):#main widget in the high score screen
    '''
    the highscore text is updated from the highscore.py file
    '''
    hst = NumericProperty(HighScore)#highscore text

class MenuScreen(Screen):
    mw = ObjectProperty()
    
class MenuWidget(Widget):#main widget of the menu screen
    play_btn = ObjectProperty()
    htp_btn = ObjectProperty()
    exit_btn = ObjectProperty()
    sm = ObjectProperty()
            
    def goto_game_screen(self,*args):
        self.sm.current = "game"
    def goto_help_screen(self,*args):
        self.sm.current = "help"
    def goto_hs_screen(self,*args):
        self.sm.current = "highscore"
        
class HelpWidget(BoxLayout):#main widget of the help screen
    pass
        

    
class GameScreen(Screen):
    field = ObjectProperty()
class HelpScreen(Screen):
    pass
    

class ScoreLabel(Label):
    come_from = "Score text"
    set = None
    speed = None
    is_moving= None  
    
class CrashPop(Popup):#pop up when collision is found and game is over
    '''
    is_moving,set,speed properties are present and sent to None
    'cause the crash pop is not a vehicle and whenever the 
    parent widget(field) searches for all its children and uses
    their properties to determine the next thing to do it doesn't crash

    '''
    is_moving = None
    set = None
    speed = None
    score = NumericProperty(0)
    come_from = StringProperty("Nowhere")
    field = ObjectProperty()
    
    

class Field(Widget):
    default_speed = NumericProperty(4)#vehicle default speed
    lane_spacing = NumericProperty()#space of each vehicle from ref point
    score = NumericProperty(0)
    vehicle_width = NumericProperty()
    vehicle_height = NumericProperty()
    vls = NumericProperty(5)
    def __init__(self,*args,**kwargs):
        super(Field,self).__init__(**kwargs)
        self.crash_sound = SoundLoader.load("audio/crash.ogg")
        self.speed_sound = SoundLoader.load("audio/speed.ogg")
        self.stop_sound = SoundLoader.load("audio/stop.ogg")
        self.score_sound = SoundLoader.load("audio/score.ogg")
        self.bgm = SoundLoader.load("audio/bgm.ogg")
        self.sounds = [self.crash_sound,self.speed_sound,self.stop_sound,
                       self.score_sound,self.bgm]
        
    
        
    def start(self):
        """
        clear the field, generate the vehicle at different positions and at 
        different intervals
        """
        self.clear_widgets(self.children)
        self.score = 0
        for sound in self.sounds:
            sound.stop()
        Clock.schedule_interval(self.gen_vehicle_at_rvl,random.randrange(2,5))
        Clock.schedule_interval(self.gen_vehicle_at_lvl,random.randrange(4,6))
        Clock.schedule_interval(self.gen_vehicle_at_lhl,random.randrange(6,7))
        Clock.schedule_interval(self.gen_vehicle_at_rhl,random.randrange(8,9))
        Clock.schedule_interval(self.set_vehicles_on_motion,0.0001)
        Clock.schedule_interval(self.check_collision,0.00001)
        Clock.schedule_interval(self.set_score,0.0000001)
        self.bgm.play()
    

        
    def check_collision(self,*args):#checks if two or more vehicles collide
        for child in self.children:
            for otherchild in self.children:
                if child != otherchild and child.collide_widget(otherchild):

                    Clock.schedule_once(self.collision_found)
                    
    def collision_found(self,*largs):

        """
        unschedule the scheduled methods and add the crash pop up 
        then update the highscore screen with the latest score if 
        latest score is greater than the current highscore otherwise
        do nothing
        """
        Clock.unschedule(self.set_vehicles_on_motion)
        Clock.unschedule(self.gen_vehicle_at_lhl)
        Clock.unschedule(self.gen_vehicle_at_lvl)
        Clock.unschedule(self.gen_vehicle_at_rhl)
        Clock.unschedule(self.gen_vehicle_at_rvl)
        Clock.unschedule(self.check_collision)
        Clock.unschedule(self.set_score)
        self.crash_sound.play()
        
        self.add_widget(CrashPop(
                                 x = self.x+10,
                                 y = self.y+ 10,
                                 width = self.width-20,
                                 height = self.height-20,
                                 field = self,
                                 title = "Report",
                                 score = self.score
                                 ))
        if self.score > hsff:
            hsf = open("highscore.py","w")
            hsf.write("'''\n(caching) storing the highscore\n'''\n")
            hsf.write("HighScore = %s"%self.score)
            hsf.close()
        else:
            pass
        
    
    def set_score(self,*args):#sets the scores when vehicles successfully get off the screen
        score_sound = SoundLoader.load("audio/score.ogg")
        for child in self.children:
            if (child.come_from == "lvl" and child.top<self.y):
                self.score_sound.play()
                self.score+=50 
                child.parent.remove_widget(child)
            if (child.come_from == "rvl" and child.y>self.top):
                self.score_sound.play()
                self.score+=50
                child.parent.remove_widget(child)
            if (child.come_from == "lhl" and child.right<self.x):
                self.score_sound.play()
                self.score+=50
                child.parent.remove_widget(child)
            if (child.come_from == "rhl" and child.x>self.right):
                self.score_sound.play()
                self.score+=50
                child.parent.remove_widget(child)


            
        

    def set_vehicles_on_motion(self,*args):
        #sets the vehicles in motion 
        
        for child in self.children :
            if child.come_from == "lvl":
                child.top -= child.speed
                if child.speed==0:
                    child.is_moving = False
                else:
                    
                    child.is_moving = True
            elif child.come_from == "rvl":
                child.y += child.speed
                if child.speed==0:
                    child.is_moving = False
                else:
                    child.is_moving = True
            elif child.come_from == "lhl":
                child.right -= child.speed
                if child.speed==0:
                    child.is_moving = False
                else:
                    child.is_moving = True

            elif child.come_from ==  "rhl":
                child.x += child.speed
                if child.speed==0:
                    child.is_moving = False
                else:
                    child.is_moving = True


                
    def on_touch_down(self,touch,*args):
        """
        get the points for the gesture and also process touch position to
        determine the lane which touch is interacting with and setting the 
        vehicles on that lane.
        """
        self.gpoints = []
        self.gpoints.append(touch.pos)
        for child in self.children:
            if child.collide_point(*touch.pos) and child.is_moving:
                child.speed = 0
            elif child.collide_point(*touch.pos) and not child.is_moving:
                child.speed = self.default_speed
        for child in self.children:
            if child.come_from == self.process_touch_pos(touch):
                child.set = True
                

        super(Field,self).on_touch_down(touch)
                
    
    def on_touch_move(self,touch,*args):
        self.gpoints.append(touch.pos)#more points for the gesture
            
                
        
    def on_touch_up(self,touch,*args):
        """
        adds the final point to the list and converts it to a gesture
        then finds the gesturen in the database(gdb). If gesture is found,
        depending on the lane, the vehicles on that lane respond to the 
        gesture
        """

        self.gpoints.append(touch.pos)
        if (
            (self.gpoints[-1][0])-(self.gpoints[0][0])==0 
            and 
            (self.gpoints[-1][1])-(self.gpoints[0][1])==0
            ):
            print "normal touch"
        gesture = Gesture()
        gesture.add_stroke(point_list=self.gpoints)
        gesture.normalize()
        match = gdb.find(gesture, minscore=0.5)
        if match:
            for child in self.children:
                if child.come_from == "lvl" and child.set and match[1].name=="swipe_up":
                    child.speed = 0
                    self.stop_sound.play()
                elif child.come_from == "lvl" and child.set and match[1].name=="swipe_down":
                    child.speed = self.default_speed*3
                    self.speed_sound.play()
                    
                elif child.come_from == "rvl" and child.set and match[1].name == "swipe_up":
                    child.speed = self.default_speed*3
                    self.speed_sound.play()
                elif child.come_from == "rvl" and child.set and match[1].name=="swipe_down":
                    child.speed = 0
                    self.stop_sound.play()
                    
                elif child.come_from == "lhl" and child.set and match[1].name=="swipe_left":
                    child.speed = self.default_speed*3
                    self.speed_sound.play()
                elif child.come_from == "lhl" and child.set and match[1].name == "swipe_right":
                    child.speed = 0
                    self.stop_sound.play()
                    
                elif child.come_from == "rhl" and child.set and match[1].name == "swipe_left":
                    child.speed = 0
                    self.stop_sound.play()
                elif child.come_from == "rhl" and child.set and match[1].name == "swipe_right":
                    child.speed = self.default_speed*3
                    self.speed_sound.play()
                
    
    def on_size(self,*args):
        """
        repositioning the vehicles in the field when the size of the 
        window increases or reduces
        """
        self.vehicle_height= self.height/20
        self.vehicle_width = self.width/15
        self.lane_spacing = self.width/40
        self.lane_spacing = 20
        for child in self.children:
            if child.come_from == "lvl":
                child.top = self.top
                child.destination = -child.height
                child.width = self.vehicle_width
                child.height = self.vehicle_height
                child.right = self.center_x-(self.lane_spacing*0.5)-(self.vls*0.5)

            if child.come_from == "rvl":
                child.y = self.y
                child.destination = self.height + child.height
                child.x = self.center_x+(self.lane_spacing*0.5)+(self.vls*0.5)
                child.width = self.vehicle_width
                child.height = self.vehicle_height

            if child.come_from == "lhl":
                child.right = self.right
                child.destination = -child.width
                child.y = self.center_y+(self.lane_spacing*0.5)+(self.vls*0.5)
                child.width = self.vehicle_height
                child.height = self.vehicle_width

            if child.come_from ==  "rhl":
                child.x = self.x
                child.destination = self.width+child.width
                child.top = self.center_y-(self.lane_spacing*0.5)-(self.vls*0.5)
                child.width = self.vehicle_height
                child.height = self.vehicle_width
            
            if child.come_from == "Nowhere":
                child.x = self.x+10
                child.y = self.y+ 10
                child.width = self.width-20
                child.height = self.height-20
                

                

                
    def process_touch_pos(self,touch,*args):
        #returns the lane in which the touch falls on
        if (touch.x<(self.center_x-(self.lane_spacing*0.5))
            and 
            touch.x>(self.center_x-(self.lane_spacing*0.5)-(self.vehicle_width)-(self.vls))):
            return  "lvl"
        elif (
            touch.x>(self.center_x+(self.lane_spacing*0.5))
            and 
            touch.x<(self.center_x+(self.lane_spacing*0.5)+self.vehicle_width+self.vls)
            ):
            return "rvl"
                    
        elif (
            touch.y>(self.center_y+(self.lane_spacing*0.5))
            and 
            touch.y<(self.center_y+(self.lane_spacing*0.5)+self.vehicle_width+self.vls)
            ):
            return "lhl"
        elif (
            touch.y<(self.center_y-(self.lane_spacing*0.5))
            and 
            touch.y>(self.center_y-(self.lane_spacing*0.5)-self.vehicle_width-self.vls)
            ):
            return "rhl"
        
    def gen_vehicle_at_lvl(self,*args):
        vehicle = Vehicle()
        vehicle.background_color = get_random_color(1)
        vehicle.width = self.vehicle_width
        vehicle.height = self.vehicle_height
        vehicle.top = self.top+vehicle.height
        vehicle.come_from= "lvl"
        vehicle.destination = -vehicle.height
        vehicle.destination_reached = False
        vehicle.right = self.center_x-(self.lane_spacing*0.5)-(self.vls*0.5)
        vehicle.speed = self.default_speed
        vehicle.set = False
        self.add_widget(vehicle) 

        
    def gen_vehicle_at_rvl(self,*args):
        vehicle = Vehicle()
        vehicle.background_color = get_random_color(1)
        vehicle.width = self.vehicle_width
        vehicle.height = self.vehicle_height
        vehicle.y = self.y-vehicle.height
        vehicle.come_from = "rvl"
        vehicle.destination = self.height+vehicle.height
        vehicle.destination_reached = False
        vehicle.x = self.center_x+(self.lane_spacing*0.5)+(self.vls*0.5)
        vehicle.speed = self.default_speed
        vehicle.set = False
        self.add_widget(vehicle)

    def gen_vehicle_at_lhl(self,*args):
        vehicle = Vehicle()
        vehicle.background_color = get_random_color(1)
        vehicle.width = self.vehicle_height
        vehicle.height = self.vehicle_width
        vehicle.right = self.right+vehicle.width
        vehicle.y = self.center_y+(self.lane_spacing*0.5)+(self.vls*0.5)
        vehicle.come_from = "lhl"
        vehicle.destination = -vehicle.width
        vehicle.destination_reached = False
        vehicle.speed = self.default_speed
        vehicle.set = False
        self.add_widget(vehicle) 

        
    def gen_vehicle_at_rhl(self,*args):
        vehicle = Vehicle()
        vehicle.background_color = get_random_color(1)
        vehicle.width = self.vehicle_height
        vehicle.height = self.vehicle_width
        vehicle.x = self.x-vehicle.width
        vehicle.top = self.center_y-(self.lane_spacing*0.5)-(self.vls*0.5)
        vehicle.come_from = "rhl"
        vehicle.destination = self.width+vehicle.width
        vehicle.destination_reached = False
        vehicle.speed = self.default_speed
        vehicle.set = False
        self.add_widget(vehicle) 

        
    

            



class TrafficApp(App):
    def build(self):
        self.root = Root()
        return self.root
    
if __name__ == "__main__":
    TrafficApp().run()
