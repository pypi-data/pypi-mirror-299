import scipy.optimize as sp

from typing import List,Callable
def fit_curve(func: Callable,x_vals: List[float],y_vals: List[float],startx:float=None,endx:float=None,starty:float=None,endy:float=None,guess:List[float]=None,maxfev:int=10000)->tuple[Callable,List[float],List[float]]:
    #if not isinstance(func, (Callable)): raise Exception("")
    print(type(func))
    
    
    
    if (len(x_vals) < 2): raise Exception("Es gibt zu wenige X-Werte")
    if (len(x_vals) != len(y_vals)): raise Exception("Die Länge der X-Werte ist ungleich der Länge der Y-Werte")
    if startx == None: startx = x_vals[0]
    if endx == None: endx = x_vals[len(x_vals)-1]
    if starty == None: starty = min(y_vals)
    if endy == None: endy = max(y_vals)
    x_fit,y_fit = [],[]
    for i in range(0,len(x_vals)):
        x = x_vals[i]
        y = y_vals[i]
        if (startx <= x <= endx and starty <= y <= endy):
            x_fit.append(x-startx)
            y_fit.append(y-starty)
    if (len(x_fit)<2): raise Exception("Start_ Parameter sind falsch gesetzt")
    if (guess==None): popt,pcov=sp.curve_fit(func,x_fit,y_fit,maxfev=maxfev)
    else: popt,pcov=sp.curve_fit(func,x_fit,y_fit,p0=guess,maxfev=maxfev)
    return lambda x: func(x-startx, *popt) + starty,popt,pcov
