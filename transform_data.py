def check_station(dat, metric, start_date = None, end_date = None):
    '''Counts the amount of missing data points.

    Check how many data points are missing in each calendar month and checks for each day of the year, how many years are missing data for that day.
    '''

    if False:
        import load_data
        dat = load_data.load_station()
        metric = 'TMAX'
        start_date = None
        end_date = None
    m_counts = dat.query('metric == "TMAX"').groupby(['station', 'year', 'month'])['value'].aggregate('count')
    m_counts.reset_index(level = 0, drop = True, inplace = True)

    _, min_year, min_month, min_day, _ = dat.index[0]
    _, max_year, max_month, max_day, _ = dat.index[-1]

    all_days = pd.date_range(start = pd.Timestamp(
            year = min_year,
            month = min_month,
            day = min_day),
        end = pd.Timestamp(
            year = max_year,
            month = max_month,
            day = max_day),
        freq = 'D')
    m_no_missing_counts = pd.Series(np.ones((len(all_days),)),
            index = all_days)
    g = m_no_missing_counts.groupby(pd.Grouper(freq='M')).aggregate('count')


    g2_index = pd.MultiIndex.from_arrays([
            g.index.get_level_values(0).year,
            g.index.get_level_values(0).month], 
        names = ['year', 'month'])
    g2 = pd.Series(g.values, 
        index = g2_index,
        name = 'perfect')
    per_month_missing = g2 - m_counts
    

