# -*- coding: utf-8 -*-
"""
Created on Mon May 20 16:28:05 2013

@author: laegrim
"""

from pymongo import MongoClient
import pymongo
from pycef.lib.conf.constants import LOG_DICT
import logging
import logging.config


logging.config.dictConfig(LOG_DICT)

class Mongo(object):
    ''' Wrap Mongo interaction in this app for ease of use               
    '''

    def __init__(self):
        self.wrapper = None
            
    def __enter__(self):
        ''' Mongo.__enter__()
            Private function used for setup, required by 'with'  statement  
        '''
    
        class MongoWrapper(object):
            ''' Inner class of Mongo, used for wrapping queries and updates
            '''
        
            def __init__(self):
                self.db = None
                self.col = None
                self.info = None
                self.query_params = None
                self.update_status = None
                self.client = None
                self.query = None
                self.logger = logging.getLogger(
                                'scrape.mongo_interface.mongoWrapper'
                                                )
                self.results_list = []
                self.cursor = None
                    
            def push_to_mongo(self, info, db, col, query_params=None):
                ''' Mongo.MongoWrapper.push_to_mongo(info = <json>, 
                                                     db = <mongo database>
                                                     col = <mongo collection>
                                                     quer_params = <optional
                                                     query parameters>
                                                     )
                    Wrap mongo update function
                    Return update status as integer
                '''
                
                self.db = db
                self.col = col
                self.info = info
                self.query_params = query_params
           
                try:
                    with MongoClient() as self.client:
                        self.db = self.client[self.db]
                        self.col = self.db[self.col]
                        self.update_status = self.col.update(self.query_params,
                                                             self.info,
                                                             True
                                                             )
                    return self.update_status
                        
                except pymongo.errors.ConnectionFailure:
                    self.logger.exception('Connection to mongodb failed')
                except pymongo.errors.OperationFailure:
                    self.logger.exception('Update operation on mongodb failed')
            
            def pull_from_mongo(self, query, db, col):
                ''' Mongo.MongoWrapper.pull_from_mongo(query = <json>,
                                                       db = <mongo database>
                                                       col = <mongo collection>
                                                       )
                    Wrap mongo find_one function   
                    Return a query result as a json document
                '''                 
                
                self.db = db
                self.col = col
                self.query = query
                
                try:
                    with MongoClient() as self.client:
                        self.db = self.client[self.db]
                        self.col = self.db[self.col]
                        self.query = self.col.find_one(self.query)
                    return self.query
                        
                except pymongo.errors.ConnectionFailure:
                    self.logger.exception('Connection to mongodb failed')
                except pymongo.errors.OperationFailure:
                    self.logger.exception('Query operation on mongodb failed')
                    
            def find_from_mongo(self, query, db, col):
                ''' Mongo.MongoWrapper.find_from_mongo(query = <json>,
                                                       db = <mongo database>
                                                       col = <mongo collection>
                                                       )
                    Wrap mongo find function   
                    Return a query result as a json document
                '''
                
                self.db = db
                self.col = col
                self.query = query
                        
                try:
                    with MongoClient() as self.client:
                        self.db = self.client[self.db]
                        self.col = self.db[self.col]
                        self.cursor = self.col.find(self.query)
                        
                except pymongo.errors.ConnectionFailure:
                    self.logger.exception('Connection to mongodb failed')
                except pymongo.errors.OperationFailure:
                    self.logger.exception('Query operation on mongodb failed')
                    
                if self.cursor == None:
                    return None
                    
                for item in self.cursor:
                    self.results_list.append(item)
                    
                return self.results_list

        self.wrapper = MongoWrapper()
        return self.wrapper
         
    def __exit__(self, type_, value_, traceback_):
        ''' Mongo.__exit__(type, value, traceback)
            Private function used for teardown, requuired by 'with' statement
        '''
        
        self.wrapper = None
        
