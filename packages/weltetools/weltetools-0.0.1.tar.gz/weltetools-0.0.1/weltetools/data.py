import scipy.optimize as sp
from typing import List,Callable
import types
import numpy

def fit_curve(func: Callable,x_vals: List[float],y_vals: List[float],startx:float=None,endx:float=None,starty:float=None,endy:float=None,guess:List[float]=None,maxfev:int=10000)->tuple[Callable,List[float],List[float]]:
    if not isinstance(func, (types.FunctionType)): raise Exception("Bad parameter 'func'")  
    if not isinstance(x_vals, (list,numpy.ndarray)): raise Exception("Bad parameter 'x_vals'")    
    if not isinstance(y_vals, (list,numpy.ndarray)): raise Exception("Bad parameter 'y_vals'")        
    if not isinstance(startx, (float,int,types.NoneType)): raise Exception("Bad parameter 'startx'")    
    if not isinstance(endx, (float,int,types.NoneType)): raise Exception("Bad parameter 'endx'")    
    if not isinstance(starty, (float,int,types.NoneType)): raise Exception("Bad parameter 'starty'")    
    if not isinstance(endy, (float,int,types.NoneType)): raise Exception("Bad parameter 'endy'")    
    if not isinstance(guess, (list,types.NoneType,numpy.ndarray)): raise Exception("Bad parameter 'guess'")    
    if not isinstance(maxfev, (int)): raise Exception("Bad parameter 'maxfev'") 
    if (len(x_vals) < 2): raise Exception("'x_vals' too small")
    if (len(x_vals) != len(y_vals)): raise Exception("Size of 'x_vals' does not match size of 'y_vals'")
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
    if (len(x_fit)<2): raise Exception("wrong bounds")
    if (guess==None): popt,pcov=sp.curve_fit(func,x_fit,y_fit,maxfev=maxfev)
    else: popt,pcov=sp.curve_fit(func,x_fit,y_fit,p0=guess,maxfev=maxfev)
    return lambda x: func(x-startx, *popt) + starty,popt,pcov
