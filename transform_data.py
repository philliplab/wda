#TODO Next up: make the first_day and last_day actually also apply to dat in check_station


import pandas as pd
import numpy as np
import load_data


def check_station(dat, metric, first_day = None, last_day = None, grouping_level = 'month'):
    '''Counts the amount of missing data points.

    Check how many data points are missing in each calendar month and checks for each day of the year, how many years are missing data for that day.
    '''

    if False:
        dat = load_data.load_station()
        metric = 'TMAX'
        last_day = None
        first_day = None
        first_day = '1900-01-01'
        last_day = '2019-12-31'
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
    counts.reset_index(level = 0, # Drop station level from index
                       drop = True, 
                       inplace = True)

    _, min_year, min_month, min_day, _ = dat.index[0]
    _, max_year, max_month, max_day, _ = dat.index[-1]

    x = pd.Timestamp(2010,10,2)

    if first_day is not None:
        first_day = pd.Timestamp(first_day)
    else:
        first_day = pd.Timestamp(year = min_year, 
                                 month = min_month, 
                                 day = min_day)
    
    if last_day is not None:
        last_day = pd.Timestamp(last_day)
    else:
        last_day = pd.Timestamp(year = max_year, 
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
    counts = counts.reindex_like(days)
    missing = (days - counts)
    missing[missing.isna()] = days[missing.isna()]
    missing.name = 'days_missing'
    return missing

def check_list_of_stations(stations = ['USW00024127', 'USW00014943', 'USW00014922', 'USW00014735', 'USW00013722', 'USW00027502', 'USW00014839', 'USW00094823', 'USW00014933', 'USW00014820', 'USW00014837', 'USW00093817', 'USW00013957', 'USW00093819', 'USW00013994', 'USW00024028', 'USW00013723', 'USW00024128', 'USW00014764', 'USW00014914', 'USW00023066', 'USW00014929', 'USW00014739', 'USW00014733', 'USW00023065', 'USW00094849', 'USW00013891', 'USW00014925', 'USW00014768', 'USW00013966', 'USW00014734', 'USW00013880', 'USW00024018', 'USW00014944', 'USW00026617', 'USW00014848', 'USW00094014', 'USW00093820', 'USW00014840', 'USW00024157', 'USW00014898', 'USW00014936', 'USW00093822'][:10]):
    station = 'USW00014735'
    results = {}
    for station in stations:
        dat = load_data.load_station(station = station)
        results[station] = check_station(dat, first_day = '1900-01-01', last_day = '2019-12-31', metric = 'TMAX')
        print(station)
        print(results[station])
    pd.concat(results) # axis = 1 puts the station names as column names
        




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
