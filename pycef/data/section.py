# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 10:56:22 2013

@author: laegrim
"""

import datetime
import logging
import logging.config
from dateutil.relativedelta import *
import sys
import numpy

def segment_by_date(data, start_date, end_date, segment_size):
    
    '''
    Funtion takes data as a list of dictionary objects, each of which 
    must contain a 'date' key formatted as datetime:
    
        [{
        date:datetime
        }]
        
    Funtion returns a list of lists of dictionaries, with each inner list 
    containing a segment of the original data dictionaries spanning 
    segment_size.  In total the segments will span from 
    start_date to end_date, with an inocmplete section if the segments
    do not evenly divide the date range
    
    segment_size should be a dateutil.relativedelta object
    start_date and end_date should be datetime objects
    '''
    
    date = start_date
    date_segments = []
    
    #date_ranges is a list of tuples defining the segments
    while date < end_date:
        
        temp_date = date + segment_size
        date_ranges.append((date, temp_date))
        date = temp_date
        
    #segment the data into date ranges
    for date_range in date_ranges:
    
        range_data = []
        
        #for each dictionary in the data list
        for chunk in data:
            #if the data date falls into the current date segment
            if date_range[0] > datetime.datetime.strptime(data['date'],
                                 '%Y%m%d').date() >= date_range[1]:
                    #append the data to the current segment
                    range_data.append(chunk)
                    #and take the data out of the original structure
                    data.pop(data.index(chunk))
        
        #add the current segment to the 
        data_segments.append(range_data)
        
    return data_segments
    
    
            
    
    
    
    
    