from CacheHelper import CacheHelper
from ratelimit import limits, sleep_and_retry
import requests
import json


class GetData:

    def __init__(self, CACHE_FNAME):
        # Name of the Cache file
        self.CACHE_FNAME = CACHE_FNAME
        # Get the stock price data from twelve data api
        # self.STOCK_API_KEY = 'e94271ad5ef44b5bb5d4bfda57f7188b' # twelvedata
        # self.STOCK_API_KEY = 'CILI5QD4WNMUADKC' # alpha vantage
        self.STOCK_API_KEY = '77a7c7e8c70508d00d41bac85b5107cf'
        self.STOCK_TIME_PERIOD = 60

        # Get the weather data from worldweatheronline api
        self.WEATHER_API_KEY = "9c9aed8125084cfaaa073014200312"
        self.WEATHER_API_KEY_1 = "55d80763931641b2b5e73127200312"
        self.WEATHER_TIME_PERIOD = 30
        # counter
        self.counter = 0
        self.Cache = CacheHelper()

    def check_progress(self):
        ''' check how much data has already been stored in the json file '''

        try:
            cache_dict = self.Cache.read_cache(self.CACHE_FNAME)
            cache_list = sorted(cache_dict.items(),
                                key=lambda x: x[0], reverse=True)
            return cache_list[0][0]
        except:
            print("=============\nfirst time running\n=============")
            return "2020-05-01"

    def create_request_url(self, start_date, end_date):
        """
        This function prepares and returns the request url for the API call.
        It takes in the stock ticker, start date, end date, interval, decimal places.
        The documentation of the API parameters is at https://marketstack.com/
        """

        ticker = "AAPL"
        interval = "1day"  # 1min, 5min, 15min, 30min, 45min, 1h, 2h, 4h, 1day, 1week, 1month
        # start_date = "2020-05-01"
        # end_date = "2020-08-01"
        dp = 2  # decimal place, type int

        params = f"access_key={self.STOCK_API_KEY}&symbols={ticker}&date_from={start_date}&date_to={end_date}"

        url = "http://api.marketstack.com/v1/eod?" + params
        print(url)
        return url

    # @sleep_and_retry
    # @limits(calls=8, period= 60)
    # def fetch_data(self, cache_dict, datetime, url):
    #     ''' fetch data from API
    #     '''

    #     # global counter
    #     # counter
    #     self.counter += 1
    #     print('# of calls made == ' + str(self.counter))

    #     r = requests.get(url)
    #     print(f"Fetching data for {datetime}")

    #     try:
    #         # ---> will need to update the erro message, ticker especially when changing the company
    #         if r.text == '''{"code":400,"message":"No data is available on the specified dates. Try setting different start/end dates.","status":"error","meta":{"symbol":"AAPL","interval":"1day","exchange":""}}''':
    #             print("DATA NOT AVAILABLE\n--------------")
    #             return None
    #         else:
    #             content = json.loads(r.text)
    #             cache_dict[datetime] = content["values"][0]
    #             self.Cache.write_cache(self.CACHE_FNAME, cache_dict)
    #             print("Data fetched\n--------------")
    #     except:
    #         print('Error when requesting url\n--------------')
    #         return None

    def cache_or_fetch(self, cache_dict, datetime, url):
        ''' determine whether to fetch the data from API or use the cached content
        '''

        # Using cached content
        for date in cache_dict:
            if datetime == date:
                print(f"Using cache for {datetime}\n--------------")
                return datetime

        # Fetching data from API
        self.fetch_data(cache_dict, datetime, url)

    def get_date(self):
        """
        get the date for the url
        """

        self.dates = []
        # -->update   "5": "31", "6": "30", "7": "31", "8": "31"
        self.timedict = {"5": "31", "6": "30", "7": "31", "8": "31"}

        # create a list containing all the dates
        for month in self.timedict:
            for day in range(1, int(self.timedict[month])+1):
                if day < 10:
                    self.dates.append("2020-"+"0"+month+"-0"+str(day))
                else:
                    self.dates.append("2020-"+"0"+month+"-"+str(day))
        return self.dates

    # def get_data_with_caching(self):
    #     """get stock price data from the api with caching
    #     """

    #     # global counter
    #     # get the datetime that needs to be fetched from API or cached file
    #     last_date = self.check_progress()
    #     dates = self.get_date()

    #     if last_date == "2020-05-01":
    #         dates = dates
    #     else:
    #         for i in range(len(dates)):
    #             if dates[i] == last_date:
    #                 dates = dates[i+1:]
    #                 break

    #     for datetime in dates:
    #         if self.counter == 25:
    #             print("=============\nEnd of runing\n=============")
    #             return

    #         cache_dict = self.Cache.read_cache(self.CACHE_FNAME)
    #         url = self.create_request_url(datetime, datetime)

    #         # fetch data when no cache is available
    #         if len(cache_dict) == 0:
    #             self.fetch_data(cache_dict, datetime, url)

    #         # determine whether to use cache or fetch
    #         else:
    #             self.cache_or_fetch(cache_dict, datetime, url)


if __name__ == "__main__":
    stock = GetData("test_cache_stock")
    stock.create_request_url('2020-05-01','2020-05-02')
    # stock.get_data_with_caching()
