# -*- coding: utf-8 -*-
"""
Created on Mon May 20 16:28:05 2013

@author: laegrim
"""

import unittest2
import os
import sys
from bson import ObjectId
from pymongo import MongoClient

path = os.path.abspath(os.path.join(os.getcwd(), os.path.pardir)) + \
        '/lib/'
sys.path.append(path)

import mongo_interface

class TestMongoInterface(unittest2.TestCase):
    
    def setUp(self):
        self.db = 'TestDB'
        self.col = 'TestCol'
        self.id = 'ObjectId()'
        self.id = ObjectId()
        self.json = {'_id':self.id, 'feild':'Hi, I\'m a field'}
        
    def test_push_on_no_db(self):
        
        with mongo_interface.Mongo as wrapper:
            
                
        
    def test_pull_on_no_db(self):
        
    def test_dup_push(self):
        
    def test_push(self):
        
    def test_pull(self):
        
    def test_null_pull(self):
        
    def test_less_pull_params(self):
        
    def test_less_push_params(self):

    def test_less_pull_params(self):
        
    def test_wrong_push_params(self):
        
    def test_wrong_pull_params(self):
    
    
    