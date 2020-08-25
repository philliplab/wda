def check_station(dat, metric, start_date = None, end_date = None):
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

    m_counts = dat. \
        query('metric == "TMAX"'). \
        groupby(['station', 'year', 'month']) \
        ['value']. \
        aggregate('count')
    m_counts.reset_index(level = 0, 
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
    days_pm = all_days. \
            groupby(pd.Grouper(freq='M')). \
            aggregate('count')

    days_pm_indx = pd.MultiIndex.from_arrays([
            days_pm.index.get_level_values(0).year,
            days_pm.index.get_level_values(0).month], 
        names = ['year', 'month'])
    days_pm = pd.Series(days_pm.values, 
        index = days_pm_indx,
        name = 'perfect')
    missing_pm = (days_pm - m_counts).fillna(0)

