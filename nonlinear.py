import pandas as pd
import numpy as np
import scipy as sy
from scipy import signal as sig
import matplotlib.pyplot as plt
from datetime import datetime as dt

import misc 
import models

# The dual oscillator attempts to model price action through
# the motion of a two axis simple oscillator. It accepts
# two parameters X1 and X2
def dual_oscillator(data,obv=['v','c'],k1=1,k2=1):

    data_o = data.copy()
    e1 = [1,0]
    e2 = [0,1]

    x1 = f'd{obv[0]}1t_o'
    x2 = f'd{obv[1]}1t_o'

    dotx1 = f'd{obv[0]}2t_oo'
    dotx2 = f'd{obv[1]}2t_oo'

    #These values represent the x and y coords
    #of point 1 and point 2.
    l1 = data_o[x1] - data_o[x1].shift(1)
    l2 = data_o[x2] - data_o[x2].shift(1)

    r1 = pd.DataFrame({'e1':data_o[x1].add(l1),'e2':data_o[x2]})
    r2 = pd.DataFrame({'e1':data_o[x1],'e2':data_o[x2].add(l2)})

    r1mag = np.sqrt(r1['e1']**2 + r1['e2']**2)
    r2mag = np.sqrt(r2['e1']**2 + r2['e2']**2)

    c1 = 1 - (l1/r1mag)
    c2 = 1 - (l2/r2mag)

    data_o['c1'] = c1
    data_o['c2'] = c2

    f1 = data_o[dotx1].multiply(c1,axis=0) + data_o[x1].multiply(k1,axis=0) 
    f2 = data_o[dotx2].multiply(c2,axis=0) + data_o[x2].multiply(k2,axis=0)

    f_sys = f1.add(f2,axis=0)

    data_o['f_sys'] = f_sys

    # F=MA this is the 
    ma1 = f1
    ma2 = f2

    data_o['ma1'] = ma1
    data_o['ma2'] = ma2

    m1 = f1.divide(data_o[f'd{obv[0]}3t_ooo'].add(data_o[f'd{obv[1]}3t_ooo']))
    m2 = f2.divide(data_o[f'd{obv[0]}3t_ooo'].add(data_o[f'd{obv[1]}3t_ooo']))

    data_o['m1'] = m1
    data_o['m2'] = m2
    
    m_sys = f_sys.divide(data_o[f'd{obv[0]}3t_ooo'].add(data_o[f'd{obv[1]}3t_ooo']))

    data_o['m_sys'] = m_sys

    # # Momentum calculations based on the derived masses m1 and m2
    p1 = m1.multiply(data_o[f'd{obv[0]}2t_oo'],axis=0)
    p2 = m2.multiply(data_o[f'd{obv[1]}2t_oo'],axis=0)

    data_o['p1'] = p1
    data_o['p2'] = p2
# 
    dp1dt = p1-p1.shift(1)
    dp2dt = p2-p2.shift(1) 

    data_o['dp1t_o'] = dp1dt
    data_o['dp2t_o'] = dp2dt

    dp1dv = (p1-p1.shift(1)).divide(data_o[f'd{obv[0]}2t_oo']-data_o[f'd{obv[0]}2t_oo'].shift(1),axis=0)
    dp2dv = (p2-p2.shift(1)).divide(data_o[f'd{obv[1]}2t_oo']-data_o[f'd{obv[1]}2t_oo'].shift(1),axis=0)

    data_o['dp1v_o'] = dp1dv
    data_o['dp2v_o'] = dp2dv 

    data_o.fillna(0,inplace=True)

    for col in data_o.columns:
        data_o[col] = data_o[col].replace([np.inf, -np.inf], np.nan)
        data_o[col] = data_o[col].fillna(np.abs(data_o[col]).max())
 
    data_n = misc.normalizedf(data_o)

    #breakpoint()
    return data_n

################
#TEST BED
################
# import test
# data_o = test.testbed(start=dt(2020,1,1),stop=dt(2020,2,1))
# viz = showplots(data_o)
# viz.show()
# pass