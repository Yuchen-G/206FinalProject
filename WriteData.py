from unittest.main import main
from CacheHelper import CacheHelper
from sqlite3.dbapi2 import SQLITE_SELECT
import unittest
import sqlite3
import json
import os
import numpy as np
import matplotlib.pyplot as plt

class WriteData:
    def __init__(self, db_name, tb_name_1, tb_name_2,tb_name_3):
        self.db_name = db_name
        self.tb_name_1 = tb_name_1
        self.tb_name_2 = tb_name_2
        self.tb_name_3 = tb_name_3
        self.Cache = CacheHelper()

    def SetUpDatabase(self):
        path = os.path.dirname(os.path.abspath(__file__))
        conn = sqlite3.connect(path+'/' + self.db_name + '.db')
        cur = conn.cursor()
        return cur, conn

    def SetUpTable(self, cachefile1, cachefile2, cachefile3, cur, conn):
        # loads the data into dictionaries
        stock_data = self.Cache.read_cache(cachefile1)
        weather_data = self.Cache.read_cache(cachefile2)
        covid_data = self.Cache.read_cache(cachefile3)
        # create database
        # Attention data type is float for closing price
        cur.execute(
            f"CREATE TABLE IF NOT EXISTS {self.tb_name_1} (id TEXT PRIMARY KEY, closing_price REAL)")
        cur.execute(
            f"CREATE TABLE IF NOT EXISTS {self.tb_name_2} (id TEXT PRIMARY KEY, temp INTEGER)")
        cur.execute(
            f"CREATE TABLE IF NOT EXISTS {self.tb_name_3} (id TEXT PRIMARY KEY, deathIncrease INTEGER, hospitalizedIncrease INTEGER, positiveIncrease INTEGER)")
        # use for loop to enter records into table "StockData"
        for item in stock_data:
            id = item
            closing_price = stock_data[item]
            cur.execute(
                f"INSERT OR IGNORE INTO {self.tb_name_1} (id, closing_price) VALUES (?,?)", (id, closing_price))
        # use for loop to enter records into table "WeatherData"
        for item in weather_data:
            id = item
            temp = weather_data[item]
            cur.execute(
                f"INSERT OR IGNORE INTO {self.tb_name_2} (id, temp) VALUES (?,?)", (id, temp))
        # use for loop to enter records into table "CovidData"
        for item in covid_data:
            id = item
            deathIncrease = covid_data[item]["deathIncrease"]
            hospitalizedIncrease = covid_data[item]["hospitalizedIncrease"]
            positiveIncrease = covid_data[item]["positiveIncrease"]
            cur.execute(
                f"INSERT OR IGNORE INTO {self.tb_name_3} (id, deathIncrease, hospitalizedIncrease, positiveIncrease) VALUES (?,?,?,?)", (id, deathIncrease, hospitalizedIncrease, positiveIncrease))
        # handle bad value
        cur.execute('DELETE FROM WeatherData WHERE WeatherData.id IN (SELECT WeatherData.id FROM WeatherData JOIN StockData ON StockData.id = WeatherData.id WHERE StockData.closing_price = -99)')
        cur.execute('DELETE FROM CovidData WHERE CovidData.id IN (SELECT CovidData.id FROM CovidData JOIN StockData ON StockData.id = CovidData.id WHERE StockData.closing_price = -99)')
        cur.execute('DELETE FROM StockData WHERE StockData.closing_price = -99')
        # commit changes
        conn.commit()

    def correl(self, col0, tb0, col1, tb1, cur, conn):
        """
        calculate the correlation coefficient for two datasets in the database
        """

        # x axis is weather info
        cur.execute(f'SELECT {col0} FROM {tb0}')
        x = cur.fetchall()
        # convert x into a normal list
        l0 = list()
        for item in x:
            l0.append(item[0])
        # convert l0 into an np array
        l0 = np.array(l0)

        # y axis is stock price 
        cur.execute(f'SELECT {col1} FROM {tb1}')
        y = cur.fetchall()
        # convert y into a normal list
        l1 = list()
        for item in y:
            l1.append(item[0])
        # convert l1 into an np array
        l1 = np.array(l1)

        conn.commit()
        r = np.corrcoef(l0, l1)
        return r[0,1]

    def viz(self, col0, tb0, col1, tb1, cur, conn):
        # x axis is weather info
        cur.execute(f'SELECT {col0} FROM {tb0}')
        x = cur.fetchall()
        # convert x into a normal list
        l0 = list()
        for item in x:
            l0.append(item[0])

        # y axis is stock price 
        cur.execute(f'SELECT {col1} FROM {tb1}')
        y = cur.fetchall()
        # convert y into a normal list
        l1 = list()
        for item in y:
            l1.append(item[0])

        conn.commit()

        x = np.array(l0)
        y = np.array(l1)
        plt.scatter(l0, l1)
        m, b = np.polyfit(x, y, 1)
        plt.plot(x, m*x + b)
        plt.set_xlabel('deathIncrease')
        plt.set_ylabel('stock close price')
        plt.set_title('deathIncrease vs. stock close price')
        plt.show()

if __name__ == "__main__":
    writer = WriteData("Warehouse", "StockData", "WeatherData", "CovidData")
    cur, conn = writer.SetUpDatabase()
    writer.viz('positiveIncrease', 'CovidData', 'closing_price', 'StockData', cur, conn)
#     writer.SetUpTable("cache_stock", "cache_weather", "test_cache_Covid", cur, conn)
#     print(writer.correl('temp', 'WeatherData', 'closing_price', 'StockData', cur, conn))
#     print(writer.correl('deathIncrease', 'CovidData', 'closing_price', 'StockData', cur, conn))
#     print(writer.correl('positiveIncrease', 'CovidData', 'closing_price', 'StockData', cur, conn))
#     print(writer.correl('hospitalizedIncrease', 'CovidData', 'closing_price', 'StockData', cur, conn))
