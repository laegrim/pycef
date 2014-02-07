# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 09:38:23 2013

@author: laegrim

Trading algorithms and associated functions that rely on analysis of 
associativity graphs
"""
import datetime
from dateutil.relativedelta import relativedelta
#import pycef
#from pycef.lib.mining.graph import build_graph
#import pycef.lib.analytics.fundamentals as fund
import numpy as np

def update_graph_lazy(graph_args):
    '''
    simply return the passed graph
    '''
    return graph_args[0]


def simple_rising_values(graph, data, day):
    '''
    Rising values for a node are calculated by the sum of the
    average gain of the neighbors of that node
    '''
    
    #store data here to be returned
    rising_values  = {}
    
    #current day
    day = datetime.datetime.strptime(day, '%Y%m%d')
    #print "Calculating Rising Valuse For Date: " + str(day)
    
    #day before
    day_before = day + relativedelta(days=-1)
    
    #for node in the graph
    for node in graph:
        
        neighbor_gains = []
        
        #for each node find neighbors for calculations
        for neighbor in graph.neighbors(node):
                       
            #find the current price of the neighbor
            curr_val = [date['curr_price'] for date in [
                cef for cef in data if cef['_id'] == neighbor][0]['history'] 
                if date['date'] == day.strftime('%Y%m%d')]
                                
            #make sure that there is a price for this day
            if curr_val == []:
                #if not, it's a holliday or a weekend
                return None
                
            #pop out of the list
            curr_val = curr_val[0]
            
            #find the previous price of the neighbor
            prev_val = [date['curr_price'] for date in 
                [cef for cef in data if cef['_id'] == neighbor][0]['history']
                if date['date'] == day_before.strftime('%Y%m%d')]
            
            #Go to last day before current day in which there is data
            #Corrects for situations in which the last day of trading was
            #More than one day ago (weekends, holidays, etc...)
            while prev_val == []:
                
                prev_val = [date['curr_price'] for date in 
                [cef for cef in data if cef['_id'] == neighbor][0]['history']
                if date['date'] == day_before.strftime('%Y%m%d')]
                    
                day_before += relativedelta(days=-1)
            
            #pop prev_val out of the list
            prev_val = prev_val[0]
               
            #compute the weighted gain
            neighbor_gains.append((curr_val / prev_val))
            
        #use the average of each neighbors weighted gains as the rising value
        rising_values[node] = (sum(neighbor_gains)/
                                len(neighbor_gains))
        
    return rising_values
    
def weighted_rising_values(graph, data, day):
    '''
    Rising values for a node are calculated by the sum of the
    average gain of the neighbors of that node
    '''
    
    #store data here to be returned
    rising_values  = {}
    
    #current day
    day = datetime.datetime.strptime(day, '%Y%m%d')
    #print "Calculating Rising Valuse For Date: " + str(day)
    
    #day before
    day_before = day + relativedelta(days=-1)
    
    #for node in the graph
    for node in graph:
        
        neighbor_weighted_gains = []
        
        #for each node find neighbors for calculations
        for neighbor in graph.neighbors(node):
            
            #find the weight of the edges between each node, neighbor pair
            #edge_weight = graph.edge[node][neighbor]['weight']
            
            #find the current price of the neighbor
            curr_val = [date['curr_price'] for date in [
                cef for cef in data if cef['_id'] == neighbor][0]['history'] 
                if date['date'] == day.strftime('%Y%m%d')]
                                
            #make sure that there is a price for this day
            if curr_val == []:
                #if not, it's a holliday or a weekend
                return None
                
            #pop out of the list
            curr_val = curr_val[0]
            
            #find the previous price of the neighbor
            prev_val = [date['curr_price'] for date in 
                [cef for cef in data if cef['_id'] == neighbor][0]['history']
                if date['date'] == day_before.strftime('%Y%m%d')]
            
            #Go to last day before current day in which there is data
            #Corrects for situations in which the last day of trading was
            #More than one day ago (weekends, holidays, etc...)
            while prev_val == []:
                
                prev_val = [date['curr_price'] for date in 
                [cef for cef in data if cef['_id'] == neighbor][0]['history']
                if date['date'] == day_before.strftime('%Y%m%d')]
                    
                day_before += relativedelta(days=-1)
            
            #pop prev_val out of the list
            prev_val = prev_val[0]
               
            #compute the weighted gain
            gain = (curr_val / prev_val)
            diff = 1 - graph.edge[node][neighbor]['weight']
            if gain <= 0:
                diff = -diff
            else:
                weighted_gain = (1 + (.1 - diff)) * gain
                
            neighbor_weighted_gains.append((curr_val / prev_val))
            
        #use the average of each neighbors weighted gains as the rising value
        rising_values[node] = (sum(neighbor_weighted_gains)/
                                len(neighbor_weighted_gains))
        
    return rising_values

def weighted_rising_values_relative(graph, data, day):
    '''
    Rising values for a node are calculated by the sum of the
    average gain of the neighbors of that node
    '''
    
    #store data here to be returned
    rising_values  = {}
    
    #current day
    day = datetime.datetime.strptime(day, '%Y%m%d')
    #print "Calculating Rising Valuse For Date: " + str(day)
    
    #day before
    day_before = day + relativedelta(days=-1)
    
    #for node in the graph
    for node in graph:
        
        neighbor_weighted_gains = []
        
        #for each node find neighbors for calculations
        for neighbor in graph.neighbors(node):
            
            #find the weight of the edges between each node, neighbor pair
            #edge_weight = graph.edge[node][neighbor]['weight']
            
            #find the current price of the neighbor
            curr_val = [date['curr_price'] for date in [
                cef for cef in data if cef['_id'] == neighbor][0]['history'] 
                if date['date'] == day.strftime('%Y%m%d')]
                                
            #make sure that there is a price for this day
            if curr_val == []:
                #if not, it's a holliday or a weekend
                return None
                
            #pop out of the list
            curr_val = curr_val[0]
            
            #find the previous price of the neighbor
            prev_val = [date['curr_price'] for date in 
                [cef for cef in data if cef['_id'] == neighbor][0]['history']
                if date['date'] == day_before.strftime('%Y%m%d')]
            
            #Go to last day before current day in which there is data
            #Corrects for situations in which the last day of trading was
            #More than one day ago (weekends, holidays, etc...)
            while prev_val == []:
                
                prev_val = [date['curr_price'] for date in 
                [cef for cef in data if cef['_id'] == neighbor][0]['history']
                if date['date'] == day_before.strftime('%Y%m%d')]
                    
                day_before += relativedelta(days=-1)
            
            #pop prev_val out of the list
            prev_val = prev_val[0]
               
            #compute the weighted gain
            neighbor_weighted_gains.append((curr_val / prev_val))
            
        #use the average of each neighbors weighted gains as the rising value
        rising_values[node] = (sum(neighbor_weighted_gains)/
                                len(neighbor_weighted_gains))
        
    return rising_values

def partition_update(partition, rising_values, data, cur_day):
    '''
    Update the position of the current partition
    This version of the function takes cash holdings into account
    '''
    
    #update value proposition of current holdings
    symbol, shares = partition['currentinvestment']
    
    #find the value per share of the current investment
    current_share_price = None
    if symbol == 'cash':
        current_share_price = partition['currentvalue']
    else:
        current_share_price = [day for day in [cef for cef in data
            if cef['_id'] == symbol][0]['history']
            if day['date'] == cur_day][0]['curr_price']
        
    #find the current total value of the pools investment
    partition['currentvalue'] = (current_share_price * shares)
    
    #find the pools current value proposition
    current_value_prop = None
    if symbol == 'cash':
        current_value_prop = 1.0
    else:
        #this should be changed.... doesn't make any sense to reference the 
        #value, only need the probability that value rises or falls.
        #Maybe have a range [-1, 1]?  Warrants future looks.
        current_value_prop = (partition['currentvalue']/
            partition['initialvalue']) * rising_values[symbol]
            
    partition['currentvalueprop'] = current_value_prop
    
    return partition
    
            
def execute_trades_safety_no_tax(partition, pool_partitions, 
                                 data, cur_day, rising_values, 
                                 trade_duration_weight, 
                                 diversity_coeficient):
    '''
    Determine whether to make a trade based on criteria
    This version of the function allows money market holding positions
    '''
    swap = None
    swap_value = None
    swapped = False
    
    #use cash as a baseline investment, always has a value proposition
    #of 1
    if 1.0 > partition['currentvalueprop']:
        
        swap = 'cash'   
        swapped = True                         
    
    #move partition to the largest current position
    for rising_value in rising_values:
        #try to encourage a little diversityb
        number_of_partitions_on_node = len([
            part for part in pool_partitions
            if part['currentinvestment'][0] == rising_value])
        
        swap_value = ((1.0 - number_of_partitions_on_node *
            diversity_coeficient) * trade_duration_weight *
            rising_values[rising_value])                

        if swap_value > partition['currentvalueprop']:
            
            swap = rising_value
            swapped = True
            
    if swap == 'cash':
            
        partition['initialvalue'] = partition['currentvalue']
        partition['currentvalueprop'] = 1.0
        partition['currentinvestment'] = ('cash', 1)
        
    elif swap != None:
        
        partition['initialvalue'] = partition['currentvalue']
            
        current_share_price = [day for day in [cef for cef in data if
            cef['_id'] == swap][0]['history']
            if day['date'] == cur_day][0]['curr_price']
                
        num_shares = partition['currentvalue']/current_share_price
        partition['currentinvestment'] = (swap, num_shares)
            
        print ("Swap Val: " +  str(swap_value) + ", Part Val: " + 
        str(partition['currentvalueprop']))
        
    if swapped == True:    
        
        print ("Partition " + str(pool_partitions.index(partition)) + 
        " swapped to " + str(partition['currentinvestment']))
        
        return partition

def trawl_graph(pool_partitions, start_date, end_date,
                graphing_update_function, graph_args, rising_values_function,
                partition_update_function, execute_trades_function,
                trade_duration_weight, diversity_coeficient, data):
    '''
    Algorithm is designed to make trades by trawling a weighted graph composed
    of value (price, discount, etc...) correlated
    instruments.
    
    With an initial sum of money, partitioned into a set of discrete pools:
    
    for each day of history provided:
        update the graph to reflect current circumstances
        
        for each node in the graph:
            assign a "Rising Value", or a weight loosely reflecting the 
            probability that the node will rise in value, 
            
        for each partition on the pool:
            calculate the current value proposition
            
        for each partition on the pool:
            if partition has fallen below the lower split value (percent of
            it's initial value):
                join the partition to the partition with the highest value
                proposition
            if partition has gone above the upper split value (percent of it's
            initial value):
                split the partition into two smaller paritions, which are then
                moved to the highest value propositions
            if another node has a higher value proposition (weighted against
            multiple partitions on the same node, sorted list by highest
            value propositions):
                sell current holdings and move to that node
            
                
    takes as arguments:
        list of pools (the sum of which is the total initial investment)
        start_date (datetime)
        end_date (datetime)
        function to generate the graph
        function to generate the rising value for each node
        trade duration weight (larger values weight towards longer position
            holds, smaller values weight towards shorter position holds)
        diversity coeficient (larger values encourage more diverse positions)
        historical data for each node in the graph
        
        each pool should be a dict:
            {
             initialvalue : , 
             currentvalue : ,
             currentvalueprop : ,
             currentinvestment : (symbol, number_of_shares)
            }
        
        
    '''
    
    total_starting_investment = sum([partition['initialvalue']
                                    for partition in pool_partitions])
                                        
    date_list = []
    delta = end_date - start_date
    
    for day in range(delta.days):
        
        curr_date = start_date + relativedelta(days=day)
        date_list.append(curr_date.strftime('%Y%m%d'))
        
    for cur_day in date_list:
                
        #get the most up to date graph
        graph = graphing_update_function(graph_args)
        
        #grab the value reflecting each nodes likelyhood to rise
        #returns a dictionary of node ids and an associated rising value
        rising_values = rising_values_function(graph, data, cur_day)
        if not rising_values:
            continue
        
        
        #find new partition positions
        for partition in pool_partitions:
            
            partition = partition_update_function(partition, rising_values, 
                                                  cur_day, data)

        #execute trades based on new positions and parameters
        for partition in pool_partitions:
            
            partition = execute_trades_function(partition, pool_partitions,
                                                data,
                                                cur_day, rising_values,
                                                diversity_coeficient,
                                                trade_duration_weight)
                                         
    #Print block of relevant data
    #Total ammount of mony in pool_partitions at end of simulation
    total_ending_investment = sum([partition['initialvalue']
        for partition in pool_partitions])
    
    #Total ending gain(percentage)
    total_ending_gain = total_ending_investment / total_starting_investment
    
    #Number of days tracked in simulation
    history_length = len(data[0]['history'])
    
    daily_prices = [[cef['history'][day]['curr_price'] for cef in data] for
                        day in range(history_length)]
    
    #Starting prices for each tracked instrument
    start_day_prices = [price for price in daily_prices[0]]
    
    #Ending prices for each tracked instrument
    end_day_prices = [price for price in daily_prices[history_length -1]]
            
    #Gain for each tracked instrument
    gains = [start_day_prices[i] / end_day_prices[i] for i in range(len(data))]
    
    #Market Geometric Average Gains
    geo_gain = []
    for day in daily_prices:
        geo_gain.append(pow(np.product(day), 1.0/len(day)))
    
    geo_gain = pow(np.product(geo_gain, 1.0/len(day)))
    
    #Average gain for each tracked instrument
    total_market_gain = sum(gains)/len(data)

    print "Total Starting Investment: " + str(total_starting_investment)
    print "Total Ending Investment: " + str(total_ending_investment)
    print "Total Ending Gain: " + str(total_ending_gain)
    print "Total Market Gain: " + str(total_market_gain)
    print "Percent Over/Under Market Gain: " + str(total_ending_gain - 
            total_market_gain)
    print "Market Geometric Average Gain: " + str(geo_gain)
    print "Ending Positions: " 
    #print position per partition in pool
    for i in range(len(pool_partitions)):
        print ("Partition: " + str(i) + " Symbol: " + 
        pool_partitions[i]['currentinvestment'][0] + 
        ', Shares: ' + str(pool_partitions[i]['currentinvestment'][1]) + 
        ', Value: ' + str(pool_partitions[i]['currentvalue']))
        

                    
                
                
        
            
        
                
            
            
            
            
            
            
        
    
        
    
    