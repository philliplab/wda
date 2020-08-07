# Script that contains functions for loading NOAA GHCND data files.

import numpy as np
import pandas as pd
import re

def load_station(station, data_dir = '/home/phillipl/0_para/3_resources/noaa_ghcnd/ghcnd_all'):
    if False: # Debugging notes
        station = 'USW00026617'
    input_file = data_dir + '/' + station + '.dly'
    input_file = re.sub('//', '/', input_file)
    repeated_cols = [('v_'+str(i+1), 
                      'mf_'+str(i+1), 
                      'qf_'+str(i+1), 
                      'sf_'+str(i+1)) for i in range(31)]
    col_names = ['station', 'year', 'month', 'metric'] + \
                [item for t in repeated_cols for item in t]
    repeated_col_widths = [(5,1,1,1) for i in range(31)]
    widths = [11, 4, 2, 4] + [j for k in repeated_col_widths for j in k]
    dat = pd.read_fwf(input_file, 
                      widths = widths,
                      names = col_names,
                      header = None)
    days_index = [k for j in [(i, i, i, i) for i in range(31)] for k in j]
    repeated_cols_index = ['value', 'mflag', 'qflag', 'sflag']*31

    # converting into proper long format
    '''
    dat.set_index(['station', 'year', 'month', 'metric'])
    dat_mi1 = dat.set_index(['station', 'year', 'month', 'metric'])
    dat_mi2 = pd.DataFrame(dat_mi1, columns = [days_index, repeated_cols_index])
    dat_mi3 = dat_mi2.unstack([0,1,2,3])
    dat_mi4 = dat_mi3.reset_index()
    now you can
    dat_mi4.query('metric == "TMAX" and vf == "value"')
    '''

    return dat
