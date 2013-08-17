# -*- coding: utf-8 -*-
"""
Created on Thurs July 11 11:16:38 2013

@author: laegrim
"""

import logging
import logging.config
import re
from configobj import ConfigObj
from pycef.lib.mongo.mongo_interface import Mongo
from pycef.lib.conf.constants import LOG_DICT


logging.config.dictConfig(LOG_DICT)

class ExportCSV(object):
    ''' Class ExportCSV handles the grabbing and bundling of db 
        information into a .csv file format
    '''
    
    def __init__(self, conf_loc):
        self.conf = ConfigObj(conf_loc)
        self.logger = logging.getLogger('send_mail.GenerateAttachment')
        self.parse_dict = self.conf['send_options']
        self.options_list = None
        self.db_list = None
        self.info_list = []
        self.formatted_lines = []
        
    def parse_config(self):
        ''' GenerateAttachment.parse_config()
            function to grab relevant information from database
        '''
        
        try:
            if self.parse_dict['range'] == 'ALL':
                self.options_list = ['ALL']
            else:
                self.options_list = [int(self.parse_dict['range'])]
        except ValueError:
            self.logger.exception('incorrect value stored in ''range''')
            return False
        except KeyError:
            self.logger.exception(
                        'options list or parse dict doesn''t have value')
            return False
        finally:
            self.parse_dict.pop('range')
            
        for item in self.parse_dict:
            if self.parse_dict[item] == 'True':
                self.options_list.append(item)

    def grab_info(self, db, col):
        ''' GenerateAttachment.grab_info(db, col)
            function to grab relevant information from database
        '''
        
        #mongo_interface.find_from_mongo() returns a list of query matches
        with Mongo() as mongo_interface:
            self.db_list = mongo_interface.find_from_mongo(None, 
                                                             db,
                                                             col)
                                                             
        self.logger.debug(len(self.db_list))                         
                                                             
        if self.db_list == None:
            self.logger.error('mongo db find operation returned Nothing')
            
        if self.options_list[0] == 'ALL':
            for ticker in self.db_list:
                ticker_list = [ticker['_id']]
                for days_values in ticker['history']:
                    day_info = []
                    try:
                        day_info.append(days_values['date'])
                        day_info.append(days_values['curr_price'])
                        day_info.append(days_values['curr_dis'])
                        day_info.append(days_values['curr_nav'])
                        for option in self.options_list[1:]:
                            day_info.append(days_values[option])
                    except KeyError:
                        self.logger.exception(
                                    'days_values does not have value')
                    ticker_list.append(day_info)
                self.info_list.append(ticker_list)
        else:
            for ticker in self.db_list:
                ticker_list = [ticker['_id']]
                num_days = self.options_list[0]
                for days_values in ticker['history'][:num_days]:
                    day_info = []
                    try:
                        day_info.append(days_values['date'])
                        day_info.append(days_values['curr_price'])
                        day_info.append(days_values['curr_dis'])
                        day_info.append(days_values['curr_nav'])
                        for option in self.options_list[1:]:
                            day_info.append(days_values[option])
                    except KeyError:
                        self.logger.exception(
                                'days_values does not have value')
                    ticker_list.append(day_info)
                self.info_list.append(ticker_list)
    
    def format_info(self):
        ''' GenerateAttachment.format_info()
            function to format information grabbed from databse
        '''
        
        
        for ticker in self.info_list:
            for day in ticker[1:]:
                day = [re.sub('[$,%;&]', '', str(val)) for val in day]
                self.formatted_lines.append(ticker[0] + "," + \
                                    ",".join([val for val in day]) + \
                                    "\n")
                                    
        self.options_list[0] = '_id'
        self.options_list.insert(1, 'date')
        self.options_list.insert(2, 'curr_price')
        self.options_list.insert(3, 'curr_dis')
        self.options_list.insert(4, 'curr_nav')
        self.formatted_lines.insert(0, ",".join(self.options_list) + "\n")

    def write_info(self, output_file_loc):
        ''' GenerateAttachment.write_info(db, col)
            function to write information to a file
        '''
        try:
            with open(output_file_loc, 'w') as out_file:
                out_file.writelines(self.formatted_lines)
        except IOError:
            self.logger.exception('could not open file')
            return False
        