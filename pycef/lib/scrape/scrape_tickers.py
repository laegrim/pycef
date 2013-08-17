# -*- coding: utf-8 -*-
"""
Created on Mon May 20 16:28:05 2013

@author: laegrim
"""

import requests
import re
from BeautifulSoup import BeautifulSoup
import logging
import logging.config
from pycef.lib.conf.constants import LOG_DICT
from pycef.lib.mongo.mongo_interface import Mongo

logging.config.dictConfig(LOG_DICT)

class TickerGet(object):
    '''Bundles methods to grab cef tickers from the daily list at the wsj
    '''
    
    def __init__(self, db, collection):
        
        self.logger = logging.getLogger('scrape.scrape_tickers')
        self.compare_list = None
        self.results_list = None
        self.daily_cef_list = None
        self.table_rows = None
        self.url = None
        self.cef_url = None
        self.base_url = None
        self.soup = None
        self.ticker_list = None
        self.href = None
        self.wsj_finance_contents_page = None
        self.cef_soup = None
        self.interface = None
        self.db = db
        self.col = collection
    
    def get_tickers(self, ticker_list = None):
        '''grab the list of ticker from todays wsj page
        '''    
            
        self.ticker_list = ticker_list
        
        if self.ticker_list != None:
            self.results_list = ticker_list
            return True
        
        self.base_url = 'http://online.wsj.com'
        self.url = 'http://online.wsj.com/mdc/page/marketsdata.html' + \
                   '?mod=WSJ_topnav_marketdata_main'
            
        try:
            #Find the daily CEF closing table
            self.wsj_finance_contents_page = requests.get(self.url, 
                                                          timeout=30.00)
            self.soup = BeautifulSoup(self.wsj_finance_contents_page.content)
            self.href = self.soup.find('a', href=re.compile("-CEF.html?"))
                
            if self.href == None:
                raise Exception("Href could not be found")
                        
            #In the daily CEF closing table, seperate out tickers 
            #self.cef_url = self.base_url + self.href.attrs[0][1]
            self.cef_url = self.href.attrs[0][1]
                   
            self.daily_cef_list = requests.get(self.cef_url, timeout=30.00)
            self.cef_soup = BeautifulSoup(self.daily_cef_list.content)
            self.table_rows = self.cef_soup.findAll('a', 
                                                    href=re.compile("symbol=")
                                                    )
                
            if self.table_rows == []:
                raise Exception("TableRows could not be found")          
            
            #results_list will carry the data for later comparison 
            self.results_list = [row.text for row in self.table_rows]
            return True
                        
        except Exception:
            self.logger.exception('get_tickers: ')
            return False            
    
    def compare_tickers(self): 
        '''Compare scraped tickers to tickers in memory, and add any new ones
        '''
                
        try:
            with Mongo() as self.interface:
                self.compare_list = self.interface.pull_from_mongo(
                                                        {'_id': 'ticker_list'},
                                                        self.db, 
                                                        self.col
                                                        )
      
                                                                    
                if self.compare_list == None:
                    self.compare_list = self.results_list
                    
                    self.interface.push_to_mongo({'_id': 'ticker_list', 
                                                'list' : self.compare_list},
                                                self.db, 
                                                self.col,
                                                {'_id': 'ticker_list'}
                                                )
                                                
                else:
                    for ticker in self.results_list:
                        if self.compare_list['list'].count(ticker) == 0:
                            self.compare_list['list'].append(ticker)
                            self.logger.info(
                                            "ticker_list update: " + \
                                            str(ticker) + '\n'
                                            )
                        
                    self.interface.push_to_mongo(
                                        {'_id': 'ticker_list', 
                                        'list' : self.compare_list['list']},
                                        self.db, 
                                        self.col,
                                        {'_id': 'ticker_list'}
                                        )
                return True
                
        except Exception:
            self.logger.exception('compare_tickers: ')
            return False
