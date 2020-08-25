def check_station(dat, metric, start_date = None, end_date = None, grouping_level = 'month'):
    '''Counts the amount of missing data points.

    Check how many data points are missing in each calendar month and checks for each day of the year, how many years are missing data for that day.
    '''

    if False:
        import pandas as pd
        import numpy as np
        import load_data
        dat = load_data.load_station()
        metric = 'TMAX'
        start_date = None
        end_date = None
        grouping_level = 'year'
        grouping_level = 'month'

    if grouping_level == 'month':
        group_by_list = ['station', 'year', 'month']
        grouper_freq = 'M'
    elif grouping_level == 'year':
        group_by_list = ['station', 'year']
        grouper_freq = 'Y'

    counts = dat. \
        query('metric == "TMAX"'). \
        groupby(group_by_list) \
        ['value']. \
        aggregate('count')
    counts.reset_index(level = 0, 
                         drop = True, 
                         inplace = True)

    _, min_year, min_month, min_day, _ = dat.index[0]
    _, max_year, max_month, max_day, _ = dat.index[-1]

    first_day = pd.Timestamp(
        year = min_year,
        month = min_month,
        day = min_day)
    last_day = pd.Timestamp(
        year = max_year,
        month = max_month,
        day = max_day)
    all_days_indx = pd.date_range(start = first_day,
        end = last_day,
        freq = 'D')
    all_days = pd.Series(np.ones((len(all_days_indx),)),
            index = all_days_indx)
    days = all_days. \
            groupby(pd.Grouper(freq=grouper_freq)). \
            aggregate('count')

    if grouping_level == 'month':
        days_indx = pd.MultiIndex.from_arrays([
                days.index.get_level_values(0).year,
                days.index.get_level_values(0).month], 
            names = group_by_list[1:])
    else:
        days_indx = pd.Index(
                days.index.get_level_values(0), 
            name = group_by_list[-1])
    days = pd.Series(days.values, 
        index = days_indx,
        name = 'perfect')
    missing = (days - counts)
    missing[missing.isna()] = days[missing.isna()]
    missing.name = 'days_missing'

def plot_missing(missing):
    if False:
        import plotnine as gg
        from IPython import get_ipython
        ipython = get_ipython()
        ipython.magic('matplotlib')

    missing = missing.reset_index()
    if 'month' in missing.columns:
        time_col = 'Year.Month'
        missing[time_col] = [i+j/12.0 for i, j in zip(missing['year'],  missing['month'])]
    else:
        time_col = 'year'
    (gg.ggplot(missing, gg.aes(x = time_col, y = 'days_missing')) +
        gg.geom_point())
