import nonlinear as nl
import misc
from datetime import timedelta
import models as mod
import frequencies as freq
import plots

def stream_r(data,harms,F,mode,refresh,obv=['v','c'],diff_offset=1,diff=1,m=1,N=7):
    # At the start it is assumed that test
    # N days have already been processed tst
    for row in data.index:
        try:
            print(f'\n - Processing Frame #{row.value}: start:{min(data.index)} end:{max(data.index)}\n')
        except KeyboardInterrupt:
            break

        data_i = data.loc[row:row+timedelta(days=N),:]

        data_p = mod.point_sys(data_i,size=3)
        data_d = mod.ddm(   data=data_p
                            )
        data_n = misc.normalizedf(data_d)
        data_c = freq.complex_coords(data_n,[data_n.x1nm,data_n.x2nm])
        data_o = nl.dual_oscillator(data=data_c
                                    ,F=F
                                    ,m=m
                                    ,obv=obv
                                    )
        idx = data_o.columns.get_loc('al1')
        data_n = misc.normalizedf(data_o,s=idx)
        plots.showplots(df1=data_n,caller='stream',F=F,obv=obv,refresh=refresh)        

    print('- rolling backtest complete...')

    return data_n


def stream_e(data,harms,F,mode,refresh,obv=['v','c'],diff_offset=1,diff=1,m=1,N=7):
    # At the start it is assumed that 
    # N days have already been processed
    data_s = data[:N].copy()

    for t in range(N,len(data)):
        try:
            print(f'\n- Processing Frame #{t}: start:{min(data_s.index)} end:{max(data_s.index)}\n')
        except KeyboardInterrupt:
            break

        data_n = misc.normalizedf(data_s)

        data_p = mod.point_sys( data=data_n
                                ,size=3
                                )
        data_c  = freq.complex_coords(data_p,x=[data_p.dv1dt1nm,data_p.dc1dt1nm])
        data_m  = mod.ddm(  data=data_c
                            )
        data_o = nl.dual_oscillator(data=data_m
                                    ,m=m
                                    ,obv=obv
                                    ,F=F
                                    )
        plots.showplots(df1=data_o,caller='stream',F=F,obv=obv,refresh=refresh)  

        data_s = data_o.append(data.iloc[t])        

    print('- expanding backtest complete...')

    return data_s
   
def dump(data,F,refresh,m=1,obv=['v','c'],diff_offset=1,diff=1):
    data_p = mod.point_sys( data=data
                            ,size=3
                            )
    data_m  = mod.ddm(  data=data_p
                        )
    data_n = misc.normalizedf(data_m)

    data_c  = freq.complex_coords(data_n,x=[data_n.x1nm,data_n.x2nm])
    data_o = nl.dual_oscillator(data=data_c
                                ,m=m
                                ,obv=obv
                                ,F=F
                                )
    idx = data_o.columns.get_loc('al1')
    data_n = misc.normalizedf(data_o,s=idx)
    plots.showplots(df1=data_n,caller='dump',F=F,obv=obv,refresh=refresh) 

    print('- Dump Complete...')
    breakpoint()
    return data_n