CEF-Scraping-Scripts
====================
Scripts require BeautifulSoup, requests, sys, and re

******************************
stockinfo.py
******************************
Currently reads a list of tickers from stocks.csv, scrapes information
from cefconnect.com, and ouputs data on CEFs with discounts to Info.csv.
Log.txt records exceptions and errors.

******************************
tickerget.py
******************************
Currently scrapes wsj.com's list of CEF closing prices to find a current list 
of CEF tickers, and outputs the list to stocks.csv.
Log.txt records exceptions and errors.
