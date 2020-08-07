# Script that contains functions for loading NOAA GHCND data files.

import numpy as np
import pandas as pd
import re

def load_station(station, data_dir = '/home/phillipl/0_para/3_resources/noaa_ghcnd/ghcnd_all'):
    if False: # Debugging notes
        station = 'USW00026617'
    input_file = data_dir + '/' + station + '.dly'
    input_file = re.sub('//', '/', input_file)
    col_names = ['station'] + \
                [item for t in [('v_'+str(i+1), 'f_'+str(i+1)) for i in range(31)] 
                      for item in t]
    dat = pd.read_table(input_file, 
                        sep = '\s+',
                        header = None,
                        names = col_names)
    return dat
