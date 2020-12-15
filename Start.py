from GetStockData import GetStockData
from GetWeatherData import GetWeatherData
from GetCovidData import GetCovidData
from WriteData import WriteData
from CacheHelper import CacheHelper

Cache = CacheHelper()
'''
This file runs the entire code by calling other classes. 
It will output the calculation(four correlation coefficients) into 'output.txt' 
and print four graphs after 5 executions.  
'''

if __name__ == "__main__":
    # define variables
    cache_stock = "cache_stock"
    cache_weather = "cache_weather"
    cache_Covid = "cache_Covid"
    db_name = "Warehouse"
    tb_stock = "StockData"
    tb_weather = "WeatherData"
    tb_Covid = "CovidData"
    tb_Covid1 = "CovidData1"
    # Get Stock Data
    Stock = GetStockData(cache_stock)
    Stock.get_data_with_caching()
    # Get Weather Data
    Weather = GetWeatherData(cache_weather)
    Weather.get_data_with_caching()
    # Get Covid Data
    Covid = GetCovidData(cache_Covid)
    Covid.get_data_with_caching()
    # Write data into database
    writer = WriteData(db_name, tb_stock, tb_weather, tb_Covid, tb_Covid1)
    cur, conn = writer.SetUpDatabase()
    writer.SetUpTable(cache_stock, cache_weather, cache_Covid, cur, conn)
    # Get the correlation coefficients
    stock_dic = Cache.read_cache(cache_stock)
    if stock_dic.get('2020-09-25', 0) != 0:
        # Correlation Coefficient 0
        correl0 = writer.correl('temp', 'WeatherData',
                                'closing_price', 'StockData', cur, conn)
        str0 = "Correlation coefficient between temperature and Apple's stock price is " + \
            str(correl0)
        writer.write_correl('output.txt', str0)
        # Correlation Coefficient 1
        correl1 = writer.correl(
            'positiveIncrease', 'CovidData', 'closing_price', 'StockData', cur, conn)
        str1 = "Correlation coefficient between daily positive cases and Apple's stock price is " + \
            str(correl1)
        writer.write_correl('output.txt', str1)
        # Correlation Coefficient 2
        correl2 = writer.correl(
            'deathIncrease', 'CovidData', 'closing_price', 'StockData', cur, conn)
        str2 = "Correlation coefficient between daily death cases and Apple's stock price is " + \
            str(correl2)
        writer.write_correl('output.txt', str2)
        # Correlation Coefficient 3
        correl3 = writer.correl(
            'hospitalizedIncrease', 'CovidData', 'closing_price', 'StockData', cur, conn)
        str3 = "Correlation coefficient between daily hospitalized cases and Apple's stock price is " + \
            str(correl3)
        writer.write_correl('output.txt', str3)
        # Visualization
        writer.viz('temp', 'weatherData',
                    'closing_price', 'StockData', cur, conn, 'Daily Temperature',
                    "Apple stock's closing price", '''Daily Temperature vs. Apple Stock's Closing Price''')
        writer.viz('positiveIncrease', 'CovidData',
                   'closing_price', 'StockData', cur, conn, 'Daily Covid Positive Increase',
                   "Apple stock's closing price", '''Daily Covid Positive Increase vs. Apple Stock's Closing Price''')
        writer.viz('deathIncrease', 'CovidData',
                   'closing_price', 'StockData', cur, conn, 'Daily Covid Death Increase',
                   "Apple stock's closing price", '''Daily Covid Death Increase vs. Apple Stock's Closing Price''')
        writer.viz('hospitalizedIncrease', 'CovidData',
                   'closing_price', 'StockData', cur, conn, 'Daily Covid Hospitalized Increase',
                   "Apple stock's closing price", '''Daily Covid Hospitalized Increase vs. Apple Stock's Closing Price''')
