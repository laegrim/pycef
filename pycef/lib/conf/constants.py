# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 13:51:06 2013

@author: laegrim
"""
import os
print "In constants.py"

CONF_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_CONF_LOC = os.path.dirname(os.path.abspath(__file__)) + '/logging.conf'
SCRAPE_CONF_LOC = os.path.dirname(os.path.abspath(__file__)) + '/scrape.conf'

print 'CONF_DIR'
print 'LOG_CONF_LOC'
print 'SCRAPE_CONF_LOC'