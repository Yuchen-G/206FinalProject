from GetStockData import GetStockData
from GetWeatherData import GetWeatherData
from GetCovidData import GetCovidData
from WriteData import WriteData

if __name__ == "__main__":
    # define variables
    cache_stock = "cache_stock"
    cache_weather = "cache_weather"
    cache_Covid = "cache_Covid"
    db_name = "Warehouse"
    tb_stock = "StockData"
    tb_weather = "WeatherData"
    tb_Covid = "CovidData"
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
    writer = WriteData(db_name, tb_stock, tb_weather, tb_Covid)
    cur, conn = writer.SetUpDatabase()
    writer.SetUpTable(cache_stock, cache_weather, cache_Covid, cur, conn)
    # Get the correlation coefficients
    print(writer.correl('temp', 'WeatherData',
                        'closing_price', 'StockData', cur, conn))
    print(writer.correl('deathIncrease', 'CovidData',
                        'closing_price', 'StockData', cur, conn))
    print(writer.correl('positiveIncrease', 'CovidData',
                        'closing_price', 'StockData', cur, conn))
    print(writer.correl('hospitalizedIncrease', 'CovidData',
                        'closing_price', 'StockData', cur, conn))
