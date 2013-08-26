# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 10:59:01 2013

@author: laegrim
"""

from pymongo import MongoClient
import pymongo
import requests
from BeautifulSoup import BeautifulSoup
import logging
import re

client = MongoClient()
cef_db = client['CEFS']
coll = cef_db['CEF_Info']
logger = logging.getLogger('reformat_logger')
logger.setLevel(logging.DEBUG)
strmhdlr = logging.StreamHandler()
strmhdlr.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
strmhdlr.setFormatter(formatter)
logger.addHandler(strmhdlr)

reg = re.compile('[1234567890$]')

url_stub = 'http://www.cefconnect.com/Details/Summary.aspx?ticker='   

for cef in coll.find():
    
    dist_freq = 'Missing'
    tax_category = 'Missing'
    
    if cef.has_key('dist_freq') and cef.has_key('tax_classification'):
        try:
            page = requests.get(url_stub + cef['_id'], timeout=60.00)
            contents = page.content
            soup = BeautifulSoup(contents)
            
            tax_category = soup.find('td', attrs={'class':'tabs',
                                                  'align':'left'}, 
                                                  text='Category:').findNext(
                                                  ).text.encode('ascii',
                                                    'ignore')
            table = soup.find(id=re.compile('DistrDetails')).findChildren()
            text = [row.text for row in table]
            text = text[2::3]

            if len(reg.findall(text[2])) == 0:
                dist_freq = text[2]                     
            
            else:
                if len(text) >= 4 and len(reg.findall(text[3])) == 0:
                    dist_freq = text[3]
            
            logger.info('CEF, Tax Category, Dist_Freq : ' + cef['_id'] + ', ' + tax_category + ', ' + dist_freq)
            
        except Exception:
            logger.exception('Did not work for cef: ' + cef['_id'])
    
    else:
        for historical_item in cef['history']:
            if historical_item.has_key('dist_freq'):
                dist_freq = historical_item['dist_freq']
                historical_item.pop('dist_freq', '')
    
            if historical_item.has_key('category'):
                tax_category = historical_item['category']
                historical_item.pop('category', '')
            
        
    cef['dist_freq'] = dist_freq
    cef['tax_classification'] = tax_category
    coll.save(cef)