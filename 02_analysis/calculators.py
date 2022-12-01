# Calculation Functions

import numpy as np
import pandas as pd

def temp_r(df,col_temp,col_r,alpha_TC,alpha_TH,TC,TH):
    cond_temps = [df[col_temp] > TH, (df[col_temp] > TC) & (df[col_temp] <= TH), df[col_temp] < TC]
    choice_temps = [alpha_TH*(df[col_temp]-TH)+1,1,alpha_TC*(TC-df[col_temp])+1]
    df[col_r] = np.select(condlist=cond_temps,choicelist=choice_temps,default=np.nan)


