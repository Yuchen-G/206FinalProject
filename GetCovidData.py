from ratelimit import limits, sleep_and_retry
import requests
import json
from GetData import GetData


class GetCovidData(GetData):
    TIME_PERIOD = 30
    CALLS = 25

    def __init__(self, CACHE_FNAME):
        super().__init__(CACHE_FNAME)

    def create_request_url(self, start_date):
        """
        This function prepares and returns the request url for the API call.
        """

        'https://api.covidtracking.com/v1/us/20200501.json'
        date = start_date.replace('-', '')

        params = f"{date}.json"
        url = "https://api.covidtracking.com/v1/us/" + params
        return url

    @sleep_and_retry
    @limits(calls=CALLS, period=TIME_PERIOD)
    def fetch_data(self, cache_dict, datetime, url):
        ''' fetch data from API'''

        # counter
        self.counter += 1
        print('# of calls made == ' + str(self.counter))

        r = requests.get(url)
        print(f"Fetching data for {datetime}")

        try:
            # ---> will need to update the erro message, ticker especially when changing the company
            content = json.loads(r.text)
            cache_dict[datetime] = {'deathIncrease': content["deathIncrease"],
                                    "hospitalizedIncrease": content["hospitalizedIncrease"], "positiveIncrease": content["positiveIncrease"]}
            self.Cache.write_cache(self.CACHE_FNAME, cache_dict)
            print("Data fetched\n--------------")
        except:
            print('Error when requesting url\n--------------')
            return None

    def get_data_with_caching(self):
        """get stock price data from the api with caching"""

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


# if __name__ == "__main__":
#     Covid = GetCovidData("test_cache_Covid")
#     Covid.get_data_with_caching()