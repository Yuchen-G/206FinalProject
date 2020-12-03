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
# Get the weather data from data api
Weather_api_key = "9c9aed8125084cfaaa073014200312"

def create_request_url(start_date, end_date):
    """
    This function prepares and returns the request url for the API call.
    It takes in the FIXFIXFIX
    The the API query website is FIX
    """
   
    params = 
    url = "HTTP: http://api.worldweatheronline.com/premium/v1/past-weather.ashx" + params