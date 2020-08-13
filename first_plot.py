import numpy as np
import pandas as pd
import load_data
#import matplotlib.pyplot as plt
#plt.show()

from plotnine import ggplot, geom_point, aes, stat_smooth, facet_wrap, geom_line
from plotnine.data import mtcars

(ggplot(mtcars, aes('wt', 'mpg', color='factor(gear)'))
 + geom_point()
 + stat_smooth(method='lm')
 + facet_wrap('~gear'))


dat = load_data.load_station()
%matplotlib 

# plotting by abusing the column headings
#pdat = pd.pivot_table(
#        dat.loc[(slice(None), np.arange(1920, 2021), slice(None), 'TMAX'), 
#          ('value',)], 
#  values = 'value', 
#  index = ['year', 'month'], 
#  aggfunc = 'mean')
#
#pdat.unstack('year').plot()

pdat = pd.pivot_table(
        dat.loc[(slice(None), np.arange(1920, 2021), slice(None), 'TMAX'), 
          ('value',)], 
  values = 'value', 
  index = ['year', 'month'], 
  aggfunc = 'mean')

pdat = pdat.reset_index()

(ggplot(pdat, aes(x = 'month', y = 'value', color = 'factor(year)'))
 + geom_line())
(ggplot(pdat, aes(x = 'month', y = 'value', color = 'year', group = 'year'))
 + geom_line())
#plt.plot(
