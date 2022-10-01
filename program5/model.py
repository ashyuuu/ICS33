import controller
import model   # Calls to update in update_all are passed a reference to model

#Use the reference to this module to pass it to update methods
from ball      import Ball
from floater   import Floater
from blackhole import Black_Hole
from pulsator  import Pulsator
from hunter    import Hunter
from special import Special
from prey import Prey


# Global variables: declare them global in functions that assign to them: e.g., ... = or +=
running     = False
cycle_count = 0
simultons   = set()
obj=None

#return a 2-tuple of the width and height of the canvas (defined in the controller)
def world():
    return (controller.the_canvas.winfo_width(),controller.the_canvas.winfo_height())

#reset all module variables to represent an empty/stopped simulation
def reset ():
    global running,cycle_count,simultons,obj
    running     = False
    cycle_count = 0
    simultons.clear()
    obj         = None

#start running the simulation
def start ():
    global running
    running = True


#stop running the simulation (freezing it)
def stop ():
    global running
    running = False 


#step just one update in the simulation
def step ():
    global running
    running = True
    update_all()
    display_all()
    running = False


#remember the kind of object to add to the simulation when an (x,y) coordinate in the canvas
#  is clicked next (or remember to remove an object by such a click)   
def select_object(kind):
    global obj
    obj = kind


#add the kind of remembered object to the simulation (or remove all objects that contain the
#  clicked (x,y) coordinate
def mouse_click(x,y):
    global obj, simultons
    if obj == 'Remove':
        for k in find(f's.contains(({x},{y}))'):
            remove(k)
    elif obj !=None:
        s = Ball(x,y) if obj == 'Ball' else Floater(x,y) if obj=='Floater' \
        else Hunter(x,y) if obj=='Hunter' else Black_Hole(x,y) if obj=='Black_Hole' else Pulsator(x,y) if obj=='Pulsator' else Special(x,y)
        add(s) 
        

#add simulton s to the simulation
def add(s): 
    global simultons
    simultons.add(s)
    

# remove simulton s from the simulation    
def remove(s):
    global simultons
    simultons.remove(s)
    

#find/return a set of simultons that each satisfy predicate p    
def find(p):
    #print(p)
    global simultons
    l=set()
    for s in simultons:
        if eval(p):
            l.add(s)    
    return l


# for each simulton in this simulation, call update (passing model to it) 
#this function should loop over one set containing all the simultons
#  and should not call type or isinstance: let each simulton do the
#  right thing for itself, without this function knowing what kinds of
#  simultons are in the simulation
def update_all():
    global cycle_count, simultons
    if running:
        cycle_count += 1
        for k in range(len(simultons)):
            try:
                list(simultons)[k].update(model)
            except IndexError:
                k-=1
#How to animate: 1st: delete all simultons on the canvas; 2nd: call display on
#  all simulton being simulated, adding each back to the canvas, maybe in a
#  new location; 3rd: update the label defined in the controller for progress 
#this function should loop over one set containing all the simultons
#  and should not call type or isinstance: let each simulton do the
#  right thing for itself, without this function knowing what kinds of
#  simultons are in the simulation
def display_all():
    # remove current objects
    global simultons,cycle_count
    for i in controller.the_canvas.find_all():
        controller.the_canvas.delete(i)
    for k in simultons:
        k.display(controller.the_canvas)
    controller.the_progress.config(text=str(len(simultons))+" Simultons/"+str(cycle_count)+" cycles")