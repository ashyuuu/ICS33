# The Hunter class is derived (in order) from both Pulsator and Mobile_Simulton.
#   It updates/displays like its Pulsator base, but is also mobile (moving in
#   a straight line or in pursuit of Prey), like its Mobile_Simultion base.


from prey  import Prey
from pulsator import Pulsator
from mobilesimulton import Mobile_Simulton
import math,random


class Hunter(Pulsator, Mobile_Simulton):  
    # special kind of pulsator
    # moves towards the closest edible in vision (limited)
    def __init__(self,x,y,w=20,h=20,s=5):
        Mobile_Simulton.__init__(self,x,y,w,h,random.random()*math.pi*2,s)
        Pulsator.__init__(self,x,y)
    
    def update(self,model,vision=200):
        seen=set()
        for i in model.find(f'isinstance(s,Prey) and type(s) != {type(self).__name__}'):
            if i.distance(self.get_location()) <= vision:
                seen.add((i,i.distance(self.get_location())))
        if len(seen) >0:
            target = sorted(seen,key=lambda x:x[1])[0][0]
            self.set_angle(math.atan2(target.get_location()[1]-self.get_location()[1],target.get_location()[0]-self.get_location()[0]))
        Pulsator.update(self,model)
        self.move()
        self.wall_bounce()
        return seen 
        