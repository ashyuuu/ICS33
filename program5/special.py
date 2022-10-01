# Specials are special preys that are at the same time hunters
# that move a little slower and can see potential threats
# from a far away and run for its life early (turning 180 degrees around)
# however when they see any instances of Prey they would also hunt for it 

# Specials get eaten by all instances of Black_Holes (except for special. they are not cannibals)
# when preys and predators are both in sight of a Special, it might take risks
# if the prey is not in sight of the predator and if the prey is closer to Special
# if the predator is stationary, Special will also take the risk
# it will take the risk and hunt for the prey. In all other cases, it will run

# Like Hunters, a Special might starve to death the same way a Hunter might

# Specials travel in straight lines and have a constant speed throughout their lifetimes
# It is derived from the Prey and Hunter class. They are displayed in green circles 
# It starts with a random angle, a constant speed of 7 pixels/update, and a radius of 7

from prey import Prey
from hunter import Hunter
import math,random


class Special(Prey,Hunter):
    radius = 7
    def __init__(self,x,y):
        Prey.__init__(self,x,y,Special.radius*2,Special.radius*2,random.random()*2*math.pi,7)
        Hunter.__init__(self,x,y)
    
    def update(self,model):
        print(self._counter,self.get_dimension())
        seen=[Hunter.update(self,model,300),set()]
        for i in model.find('isinstance(s,Black_Hole)'):
            if i.distance(self.get_location()) <= 300:
                seen[1].add((i,i.distance(self.get_location())))
 
        
        if len(seen) >0: 

            closest_prey = sorted(seen[0],key=lambda x:x[1])[1] if len(seen[0]) > 0 else None
            closest_pred = sorted(seen[1],key=lambda x:x[1])[1] if len(seen[1]) > 0 else None
            
            
            if closest_prey and (not closest_pred or (closest_prey[1]<closest_pred[1] and (type(closest_pred) != Hunter or closest_pred.distance(closest_prey[0].get_location) < 200) )):
                self.set_angle(math.atan2(closest_prey[0].get_location()[1]-self.get_location()[1],closest_prey[0].get_location()[0]-self.get_location()[0]))
            elif closest_pred:
                self.set_angle(math.atan2(closest_pred[0].get_location()[1]-self.get_location()[1],closest_pred[0].get_location()[0]-self.get_location()[0])-math.pi)
            
            
            
        self.move()
        self.wall_bounce()
    
    def display(self,canvas):
        canvas.create_oval(self._x-self.get_dimension()[0]/2, self._y-self.get_dimension()[1]/2,self._x+self.get_dimension()[0]/2, self._y+self.get_dimension()[1]/2,fill='green')