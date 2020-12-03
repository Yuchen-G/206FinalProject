from ratelimit import limits, sleep_and_retry
import requests
import json
from GetData import GetData


# Get the stock price data from twelve data api
class GetStockData(GetData):
    TIME_PERIOD = 60
    CALLS = 8

    def __init__(self, CACHE_FNAME):
        super().__init__(CACHE_FNAME)


    @sleep_and_retry
    @limits(calls=CALLS, period=TIME_PERIOD)
    def fetch_data(self, cache_dict, datetime, url):
        ''' fetch data from API
        '''

        # counter
        self.counter += 1
        print('# of calls made == ' + str(self.counter))

        r = requests.get(url)
        print(f"Fetching data for {datetime}")

        try:
            # ---> will need to update the erro message, ticker especially when changing the company
            if r.text == '''{"code":400,"message":"No data is available on the specified dates. Try setting different start/end dates.","status":"error","meta":{"symbol":"AAPL","interval":"1day","exchange":""}}''':
                print("DATA NOT AVAILABLE\n--------------")
                return None
            else:
                content = json.loads(r.text)
                cache_dict[datetime] = content["values"][0]
                self.Cache.write_cache(self.CACHE_FNAME, cache_dict)
                print("Data fetched\n--------------")
        except:
            print('Error when requesting url\n--------------')
            return None


    def get_data_with_caching(self):
        """get stock price data from the api with caching
        """

        # get the datetime that needs to be fetched from API or cached file
        last_date = self.check_progress()
        dates = self.get_date()

        if last_date == "2020-05-01":
            dates = dates
        else:
            for i in range(len(dates)):
                if dates[i] == last_date:
                    dates = dates[i+1:]
                    break

        for datetime in dates:
            if self.counter == 25:
                print("=============\nEnd of runing\n=============")
                return

            cache_dict = self.Cache.read_cache(self.CACHE_FNAME)
            url = self.create_request_url(datetime, datetime)

            # fetch data when no cache is available
            if len(cache_dict) == 0:
                self.fetch_data(cache_dict, datetime, url)

            # determine whether to use cache or fetch
            else:
                self.cache_or_fetch(cache_dict, datetime, url)


# def check_progress(CACHE_FNAME):
#     ''' check how much data has already been stored in the json file '''

#     try:
#         cache_dict = Cache.read_cache(CACHE_FNAME)
#         cache_list = sorted(cache_dict.items(),
#                             key=lambda x: x[0], reverse=True)
#         return cache_list[0][0]
#     except:
#         print("=============\nfirst time running\n=============")
#         return "2020-05-01"


# def create_request_url(start_date, end_date):
#     """
#     This function prepares and returns the request url for the API call.
#     It takes in the stock ticker, start date, end date, interval, decimal places.
#     The documentation of the API parameters is at https://twelvedata.com/docs.
#     """

#     ticker = "AAPL"
#     interval = "1day"  # 1min, 5min, 15min, 30min, 45min, 1h, 2h, 4h, 1day, 1week, 1month
#     # start_date = "2020-05-01"
#     # end_date = "2020-08-01"
#     dp = 0  # decimal place, type int

#     params = f"?symbol={ticker}&interval={interval}"\
#         f"&start_date={start_date}&end_date={end_date}"\
#         f"&dp={dp}&apikey={STOCK_API_KEY}"

#     url = "https://api.twelvedata.com/time_series" + params
#     # print(url)
#     return url


# def cache_or_fetch(cache_dict, CACHE_FNAME, datetime, url):
#     ''' determine whether to fetch the data from API or use the cached content
#     '''

#     # global counter

#     # Using cached content
#     for date in cache_dict:
#         if datetime == date:
#             print(f"Using cache for {datetime}\n--------------")
#             return datetime

#     # Fetching data from API
#     fetch_data(cache_dict, CACHE_FNAME, datetime, url)


# def get_date(CACHE_FNAME):
#     """
#     get the date for the url
#     """

#     dates = []
#     # -->update   "5": "31", "6": "30", "7": "31", "8": "31"
#     timedict = {"5": "31", "7": "31"}

#     # create a list containing all the dates
#     for month in timedict:
#         for day in range(1, int(timedict[month])+1):
#             if day < 10:
#                 dates.append("2020-"+"0"+month+"-0"+str(day))
#             else:
#                 dates.append("2020-"+"0"+month+"-"+str(day))
#     return dates


# def get_data_with_caching(CACHE_FNAME):
#     """get stock price data from the api with caching
#     """

#     global counter
#     # get the datetime that needs to be fetched from API or cached file
#     last_date = check_progress(CACHE_FNAME)
#     dates = get_date(CACHE_FNAME)

#     if last_date == "2020-05-01":
#         dates = dates
#     else:
#         for i in range(len(dates)):
#             if dates[i] == last_date:
#                 dates = dates[i+1:]
#                 break

#     for datetime in dates:
#         if counter == 25:
#             print("=============\nEnd of runing\n=============")
#             return

#         cache_dict = Cache.read_cache(CACHE_FNAME)
#         url = create_request_url(datetime, datetime)

#         # fetch data when no cache is available
#         if len(cache_dict) == 0:
#             fetch_data(cache_dict, CACHE_FNAME, datetime, url)

#         # determine whether to use cache or fetch
#         else:
#             cache_or_fetch(cache_dict, CACHE_FNAME, datetime, url)



# if __name__ == "__main__":
#     Stock = GetStockData("test_cache_stock")
#     Stock.get_data_with_caching()
    # print(create_request_url("2020-05-02", "2020-07-11"))
    # print(check_progress('cache_stock'))
    # get_date('cache_stock')
