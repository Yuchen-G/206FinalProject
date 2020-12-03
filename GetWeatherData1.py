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
counter = 0
# Get the weather data from data api 
weather_api_key = "9c9aed8125084cfaaa073014200312"
weather_api_key_1 = "55d80763931641b2b5e73127200312"


def check_progress(CACHE_FNAME):
    ''' check how much data has already been stored in the json file '''

    try:
        cache_dict = Cache.read_cache(CACHE_FNAME)
        cache_list = sorted(cache_dict.items(),
                            key=lambda x: x[0], reverse=True)
        return cache_list[0][0]
    except:
        print("=============\nfirst time running\n=============")
        return "2020-05-01"


def create_request_url(start_date):
    """
    This function prepares and returns the request url for the API call.
    It takes in the FIXFIXFIX
    The the API query website is FIX
    """
    
    location = "Cupertino"
    tp = "24" # default daily weather
   
    params = f"?q={location}&date={start_date}&key={weather_api_key}&tp={tp}&format=json"
    url = "https://api.worldweatheronline.com/premium/v1/past-weather.ashx" + params
    return url


@sleep_and_retry
@limits(calls=25, period=30)
def fetch_data(cache_dict, CACHE_FNAME, datetime, url):
    ''' fetch data from API
    '''

    global counter
    # counter 
    counter += 1
    print('# of calls made == ' + str(counter))

    r = requests.get(url)
    print(f"Fetching data for {datetime}")

    try:
        # ---> will need to update the erro message, ticker especially when changing the company
        if r.text == "":    # --> update
            print("DATA NOT AVAILABLE\n--------------")
            return None
        else:
            content = json.loads(r.text)
            cache_dict[datetime] = content["data"]["weather"][0]["avgtempC"]
            Cache.write_cache(CACHE_FNAME, cache_dict)
            print("Data fetched\n--------------")
    except:
        print('Error when requesting url\n--------------')
        return None


def cache_or_fetch(cache_dict, CACHE_FNAME, datetime, url):
    ''' determine whether to fetch the data from API or use the cached content
    '''

    global counter

    # Using cached content
    for date in cache_dict:
        if datetime == date:
            print(f"Using cache for {datetime}\n--------------")
            return datetime

    # Fetching data from API
    fetch_data(cache_dict, CACHE_FNAME, datetime, url)


def get_data_with_caching(CACHE_FNAME):
    """get stock price data from the api with caching
    """

    global counter
    # get the datetime that needs to be fetched from API or cached file
    last_date = check_progress(CACHE_FNAME)
    dates = get_date(CACHE_FNAME)

    if last_date == "2020-05-01":
        dates = dates
    else:
        for i in range(len(dates)):
            if dates[i] == last_date:
                dates = dates[i+1:]
                break

    for datetime in dates:
        if counter == 25:
            print("=============\nEnd of runing\n=============")
            return

        cache_dict = Cache.read_cache(CACHE_FNAME)
        url = create_request_url(datetime)  # this line different from getstockdata

        # fetch data when no cache is available
        if len(cache_dict) == 0:
            fetch_data(cache_dict, CACHE_FNAME, datetime, url)

        # determine whether to use cache or fetch
        else:
            cache_or_fetch(cache_dict, CACHE_FNAME, datetime, url)


def get_date(CACHE_FNAME):
    """
    get the date for the url
    """

    dates = []
    # -->update   "5": "31", "6": "30", "7": "31", "8": "31"
    timedict = {"5": "31", "7": "31"}

    # create a list containing all the dates
    for month in timedict:
        for day in range(1, int(timedict[month])+1):
            if day < 10:
                dates.append("2020-"+"0"+month+"-0"+str(day))
            else:
                dates.append("2020-"+"0"+month+"-"+str(day))
    return dates


if __name__ == "__main__":
    # setup for testing, needs to be removed after finished
    CACHE_FNAME = "cache_weather"
    cache_dict = Cache.read_cache(CACHE_FNAME)
    url = create_request_url('2020-05-01')

    # print(create_request_url("2020-05-01")
    # fetch_data(cache_dict, CACHE_FNAME, "2020-05-01", url)
    get_data_with_caching(CACHE_FNAME)