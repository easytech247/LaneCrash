from kivy.app import App
from kivy.uix.widget import Widget
from Vehicles import Vehicle
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.utils import get_random_color
from kivy.lang import Builder
from kivy.properties import (ListProperty,
                             NumericProperty,
                             ObjectProperty,
                             StringProperty)

from functools import partial
Builder.load_file("traf.kv")
class StartButton(Button):
    uid = StringProperty("btn")
class Lane(Widget):
    road = ObjectProperty()
    col = ListProperty()
    uid = StringProperty()
    


        

    

    

            
            
    

            

    
class Field(Widget):
    hlvlane = ObjectProperty()
    hrvlane = ObjectProperty()
    llhlane = ObjectProperty()
    lrhlane = ObjectProperty()
    llvlane = ObjectProperty()
    lrvlane = ObjectProperty()
    rlhlane = ObjectProperty()
    rrhlane = ObjectProperty()
    ot = NumericProperty(0)
    default_speed = NumericProperty(4)
    vehicle_width = NumericProperty()
    vehicle_height= NumericProperty()
    clspacing = NumericProperty(5)
    lane_spacing = NumericProperty(10)
    
    

    def on_touch_down(self,touch,*args):
        for lane in self.children:
            if lane.collide_point(*touch.pos) and lane.uid!="btn":
                print lane.uid
                break
            elif lane.collide_point(*touch.pos) and lane.uid == "btn":
                super(Field,self).on_touch_down(touch)
            else:
                pass
                
                
    def start(self,*args):
        Clock.schedule_once(partial(self.gen_vehicle,"lvlane"))
        Clock.schedule_once(partial(self.gen_vehicle,"lhlane"))
        Clock.schedule_once(partial(self.gen_vehicle,"rvlane"))
        Clock.schedule_once(partial(self.gen_vehicle,"rhlane"))
        Clock.schedule_interval(self.set_vehicles_on_motion,0.5)

    
    def set_lanes(self,*args):
        for lane in self.children:
            if lane.uid == "lvlane":
                lane.col = 1,1,1,1
                lane.height = self.height+self.ot+self.ot
                lane.width = self.vehicle_width+(self.clspacing*2)
                lane.right = self.center_x-(self.lane_spacing*0.5)
                lane.top = self.top+self.ot

            if lane.uid == "rvlane":
                lane.col = 1,1,1,1
                lane.height = self.height+self.ot+self.ot
                lane.width = self.vehicle_width+(self.clspacing*2)
                lane.x = self.center_x+(self.lane_spacing*0.5)
                lane.y = self.y-self.ot

            if lane.uid == "lhlane":
                lane.col = 1,1,1,1
                lane.height = self.vehicle_width+(self.clspacing*2)
                lane.width = self.width+self.ot+self.ot
                lane.right= self.right+self.ot
                lane.y = self.center_y+(self.lane_spacing*0.5)
            if lane.uid == "rhlane":
                lane.col = 1,1,1,1
                lane.height = self.vehicle_width+(self.clspacing*2)
                lane.width = self.width+self.ot+self.ot
                lane.x = self.x-self.ot
                lane.top = self.center_y-(self.lane_spacing*0.5)
                
                
    def on_size(self,*args):
        self.vehicle_width = self.width/15
        self.vehilcle_height = self.height/20
        self.set_lanes()
        
    def gen_vehicle(self,lane,*args):
        if lane == "lvlane":
            vehicle = Vehicle()
            vehicle.background_color = 0,0,0,1
            vehicle.width = self.vehicle_width
            vehicle.height = self.vehicle_height
            vehicle.top = self.lvlane.top
            vehicle.center_x = self.lvlane.center_x
            vehicle.speed = self.default_speed
            self.lvlane.add_widget(vehicle)
            
        elif lane == "rvlane":
            vehicle = Vehicle()
            vehicle.background_color = 0,0,0,1
            vehicle.width = self.vehicle_width
            vehicle.height = self.vehicle_height
            vehicle.y = self.rvlane.y
            vehicle.center_x = self.rvlane.center_x
            vehicle.speed = self.default_speed
            self.rvlane.add_widget(vehicle)
            
        elif lane == "lhlane":
            vehicle = Vehicle()
            vehicle.background_color = 0,0,0,1
            vehicle.width = self.vehicle_height
            vehicle.height = self.vehicle_width
            vehicle.right = self.lhlane.right
            vehicle.center_y = self.lhlane.center_y
            vehicle.speed = self.default_speed
            self.lhlane.add_widget(vehicle)
            
        elif lane == "rhlane":
            vehicle = Vehicle()
            vehicle.background_color = 0,0,0,1
            vehicle.width = self.vehicle_height
            vehicle.height = self.vehicle_width
            vehicle.x = self.rhlane.x
            vehicle.center_y = self.rhlane.center_y
            vehicle.speed = self.default_speed
            self.rhlane.add_widget(vehicle)
            

            
    def set_vehicles_on_motion(self,*args):
        for lane in self.children:
            if lane.uid == "lvlane":
                for vehicle in lane.children:
                    vehicle.top-=vehicle.speed
            elif lane.uid == "rvlane":
                for vehicle in lane.children:
                    vehicle.y+=vehicle.speed
            elif lane.uid == "lhlane":
                for vehicle in lane.children:
                    vehicle.right -=vehicle.speed
            elif lane.uid == "rhlane":
                for vehicle in lane.children:
                    vehicle.x+=vehicle.speed
                
            


class trafApp(App):
    def build(self):
        return Field()
    
if __name__ == "__main__":
    trafApp().run()
