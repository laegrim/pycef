# -*- coding: utf-8 -*-
"""
Created on Mon May 20 16:28:05 2013

@author: laegrim
"""

import requests
import re
from BeautifulSoup import BeautifulSoup
import multiprocessing
import logging
import logging.config
import datetime
from pycef.lib.conf.constants import LOG_CONF_LOC
from pycef.lib.mongo.mongo_interface import Mongo

logging.config.fileConfig(LOG_CONF_LOC)
START_LOGGER = logging.getLogger('scrape.scrape_cefs')

print "START_LOGGER"

try:
    BATCH_SIZE = multiprocessing.cpu_count()
except NotImplementedError:
    START_LOGGER.exception('multiprocessing.cpu_count() not implemented')
    BATCH_SIZE = 4


class CEFInfo(object):
    '''Bundle methods for grabbing current CEF information from cefconnect.com
    '''
    
    def __init__(self, ticker_db, ticker_col, cef_db, cef_col):
                
        #self.logger = logging.getLogger('scrape.scrape_cefs.CEFInfo')
        print "scrape.scrape_cefs.CEFInfo"
        self.critical_logger = logging.getLogger(
                                        'scrape.scrape_cefs.CEFInfo.critical')
        self.compare_list = None
        self.ticker_db = ticker_db
        self.ticker_col = ticker_col
        self.cef_db = cef_db
        self.cef_col = cef_col
        self.interface = None
    
    def get_tickers(self):
        ''' CEFInfo.get_tickers()
            Gets current list of tickers from mongodb database
            Returns bool
        '''
    
        try:
            with Mongo() as self.interface:
                self.compare_list = self.interface.pull_from_mongo(
                                            {'_id':'ticker_list'}, 
                                            self.ticker_db, 
                                            self.ticker_col
                                            )
                self.compare_list = self.compare_list['list']  
                return True
        except AttributeError:
            #self.logger.exception('get_tickers')
            self.critical_logger.critical('get_tickers failed')
            return False    
        
    def get_info(self):
        ''' CEFInfo.get_info
            Starts threads to get relevant information from cefconnect
            Calls scrape_info(<args_list>)
            Returns bool
        '''
            
        #self.logger.debug('starting pool') 

        try:                 
            pool = multiprocessing.Pool(BATCH_SIZE)
        except AttributeError:
            #self.logger.exception('get_info: error starting pool')
            self.critical_logger.critical('get_info failed')

                
        args_dict = {
                        'compare_list' : self.compare_list,
                        'db' : self.cef_db,
                        'col' : self.cef_col,
                    }
                        
        try:
            results = pool.map_async(scrape_info, 
                                  [[i, args_dict] for i in range(BATCH_SIZE)]
                                  )
        except AttributeError:
            #self.logger.exception('get_info: error map_async')
            self.critical_logger.critical('get_info failed')

                                        
        results.wait()
        results = results.get()
                    
        pool.close()
        pool.join()
            
        #self.logger.debug('pool joined')

        flag = False
        for result in results:
            if result[0] == False:
#                self.logger.info(
#                                    'get_info: ' + \
#                                    'Unable to get info from ' + \
#                                    str(result[1])
#                                )
                flag = True
        if flag == True:
            return False
                
        return True
                
def scrape_info(args_list):
    '''actually grab information from cefconnect
    '''
    
    logger = logging.getLogger('scrape.scrape_info')
    critical_logger = logging.getLogger('scrape.scrape_info.critical')
    rank = args_list[0]
    args_dict = args_list[1]
    i = rank
    compare_list = args_dict['compare_list']
    db = args_dict['db']
    col = args_dict['col']
    url_stub = 'http://www.cefconnect.com/Details/Summary.aspx?ticker='   
    error_list = []
    no_errors = True
                
    while i < len(compare_list):
            
        try:
            
            ticker = str(compare_list[i])
            page = requests.get(url_stub + ticker, timeout=60.00)
            contents = page.content
            
            # Grab the history of the current ticker             
            with Mongo() as interface:
                ticker_info = interface.pull_from_mongo({'_id': ticker},
                                                        db, 
                                                        col
                                                        )            
            # Grab the latest update time, if it exists
            if ticker_info == None:
                stored_date = None
                ticker_info = {'_id': ticker,
                               'history':[]
                               }
            else:
                stored_date = ticker_info['history'][0]['date']
                            
            # Error check for empty request           
            if contents == None:
                no_errors = False
                error_list.append(ticker)
                i += BATCH_SIZE
                continue
                                            
            soup = BeautifulSoup(contents)
                
            # Error check for empty soup object 
            if soup == None:
                no_errors = False
                error_list.append(ticker)
                i += BATCH_SIZE
                continue
                            
            # Find the latest date for information in the soup 
            date = soup.find(id=re.compile('AsOfLabel'))
                
            # If a date couldn't be found, soup is probably bad 
            if date == None:
                no_errors = False
                error_list.append(ticker)
                i += BATCH_SIZE
                continue
            
            # Parse to get a datetime object from raw soup 
            date = date.text.split(' ')
            date = [d.strip('-,.abcdefghijklmnopqrstuvwxyz' + \
                            'ABCDEFGHIJKLMNOPQRSTUVWXYZ') for d in date]
                
            date = date[2].split('/')
            date = datetime.date(int(date[2]), int(date[0]), int(date[1]))
            date = datetime.date.strftime(date, '%Y%m%d')
            
            # If the latest data is already in the database, no need to update 
            if date <= stored_date:
                i += BATCH_SIZE
                continue
            
            # Parse soup for more numeric info 
            table = soup.find(id=re.compile('SummaryGrid')).findChildren()
            
            # If table couldn't be found, soup probably contaminated 
            if table == None:
                no_errors = False
                error_list.append(ticker)
                i += BATCH_SIZE
                continue
            
            text = [row.text.strip('$%') for row in table]
            nums = []
            
            # Grab floats from soup 
            for number in text:
                try:
                    nums.append(float(number))
                except Exception:
                    continue
            
            # If all of the data isn't there, it's probably contaminated
            if len(nums) != 12:
                no_errors = False
                error_list.append(ticker)
                i += BATCH_SIZE
                continue
            
            curr_nav = nums[0]
            curr_price = nums[1]
            curr_dis = nums[2]

            _52_wk_avg_price = nums[3]
            _52_wk_avg_nav = nums[4]
            _52_wk_avg_dis = nums[5]
            
            _52_wk_high_price = nums[6]
            _52_wk_high_nav = nums[7]
            _52_wk_high_dis = nums[8]
            
            _52_wk_low_price = nums[9]
            _52_wk_low_nav = nums[10]
            _52_wk_low_dis = nums[11]
            
            # Parse soup for distribution info 
            
            table = soup.find(id=re.compile('DistrDetails')).findChildren()
            
            # If table couldn't be found, soup probably contaminated 
            if table == None:
                no_errors = False
                error_list.append(ticker)
                i += BATCH_SIZE
                continue            
                        
            text = [row.text for row in table]
            text = text[2::3]
            
            # If all of the data isn't there, it's probably contaminated,
            # This information isn't vital though, so safe to insert missing 
            if len(text) != 3:
                dist = 'Missing'
                dist_ammt = 'Missing'
                dist_freq = 'Missing'
            else:
                dist = text[0]
                dist_ammt = text[1]
                dist_freq = text[2]
            
            # Parse soup for basic fund information 
            
            table = soup.find(id=re.compile('FundBasics')).findChildren()
            
            # If table couldn't be found, soup probably contaminated 
            if table == None:
                no_errors = False
                error_list.append(ticker)
                i += BATCH_SIZE
                continue     
            
            text = []
            for row in table:
                if row.text == 'Total Net Assets:':
                    text.append(table[table.index(row) + 1].text)
                elif row.text == 'Total Common Assets:':
                    text.append(table[table.index(row) + 1].text)
                elif row.text == 'Common Shares Outstanding:':    
                    text.append(table[table.index(row) + 1].text)
                    
            # If all of the data isn't there, it's probably contaminated,
            # This information isn't vital though, so safe to insert missing 
            if len(text) != 3:
                ttl_net_ast = 'Missing'
                ttl_cmm_ast = 'Missing'
                cmm_shr_out = 'Missing'
            else:
                ttl_net_ast = text[0]
                ttl_cmm_ast = text[1]
                cmm_shr_out = text[2]
                
            category = soup.find('td', attrs={'class':'tabs', 'align':'left'}, 
                                 text='Category:').findNext(
                                 ).text.encode('ascii', 'ignore')
                                 
            if category == None:
                category = 'Missing'
            
            # Ready the data structure for mongo update 
            curr_hist = {
            'date': date,
            'curr_nav': curr_nav,
            'curr_price': curr_price,
            'curr_dis': curr_dis,
            '_52_wk_avg_price': _52_wk_avg_price,
            '_52_wk_avg_nav': _52_wk_avg_nav,
            '_52_wk_avg_dis': _52_wk_avg_dis,
            '_52_wk_high_price': _52_wk_high_price,
            '_52_wk_high_nav': _52_wk_high_nav,
            '_52_wk_high_dis': _52_wk_high_dis,
            '_52_wk_low_price': _52_wk_low_price,
            '_52_wk_low_nav': _52_wk_low_nav,
            '_52_wk_low_dis': _52_wk_low_dis,
            'dist': dist,
            'dist_ammt': dist_ammt,
            'dist_freq': dist_freq,
            'ttl_net_ast': ttl_net_ast,
            'ttl_cmm_ast': ttl_cmm_ast,
            'cmm_shr_out': cmm_shr_out,
            'category': category
            }
                        
            ticker_info['history'].insert(0, curr_hist) 
            
            # push to Mongo
            with Mongo() as interface:
                ticker_info = interface.push_to_mongo(ticker_info,
                                                      db, col, {'_id': ticker})

            i += BATCH_SIZE
            
        except Exception:
            no_errors = False
            logger.exception( "Rank " + str(rank) + ": Ticker " + ticker)
            #"Traceback: " + str(traceback.extract_tb(sys.exc_info()[2])) + \
            #'\n' 
            error_list.append(ticker)
            i += BATCH_SIZE

    return [no_errors, error_list]
        
