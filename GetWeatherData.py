from ratelimit import limits, sleep_and_retry
import requests
import json
from GetData import GetData



# Get the weather data from data api 
class GetWeatherData(GetData):
    TIME_PERIOD = 30
    CALLS = 25

    def __init__(self, CACHE_FNAME):
        super().__init__(CACHE_FNAME)


    def create_request_url(self, start_date):
        """
        This function prepares and returns the request url for the API call.
        It takes in the FIXFIXFIX
        The the API query website is FIX
        """
        
        location = "Cupertino"
        tp = "24" # default daily weather
    
        params = f"?q={location}&date={start_date}&key={self.WEATHER_API_KEY}&tp={tp}&format=json"
        url = "https://api.worldweatheronline.com/premium/v1/past-weather.ashx" + params
        return url


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
            content = json.loads(r.text)
            cache_dict[datetime] = int(content["data"]["weather"][0]["avgtempC"])
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
            url = self.create_request_url(datetime)

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



    # def cache_or_fetch(cache_dict, CACHE_FNAME, datetime, url):
    #     ''' determine whether to fetch the data from API or use the cached content
    #     '''

    #     global counter

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


# if __name__ == "__main__":
#     Weather = GetWeatherData("test_cache_weather")
#     Weather.get_data_with_caching()