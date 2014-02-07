'''
Functions provide basic (fundamental) analysis
'''

import numpy as np

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

def exp_mov_avg(series, alpha = None, S1 = None):
    '''
    -Series is an array of numerical values.
    -Alpha is a constant weighting coeficient, and the 
    higher alpha, the more biased the EXP will be towards
    values in low indices. If no alpha is given, alpha defaults to 
    (2/len(series) + 1).
    -S1 is the value of the base case.  This value is always mathematically 
    undefined, so there is always error introduced.  If no S1 is given, 
    S1 defaults to series[0].

    Returns the exponential moving average over a series
    S(1) = S1
    for t > 1, S(t) = alpha * Y(t - 1) + (1 - alpha) * S(t - 1)
    '''

    #check to see if default alpha is used
    if alpha == None:
        alpha = (2.0/(len(series) + 1))

    #check to see if the base case is defined
    if S1 == None:
        S1 == series[0]

    #Base Case
    if len(series) == 1:
        
        #print statement is just interesting to watch sometimes
        #print ('S(1) = ' + str(series[0]))    
        return series[0]
        
    #t > 1
    else:
        
        #print statement is just interesting to watch sometimes
        print ('S(' + str(len(series)) + ') = ' + \
        str(alpha) + ' * (' + str(series[len(series) - 2]) + \
        ') + (' + str(1 - alpha) + ' + S(' + str(len(series) - 1) + '))')
        
        return ((alpha * series[len(series) - 2]) + \
        (1 - alpha)*(alt_exp_mov_avg(series[:len(series) - 1], alpha)))

def alt_exp_mov_avg(series, alpha = None, S1 = None):
    '''
    -Series is an array of numerical values.
    -Alpha is a constant weighting coeficient, and the 
    higher alpha, the more biased the EXP will be towards
    values in low indices. If no alpha is given, 
    alpha defaults to (2/len(series) + 1).
    -S1 is the value of the base case.  This value is always mathematically 
    undefined, so there is always error introduced.  If no S1 is given, 
    S1 defaults to series[0].

    Returns the exponential moving average over a series
    S(0) = S(series[0]) = Y(series[0]) = Y(0), and
    for t > 0, S(t) = alpha * Y(t) + (1 - alpha) * S(t - 1)
    '''

    #check to see if default alpha is used
    if alpha == None:
        alpha = (2.0/(len(series) + 1))

    #check to see if the base case is defined
    if S1 == None:
        S1 == series[0]

    #Base Case
    if len(series) == 1:
        
        #print statement is just interesting to watch sometimes
        #print ('S(1) = ' + str(series[0]))    
        return series[0]
        
    #t > 1
    else:
        
        #print statement is just interesting to watch sometimes
        print ('S(' + str(len(series)) + ') = ' + \
        str(alpha) + ' * (' + str(series[len(series) - 1]) + \
        ') + (' + str(1 - alpha) + ' + S(' + str(len(series) - 1) + '))')
        
        return ((alpha * series[len(series) - 1]) + \
        (1 - alpha)*(alt_exp_mov_avg(series[:len(series) - 1], alpha)))

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
    
def exp_mov_avgs(series, section_len, alpha = None, S1 = None):
    '''
    Returns a time series of exponential moving averages
    
    For a series of length N, returns [EMA(series[0:section_len]), 
    EMA(series[1:section_len + 1]), ....]
    
    '''

    #find the number of moving averages in the given series
    num_moving_avgs = len(series) - section_len + 1
    avgs = []

    #ensure basic level of correctness
    assert num_moving_avgs > 0
    
    #calculate the moving averages using pre-defined exponential moving 
    #averages function on subseries
    for i in range(num_moving_avgs):
        avgs.append(exp_mov_avg(series[i:section_len + i], alpha, S1))
    return avgs
    
    
