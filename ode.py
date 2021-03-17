# Tyler Percy
# 2/1/21
# PHY 2200

def Euler(diffeq, yn, tn, h):
    """ Given y_n at t, calculate and return y_n+1 at t+h"""

    #calculate y_n+1
    yn1 = yn + diffeq(yn,tn)*h

    return yn1

def RK2(diffeq, yn, tn, h):
    k1 = h*diffeq(yn, tn)
    k2 = h*diffeq(yn+(k1/2), tn+(h/2))
    
    yn1 = yn + k2
    
    return yn1

def RK4(diffeq, yn, tn, h):
    k1 = h*diffeq(yn, tn)
    k2 = h*diffeq(yn+(k1/2), tn+(h/2))
    k3 = h*diffeq(yn+(k2/2), tn+(h/2))
    k4 = h*diffeq(yn+k3, tn+h)
    
    yn1 = yn + k4
    
    return yn1
