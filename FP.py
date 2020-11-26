from os import name
import requests
import json
import urllib.request
import urllib.parse
import urllib.error
import os

# Get the stock price data from twelve data api
STOCK_API_KEY = 'e94271ad5ef44b5bb5d4bfda57f7188b'




def read_cache(CACHE_FNAME):
    """
    This function reads from the JSON cache file and returns a dictionary from the cache data.
    If the file doesn’t exist, it returns an empty dictionary.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    CACHE_FILE = dir_path + '/' + CACHE_FNAME + ".json"
    try:
        # Try to read the data from the file
        cache_file = open(CACHE_FILE, 'r', encoding="utf-8")
        cache_contents = cache_file.read()  # If it's there, get it into a string
        # And then load it into a dictionary
        CACHE_DICTION = json.loads(cache_contents)
        # Close the file, we're good, we got the data in a dictionary.
        cache_file.close()
        return CACHE_DICTION
    except:
        CACHE_DICTION = {}
        return CACHE_DICTION


def write_cache(cache_file, cache_dict):
    """
    This function encodes the cache dictionary (CACHE_DICT) into JSON format and
    writes the JSON to the cache file (CACHE_FNAME) to save the search results.
    """
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(cache_file, 'w')
    fw.write(dumped_json_cache)
    fw.close()


def create_request_url():
    """
    
    This function prepares and returns the request url for the API call.
    It takes in the stock ticker, start date, end date, interval, decimal places.
    The documentation of the API parameters is at https://twelvedata.com/docs.

    """
    try:
        ticker = "AAPL"
        interval = "1day"  # 1min, 5min, 15min, 30min, 45min, 1h, 2h, 4h, 1day, 1week, 1month
        start_date = "2020-05-01"
        end_date = "2020-08-01"
        dp = 0  # decimal place, type int

        params = f"?symbol={ticker}&interval={interval}"\
            f"&start_date={start_date}&end_date={end_date}"\
            f"&dp={dp}&apikey={STOCK_API_KEY}"

        url = "https://api.twelvedata.com/time_series" + params
        print(url)
        r = requests.get(url)
        return url
    except:
        print("error when requesting url")


def get_data_with_caching(CACHE_FNAME):
    """get stock price data from the api with caching
    """
    url = create_request_url()
    r = requests.get(url)
    dict = json.loads(r.text)


if __name__ == "__main__":
    # define cache file name
    dir_path = os.path.dirname(os.path.realpath(__file__))
    CACHE_FNAME = dir_path + '/' + "cache_stock.json"
    get_data_with_caching(CACHE_FNAME)
    # create_request_url()