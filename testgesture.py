'''
Created on Jan 23, 2016

@author: shaibujnr
'''
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.gesture import Gesture,GestureDatabase
from kivy.graphics import Ellipse,Color,Line
from gs import up_swipe,down_swipe,right_swipe,left_swipe

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
class Tgw(Widget):
    def on_touch_down(self,touch,*args):
        self.gpoints = []
        self.gpoints.append(touch.pos)
        with self.canvas:
            Color(rgba=(1,1,1,1))
            d = 5
            Ellipse(pos=(touch.x-d/2,touch.y-d/2),size=(d,d))
            self.line = Line(points=touch.pos)
            
    def on_touch_move(self,touch,*args):
        self.gpoints.append(touch.pos)
        self.line.points+= touch.pos
        
    def on_touch_up(self,touch,*args):
        self.gpoints.append(touch.pos)
        self.line.points+=touch.pos
        gesture = Gesture()
        gesture.add_stroke(point_list=self.gpoints)
        gesture.normalize()
        x=gdb.find(gesture,minscore=0.5)
        if x:
            print x[1].name
        
        
class tgApp(App):
    def build(self):
        return Tgw()
    
if __name__ == "__main__":
    tgApp().run()