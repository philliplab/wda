# Script that contains functions for loading NOAA GHCND data files.

import numpy as np
import pandas as pd
import re

def load_station(station = 'USW00026617', data_dir = '/home/phillipl/0_para/3_resources/noaa_ghcnd/ghcnd_all'):
    '''Loads the data for STATION from the file in DATA_DIR

    Assumes the fwf format. Obtained from ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily (ghcnd_all.tar.gz). Data described in: 
    Menne, M.J., I. Durre, R.S. Vose, B.E. Gleason, and T.G. Houston, 2012:  An overview of the Global Historical Climatology Network-Daily Database.  Journal of Atmospheric and Oceanic Technology, 29, 897-910, doi:10.1175/JTECH-D-11-00103.1.

    Note that all the string variables are stored in the index, so .astype('category') is not needed.
    '''
    if False: # Debugging notes
        station = 'USW00026617'
        data_dir = '/home/phillipl/0_para/3_resources/noaa_ghcnd/ghcnd_all'
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

    # converting indexes and formats 
    dat.set_index(['station', 'year', 'month', 'metric'], inplace = True)
    dat.columns = pd.MultiIndex.from_arrays([days_index, repeated_cols_index])
    dat = dat.stack([0])
    dat.index.rename('day', len(dat.index.names)-1, inplace = True)

    # Remove missing values and unused metrics
    dat = dat.query('value != -9999 and metric in ["TMAX", "TMIN", "PRCP", "SNOW", "SNWD"]').reorder_levels(['station', 'year', 'month', 'day', 'metric'])
    # Scale temperatures to whole degree instead of tenth of a degree
    dat.loc[(slice(None), slice(None), slice(None), slice(None), ['TMAX', 'TMIN']), ('value')] /= 10.0

    return dat



