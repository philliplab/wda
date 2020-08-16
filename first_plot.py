import numpy as np
import pandas as pd
import load_data
from plotnine import ggplot, geom_point, aes, stat_smooth, facet_wrap, geom_line
import plotnine as gg
from IPython import get_ipython
ipython = get_ipython()
ipython.magic('matplotlib')
#%matplotlib 

dat = load_data.load_station()
dat.reset_index(inplace = True)
dat['decade'] = (dat['year'] // 10) * 10

# Plotting the monthly avg TMAX per decade

decade_means = dat.query('metric == "TMAX" and decade > 1900 and decade < 2020').groupby(['decade', 'month'])['value'].aggregate(['mean']).reset_index()
decade_means.rename(columns = {'mean' : 'mean_tmax'}, inplace = True)

decade_means.columns = ['decade', 'month', 'mean_tmax']
decade_means['decade'] = ['{}-{}'.format(i, i+9) for i in decade_means['decade']]
decade_means['decade'] = decade_means['decade'].astype('category')

months_labels = [i.strftime('%b') for i in pd.date_range(start = '2010-01-01', 
    periods = 12, freq = 'M')]

(ggplot(decade_means, aes(x = 'month', y = 'mean_tmax', color = 'decade', group = 'decade'))
  + geom_line()
  + gg.labs(x = 'Month',
            y = 'Average of Daily Max Temp',
            color = 'Decade')
  + gg.scales.scale_x_continuous(breaks = list(range(1, 13)),
      labels = months_labels)
  + gg.theme(subplots_adjust={'right': 0.75}))

# Plot the deviation in the decade average monthly TMAX from the alltime monthly TMAX

overall_means = dat.query('metric == "TMAX" and decade > 1900 and decade < 2020').groupby(['month'])['value'].aggregate(['mean']).reset_index()
overall_means.columns = ['month', 'mean_tmax']

decade_deviations = decade_means.set_index(['decade', 'month']) - overall_means.set_index(['month'])
decade_deviations.reset_index(inplace = True)

(ggplot(decade_deviations, aes(x = 'month', y = 'mean_tmax', color = 'decade', group = 'decade'))
  + geom_line()
  + gg.labs(x = 'Month',
            y = 'Deviation of Decade Average\nfrom All-time average',
            color = 'Decade')
  + gg.scales.scale_x_continuous(breaks = list(range(1, 13)),
      labels = months_labels)
  + gg.theme(subplots_adjust={'right': 0.75}))

# Highlight last two decades

latest_decades = decade_deviations.query('decade == "2000-2009" or decade == "2010-2019"').copy()
latest_decades['decade'] = latest_decades['decade'].cat.remove_unused_categories()

(ggplot(decade_deviations, aes(x = 'month', y = 'mean_tmax', group = 'decade'))
  + geom_line(color = 'gray')
  + geom_line(latest_decades, 
      aes(x = 'month', y = 'mean_tmax', color = 'decade', group = 'decade'))
  + gg.labs(x = 'Month',
            y = 'Deviation of Decade Average\nfrom All-time average',
            color = 'Decade')
  + gg.scales.scale_x_continuous(breaks = list(range(1, 13)),
      labels = months_labels)
  + gg.theme(subplots_adjust={'right': 0.75}))


