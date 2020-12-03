from os import name
from typing import Counter
from ratelimit import limits, sleep_and_retry
import requests
import json
import urllib.request
import urllib.parse
import urllib.error
import os
from CacheHelper import CacheHelper

Cache = CacheHelper()
# Get the stock price data from twelve data api
STOCK_API_KEY = 'e94271ad5ef44b5bb5d4bfda57f7188b'
TIME_PERIOD = 60
counter = 0     # counter
api_key = "2e90f725535a45b696f50829eb52fe19"