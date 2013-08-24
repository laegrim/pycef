# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 10:59:01 2013

@author: laegrim
"""

from pymongo import MongoClient
import pymongo

client = MongoClient()
cef_db = client['CEFS']
coll = cef_db['CEF_Info']
for cef in coll.find():
    dist_freq = 'Missing'
    tax_category = 'Missing'
    for historical_item in cef['history']:
        if dist_freq == 'Missing' and historical_item.has_key('dist_freq'):
            dist_freq = historical_item['dist_freq']
        if tax_category == 'Missing' and historical_item.has_key('category'):
            tax_category = historical_item['category']
        historical_item.pop('dist_freq', '')
        historical_item.pop('category', '')
    cef['dist_freq'] = dist_freq
    cef['tax_classification'] = tax_category
    coll.save(cef)