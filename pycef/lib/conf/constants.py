# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 13:51:06 2013

@author: laegrim
"""

LOG_DICT = {
    'version' : 1,
    'loggers' : {
        'root' : {
            'level' : 'DEBUG',
            'handlers' : ['rotatingFile', 'email'],
            'propagate' : '0'
            },
        'scrape' : {
            'level' : 'DEBUG',
            'handlers' : ['console', 'rotatingFile', 'email'],
            'propagate' : '0'
            },
        'send_mail' : {
            'level' : 'DEBUG',
            'handlers' : ['console', 'rotatingFile', 'email'],
            'propagate' : '0'
            },
        'send_mail.GenerateAttachment' : {
            'level' : 'DEBUG',
            'handlers' : ['console', 'rotatingFile', 'email'],
            'propagate' : '0'
            },
        'scrape.mongo_interface.mongoWrapper' : {
            'level' : 'DEBUG',
            'handlers' : ['console', 'rotatingFile', 'email'],
            'propagate' : '0'
            },
        'scrape.scrape_cefs' : {
            'level' : 'DEBUG',
            'handlers' : ['console', 'rotatingFile'],
            'propagate' : '0'
            },
        'scrape.scrape_cefs.CEFInfo' : {
            'level' : 'DEBUG',
            'handlers' : ['console', 'rotatingFile'],
            'propagate' : '0'
            },
        'scrape.scrape_cefs.CEFInfo.critical' : {
            'level' : 'CRITICAL',
            'handlers' : ['console', 'rotatingFile', 'email'],
            'propagate' : '0'
            },
        'scrape.scrape_info' : {
            'level' : 'DEBUG',
            'handlers' : ['console', 'rotatingFile'],
            'propagate' : '0'
            },
        'scrape.scrape_info.critical' : {
            'level' : 'CRITICAL',
            'handlers' : ['console', 'rotatingFile', 'email'],
            'propagate' : '0'
            },
        'scrape.scrape_tickers': {
            'level' : 'DEBUG',
            'handlers' : ['console', 'rotatingFile', 'email'],
            'propagate' : '0'
            }
        },
    'handlers' : {
        'console' : {
            'class' : 'logging.StreamHandler',
            'level' : 'DEBUG',
            'formatter' : 'standard',
            'stream' : 'ext://sys.stdout'
            },
        'rotatingFile' : {
            'class' : 'logging.handlers.RotatingFileHandler',
            'level' : 'DEBUG',
            'formatter' : 'standard',
            'filename' : 'log.txt',
            'mode' : 'a',
            'maxBytes' : '1000000',
            'backupCount' : '5'
            },
        'email' : {
            'class' : 'logging.handlers.SMTPHandler',
            'level' : 'WARN',
            'formatter' : 'standard',
            'mailhost' : 'localhost',
            'fromaddr' : 'cefserver@laegrim.com',
            'toaddrs' : ['steich@gmail.com'],
            'subject' : 'CEF log'
            }
        },
    'formatters' : {
        'standard' : {
            'format' : '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt' : '%Y-%m-%d %H:%M:%S'
            }
        }
    }