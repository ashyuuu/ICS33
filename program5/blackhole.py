# The Black_Hole class is derived from Simulton; for updating it finds+removes
#   objects (of any class derived from Prey) whose center is contained inside
#   its radius (returning a set of all eaten simultons), and displays as a
#   black circle with a radius of 10 (width/height 20).
# Calling get_dimension for the width/height (for containment and displaying)'
#   will facilitate inheritance in Pulsator and Hunter

from simulton import Simulton
from prey import Prey


class Black_Hole(Simulton):  
    # stationary obj that eats edible whose center is within perim
    # override contains from simulton
    radius = 10
    def __init__(self,x,y,w=None,h=None):
        if not w or not h:
            w = Black_Hole.radius*2
            h = Black_Hole.radius*2
        Simulton.__init__(self,x,y,w,h)
        
    def contains(self,xy):
        return self.distance(xy) < self.get_dimension()[0]
    
    def update(self,model):
        #global simultons
        #model.simultons = model.find('not isinstance(s,Prey)')
        eaten = set()
        for i in model.find(f'isinstance(s,Prey) and type(s)!={type(self).__name__}'):
            if self.contains(i.get_location()) and i in model.simultons:
                eaten.add(i)
                model.simultons.remove(i)
        return eaten
    
    def display(self,canvas):
        canvas.create_oval(self._x-self.get_dimension()[0], self._y-self.get_dimension()[1],self._x+self.get_dimension()[0], self._y+self.get_dimension()[1],fill='black')