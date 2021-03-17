# Tyler Percy
# 2/1/21
# PHY 2200

from vpython import *
from ode import *
from numpy import array, zeros
from random import randint, seed
from time import time

def lunar_lander():

    seed(randint(0, 1000))

    global Fthrust

    # function to calculate differential equations
    def get_diffeq(d,tn):
        rates = zeros(6)
        rates[0] = d[3]
        rates[1] = d[4]
        rates[2] = d[5]
        rates[3] =  Fthrust.x/lander.m
        rates[4] = (Fthrust.y - lander.m * G)/lander.m
        rates[5] = Fthrust.z/lander.m
        return rates

    # key events
    def handleKeyDown(event):
        global Fthrust
        if event.key == 'w':
            Fthrust = thrust*vec(0,1,0)
            fireU.visible=True
            FarrowU.visible=True
        elif event.key == 'left':
            Fthrust = thrust*vec(-1,0,0)
            fireL.visible=True
            FarrowL.visible=True
        elif event.key == 'right':
            Fthrust = thrust*vec(1,0,0)
            fireR.visible=True
            FarrowR.visible=True
        elif event.key == 'up':
            Fthrust = thrust*vec(0,0,-1)
            fireB.visible = True
            FarrowB.visible = True
        elif event.key == 'down':
            Fthrust = thrust*vec(0,0,1)
            fireF.visible = True
            FarrowF.visible = True

    def handleKeyUp(event):
        global Fthrust
        Fthrust = vec(0,0,0)
        fireR.visible=False
        FarrowR.visible=False
        fireL.visible=False
        FarrowL.visible=False
        fireU.visible=False
        FarrowU.visible=False
        fireB.visible = False
        FarrowB.visible = False
        fireF.visible = False
        FarrowF.visible = False

    #initialize objects to build scene
    scene = canvas(title = 'Lunar Lander Game\n', width = 800, height = 600, range = 25) 
    box(pos = vec(0, -14.01, 0), size = vec(40, .5, 40), color = color.white) #floor
    landing_pad = box(pos = vec(randint(-14, 14), -13.75, randint(-14, 14)), size = vec(5, .5, 5), color=color.red)
    lander = box(pos = vec(0, 5, 0), size = vec(2,2,2), color = color.yellow)
    shadow = sphere(pos = vec(lander.pos.x, lander.pos.y-18.5, lander.pos.z), \
            size = vec(3, .5, 3), color = color.black)
    
    #constant variables
    dt = 0.01
    G=1.6
    L=3
    lander.m = 1e4
    thrust=3*lander.m*G
    scale=2*L/lander.m/G
    sw=0.5

    #variable variables =)
    t = 0
    Fthrust=vec(0,0,0)
    lander.v = vec(0,0,0)
    fuel = 100.0

    #info labels
    vstr = ("Speed: %.2f" % (0))
    lbl = label(pos = vec(0,24,0), text=vstr)
    fuel_str = ("Fuel: %.2f" % (fuel))
    fuel_lbl = label(pos = vec(-20,24,0), text = fuel_str)

    # initial set of values to be used in RK4 method
    data = array([lander.pos.x, lander.pos.y, lander.pos.z,lander.v.x, lander.v.y, lander.v.z])

    # decorations
    for _ in range(0, 30):
        box(pos = vec(randint(-20, 30), randint(0,10), 20), size = vec(.25, .25, .05), color = color.white)

    #Initialize cones and arrows to represent thrust of lander
    fireR=cone(pos=lander.pos-vec(L/2,0,0), radius=L/4, axis=L/2*vec(-1,0,0), color=color.orange, visible=False)
    fireL=cone(pos=lander.pos+vec(L/2,0,0), radius=L/4, axis=L/2*vec(1,0,0), color=color.orange, visible=False)
    fireU=cone(pos=lander.pos-vec(0,L/2,0), radius=L/4, axis=L/2*vec(0,-1,0), color=color.orange, visible=False)
    fireB = cone(pos = lander.pos-vec(0,0,2), radius = 1, axis = 2*vec(0,0,1), color = color.orange, visible = False)
    fireF = cone(pos = lander.pos-vec(0,0,2), radius = 1, axis = 2*vec(0,0,-1), color = color.orange, visible = False)
    FarrowR=arrow(pos=lander.pos, axis=scale*thrust*vec(1,0,0), color=color.orange, shaftwidth=sw, visible=False)
    FarrowL=arrow(pos=lander.pos, axis=scale*thrust*vec(-1,0,0), color=color.orange, shaftwidth=sw, visible=False)
    FarrowU=arrow(pos=lander.pos, axis=scale*thrust*vec(0,1,0), color=color.orange, shaftwidth=sw, visible=False)
    Farrowgrav=arrow(pos=lander.pos, axis=scale*lander.m*G*vec(0,-1,0), color=color.white, shaftwidth=sw, visible=True)
    FarrowB = arrow(pos = lander.pos, axis = scale*thrust*vec(0,0,-1), color = color.orange, shaftwidth = sw, visible = False)
    FarrowF = arrow(pos = lander.pos, axis = scale*thrust*vec(0,0,1), color = color.orange, shaftwidth = sw, visible = False)

    #tell our scene to recognize input
    scene.bind('keydown', handleKeyDown) 
    scene.bind('keyup', handleKeyUp)

    scene.append_to_title("Hold 'left or right' to move left or right.\n")
    scene.append_to_title("Hold 'up or down' to move forward or backward.\n")
    scene.append_to_title("Hold 'w' to move up.\n")
    scene.append_to_title("Land on the red square to win.\n")
    scene.append_to_title("Be careful not to fly too far away from the moon or you'll get lost!\n")

    scene.waitfor("click")

    playing = True
    t0 = time()
    while playing:
        rate(100)
        #get new data values for position and velocity
        if fuel > 0:
            data = RK4(get_diffeq,data,t,dt)
            lander.pos = vec(data[0], data[1], data[2])
            lander.v = vec(data[3], data[4],data[5])
            fuel = fuel - (mag(Fthrust)/lander.m/100)
            fuel_str = "Fuel: %.2f" % (fuel)
            fuel_lbl.text = fuel_str

        #update speed in label
        vstr = "Speed: %.2f" % (mag(lander.v))
        lbl.text = vstr

        #update our thrust representation objects according to new position
        Farrowgrav.pos=lander.pos
        Farrowgrav.axis=scale*lander.m*G*vec(0,-1,0)
        FarrowR.pos = lander.pos
        FarrowL.pos = lander.pos
        FarrowU.pos = lander.pos
        FarrowB.pos = lander.pos
        FarrowF.pos = lander.pos
        fireR.pos = lander.pos-vec(1,0,0)
        fireL.pos = lander.pos+vec(1,0,0)
        fireU.pos = lander.pos-vec(0,1,0)
        fireB.pos = lander.pos-vec(0,0,1)
        fireF.pos = lander.pos+vec(0,0,1)

        #update shadow position whenever lander moves
        shadow.pos.x = lander.pos.x
        shadow.pos.z = lander.pos.z

        #if lander landed outside pad
        if (lander.pos.y <= shadow.pos.y+1):
            if mag((lander.pos-vec(0,1,0))-landing_pad.pos)<1.5:
                landing_pad.color = color.green
                t1 = time()
                lbl.text = "You have landed."
                if mag(lander.v) < 2:
                    lbl.text += "You landed within the allowed speed of < 2m."
                scene.waitfor("mousedown")
                playing = False
                continue
        #if lander landed inside pad
            else:
                t1 = time()
                lbl.text = "You crashed!"
                scene.waitfor("mousedown")
                playing = False
                continue
        #if lander moves too far away from map
        if abs(lander.pos.x) > scene.range*1.5 or abs(lander.pos.y) > scene.range*1.5 or abs(lander.pos.z) > scene.range*1.5:
            t1 = time()
            lbl.text = "Your lander is lost in space!"
            scene.waitfor("mousedown")
            playing = False
            continue

        t = t+dt
    
    lbl.text = "You landed with speed: %.2f\nTime elapsed: %.2f seconds\nFuel Remaining: %.2f" % (mag(lander.v), (t1-t0), fuel)
    fuel_lbl.visible = False
    scene.pause()
    scene.title = ""
    scene.delete()
    lunar_lander()

lunar_lander()
