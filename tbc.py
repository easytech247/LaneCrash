'''
Created on Jan 24, 2016

@author: shaibujnr
'''
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.core.audio import SoundLoader,Sound

Builder.load_string("""
<root>:
    canvas:
        Rectangle:
            pos: root.pos
            size: root.size
            source: "imgs/src.jpg"
""")

class root(Widget):
    def on_touch_down(self,touch,*args):
        sound = SoundLoader.load("audio/output.wav")
        if sound:
            sound.play()
        else:
            print sound
class tgwApp(App):
    def build(self):
        return root()

if __name__ == "__main__":
    tgwApp().run()