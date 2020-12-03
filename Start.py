from GetStockData import GetStockData 
from GetWeatherData import GetWeatherData
from WriteData import WriteData


if __name__ == "__main__":
    # define variables
    cache1 = "cache_stock"
    cache2 = "cache_weather"
    db_name = "Warehouse"
    tb1_name = "StockData"
    tb2_name = "WeatherData"
    # Get Stock Data
    Stock = GetStockData(cache1)
    Stock.get_data_with_caching()
    # Get Weather Data
    Weather = GetWeatherData(cache2)
    Weather.get_data_with_caching()
    # Write data into database
    writer = WriteData(db_name, tb1_name, tb2_name)
    cur, conn = writer.SetUpDatabase()
    writer.SetUpTable(cache1, cache2, cur, conn)