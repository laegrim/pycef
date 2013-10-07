'''
Functions provide basic (fundamental) analysis
'''

def best_fit_slopes_compare(list_1, list_2):
    '''
    Comparison function for slopes of best fit lines over a series of points
    Best fit is first degree polynomial
    '''
    
    #find the slope of the best fit lines for each series of points
    slope_1 = np.polyfit(range(len(list_1)), list_1, 1)[0]
    slope_2 = np.polyfit(range(len(list_2)), list_2, 1)[0]
    #return positive ordering if slope 1 is greater
    if slope_1 > slope_2:
        return 1
    #return negative ordering if slope 2 is greater
    elif slope_1 < slope_2:
        return -1
    #slopes are the same, return neutral ordering
    else:
        return 0
        
def best_fit_line_points(series):
    '''
    Return series of best fit line points for a series of points
    Best fit is first degree polynomial
    '''
    
    #find the line of best fit
    fit = np.polyfit(range(len(series)), series, 1)
    #return a series of points along that line
    return [((fit[0] * i) + fit[1]) for i in range(len(series))]

def exp_mov_avg(series, duration, alpha = None):
    '''
    Return the exponential moving average over a series
    S(1) = Y(1)
    for t > 1, S(t) = alpha * Y(t) + (1 - alpha) * S(t-1)
    If an alpha is not given, alpha defaults to (2.0/(duration + 1))
    '''
    
    #check to see if default alpha is used
    if alpha == None:
        alpha = (2.0/(duration + 1))
        
    #base case    
    if duration == len(series):
        return series[duration - 1]
    
    #recursively calculate the sum
    else:
        return ((alpha * series[duration]) + ((1 - alpha) * exp_mov_avg(series,
                 duration - 1)))

def simple_moving_avgs(series, duration):
    '''
    Returns the simple moving averages over a given duration for a given series
    of points
    '''
    
    #find the number of moving averages in the given series
    num_moving_avgs = len(series) - duration + 1
    avgs = []

    #ensure basic level of correctness
    assert num_moving_avgs > 0
    
    #calculate the moving averages
    for i in range(num_moving_avgs):
        total = 0
        for j in range(duration):
            total += series[i + j]
        avgs.append(total / duration)

    return avgs
    
def exp_mov_avgs(series, duration):
    '''
    Returns the exponential moving averages over a given duration for a given 
    series of points
    '''

    #find the number of moving averages in the given series
    num_moving_avgs = len(series) - duration + 1
    avgs = []

    #ensure basic level of correctness
    assert num_moving_avgs > 0
    
    #calculate the moving averages using pre-defined exponential moving 
    #averages function on subseries
    for i in range(num_moving_avgs):
        avgs.append(exp_mov_avg([series[i] for i in range(i, duration + i)], 
                                 duration))
    return avgs