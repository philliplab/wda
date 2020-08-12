import numpy as np
import pandas as pd
import load_data
import matplotlib.pyplot as plt
plt.show()

dat = load_data.load_station()
# %matplotlib inline

pdat = pd.pivot_table(
        dat.loc[(slice(None), np.arange(1920, 2021), slice(None), 'TMAX'), 
          ('value',)], 
  values = 'value', 
  index = ['year', 'month'], 
  aggfunc = 'mean')

pdat.unstack('year').plot()

pdat = pd.pivot_table(
        dat.loc[(slice(None), np.arange(1920, 2021), slice(None), 'TMAX'), 
          ('value',)], 
  values = 'value', 
  index = ['year', 'month'], 
  aggfunc = 'mean')

#plt.plot(
