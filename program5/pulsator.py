# A Pulsator is a Black_Hole; it updates as a Black_Hole
#   does, but also by growing/shrinking depending on
#   whether or not it eats Prey (and removing itself from
#   the simulation if its dimension becomes 0), and displays
#   as a Black_Hole but with varying dimensions 


from blackhole import Black_Hole


class Pulsator(Black_Hole): 
    # special kind of blackhole
    # gets bigger when eating and smaller when starving
    # if too small: dies and removed from simlulation
    counter = 30
    def __init__(self,x,y):
        self._counter = 0
        Black_Hole.__init__(self,x,y)
    
    def update(self,model):
        eaten = Black_Hole.update(self,model)
        for i in eaten:
            self.set_dimension(self.get_dimension()[0]+1,self.get_dimension()[1]+1)
            self._counter = 0
        if self._counter % Pulsator.counter == 0 and self._counter != 0:
            self.set_dimension(self.get_dimension()[0]-1,self.get_dimension()[1]-1)
            if 0 in self.get_dimension():
                model.simultons.remove(self)
        self._counter+=1
        return eaten