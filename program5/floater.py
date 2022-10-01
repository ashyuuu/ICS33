# A Floater is Prey; it updates by moving mostly in
#   a straight line, but with random changes to its
#   angle and speed, and displays as ufo.gif (whose
#   dimensions (width and height) are computed by
#   calling .width()/.height() on the PhotoImage 


from PIL.ImageTk import PhotoImage
from prey import Prey
import random,math


class Floater(Prey): 
    # edible that travel in irregular patterns
    def __init__(self,x,y):
        self._image = PhotoImage(file='ufo.gif') 
        Prey.__init__(self,x,y,self._image.width(),self._image.height(),random.random()*math.pi*2,5)
        
    def update(self,model):
        self.move()
        self.wall_bounce()
        if random.random() < 0.3:
            self.set_angle(self.get_angle()+random.random()-0.5)
            self.set_speed(random.random()-0.5)
            if self.get_speed() < 3:
                self.set_speed(3)
            elif self.get_speed() > 7:
                self.set_speed(7)
        
    def display(self,canvas):
        canvas.create_image(*self.get_location(),image=self._image)
