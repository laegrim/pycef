# -*- coding: utf-8 -*-
"""
Created on Mon May 20 16:28:05 2013

@author: laegrim
"""

import logging
import logging.config
import pycef.lib.scrape.scrape_cefs as scrape_cefs
import pycef.lib.scrape.scrape_tickers as scrape_tickers
from pycef.lib.conf.constants import LOG_DICT

logging.config.dictConfig(LOG_DICT)

class Scrape(object):
    '''Simple script tying together everything else
    '''
    
    def __init__(self):
        self.logger = logging.getLogger('scrape')
        self.ticker_get = None
        self.cef_get = None
        self.scrape_tickers_script()
        self.scrape_cefs_script()
        
    def scrape_tickers_script(self):
        ''' Scrape.scrape_tickers_script()
            simple function to actually put everything together
        '''
        
        self.ticker_get = scrape_tickers.TickerGet('Tickers', 'Ticker_list')
        
        if not self.ticker_get.get_tickers():
            self.logger.critical('self.ticker_get.get_tickers() failed')
        elif not self.ticker_get.compare_tickers():
            self.logger.critical('self.ticker_get.compare_tickers() failed')
            
        #self.logger.debug(self.ticker_get.get_tickers())
        #self.logger.debug(self.ticker_get.compare_tickers())
        
    def scrape_cefs_script(self):
        ''' Scrape.scrape_cefs_script()
            simple function to actually put everything together
        '''
        
        self.cef_get = scrape_cefs.CEFInfo('Tickers', 'Ticker_list', 'CEFS',
                                           'CEF_Info')
                        
        if not self.cef_get.get_tickers():
            self.logger.critical('self.cef_get.get_tickers() failed')
        elif not self.cef_get.get_info():
            self.logger.warning('self.cef_get.get_info() failed')
            
        #self.logger.debug(self.cef_get.get_tickers())
        #self.logger.debug(self.cef_get.get_info())    
    
if __name__ == '__main__':
    
    SCRAPER = Scrape()
    SCRAPER = None
    
    
    
