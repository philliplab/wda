import numpy as np
import pandas as pd
import load_data

import IPython
ipython = IPython.get_ipython()
ipython.magic('matplotlib')

from plotnine import ggplot, geom_point, aes, stat_smooth, facet_wrap, geom_line
import plotnine as gg

save_img = False
out_dir = '/home/phillipl/0_para/1_projects/wda/posts/p011'

station = 'USW00094789' # JFK intl AP at NYC

dat = load_data.load_station(station = station)
dat.reset_index(inplace = True)
dat['decade'] = (dat['year'] // 10) * 10

print(dat)

# Number missing per year
dat.isna().sum(axis=0)

response_distributions = \
(ggplot(dat.query('metric == "TMAX" | metric == "TMIN"'), 
    aes(x = 'value', y = 'stat(count)'))
  + gg.facet_wrap('metric')
  + gg.geom_histogram(bins = 30)
  + gg.labs(x = 'Temperature',
            y = 'Number of Observations'))

response_distributions
if save_img:
    response_distributions.save(out_dir + '/response_distributions.png')

by_year_missing = dat.query('metric in ("TMAX", "TMIN")').groupby(['year', 'metric'])['value'].aggregate(count = ('value', 'count')).reset_index()

# While there are records as early as late 1940s, they are only consistent after 1960

obs_per_year = \
(ggplot(by_year_missing, aes(x = 'year', y = 'count'))
  + geom_point()
 + gg.facet_wrap('metric')
  + gg.labs(x = 'Year',
            y = 'Number of Observations in Year'))

obs_per_year
if save_img:
    obs_per_year.save(out_dir + '/obs_per_year.png')

bla = \
(by_year_missing.query('year < 1961').set_index(['year', 'metric']).unstack('metric')).round(1).to_markdown()
bla.split('\n')

by_year_avg = dat.query('year >= 1960 & year < 2020 & metric in ("TMIN", "TMAX")').groupby(['year', 'metric'])['value'].aggregate(avg = ('value', 'mean')).reset_index()


yearly_avg = \
(ggplot(by_year_avg, aes(x = 'year', y = 'avg', color = 'metric', group = 'metric'))
  + gg.geom_point()
  + gg.geom_smooth(method = 'lm', se = False)
  + gg.theme(subplots_adjust = {'right' : 0.75})
  + gg.labs(color = 'Metric',
            x = 'Year',
            y = 'Average of Metric for the Year'))

yearly_avg
if save_img:
    yearly_avg.save(out_dir + '/yearly_avg.png')


dat = dat.assign(doy = pd.DatetimeIndex([pd.Timestamp(f'{i[0]}-{i[1]}-{i[2]}') for i in zip(dat.year, dat.month, dat.day)]).strftime('%j'))
dat

by_doy_avg = dat.query('year >= 1960 & year < 2020 & metric in ("TMIN", "TMAX")').groupby(['doy', 'metric', 'month'])['value'].aggregate(avg = ('value', 'mean')).reset_index()
by_doy_avg

by_doy_avg['month'] = by_doy_avg.month.astype('category')
months = pd.DataFrame({'doy' : [i*30.4 for i in range(13)]})
months

daily_avgs = \
(ggplot(by_doy_avg, aes(x = 'doy', y = 'avg'))
  + gg.geom_point(aes(color = 'month'))
  + gg.facet_wrap('metric')
  + gg.geom_vline(data = months, mapping = aes(xintercept = 'doy'), color = 'gray')
  + gg.labs(color = 'Month',
            x = 'Day of the Year',
            y = 'Average of Metric for\nthe Day of the Year')
  + gg.theme(axis_text_x = gg.element_blank(),
             axis_ticks_major_x = gg.element_blank()))

daily_avgs
if save_img:
    daily_avgs.save(out_dir + '/daily_avgs.png')

bla = \
pd.DataFrame({'lag':range(1,11),'cor':[round(dat.query('year >= 1960 & year < 2020 & metric in ("TMAX")')['value'].autocorr(i),3) for i in range(1,11)]}).to_markdown()

bla.split('\n')




