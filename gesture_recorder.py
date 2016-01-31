'''
Created on Jan 23, 2016

@author: shaibujnr
'''
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.gesture import Gesture,GestureDatabase
from kivy.graphics import Canvas,Color,Ellipse,Line

class Grw(Widget):
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
        self.line.points+=touch.pos
        
    def on_touch_up(self,touch,*args):
        self.gpoints.append(touch.pos)
        self.line.points+=touch.pos
        gesture = Gesture()
        gdb = GestureDatabase()
        gesture.add_stroke(point_list=self.gpoints)
        gesture.normalize()
        gdb.add_gesture(gesture)
        gstr=gdb.gesture_to_str(gesture)
        gfile = open("gestures.txt","w")
        gfile.write("swipe\n")
        gfile.write("-----------\n")
        gfile.write("\n")
        gfile.write(gstr)
        gfile.close()
        
        
        

        
class grApp(App):
    def build(self):
        return Grw()

if __name__ == "__main__":
    grApp().run()
    


    