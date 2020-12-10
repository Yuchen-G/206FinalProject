from unittest.main import main
from CacheHelper import CacheHelper
from sqlite3.dbapi2 import SQLITE_SELECT
import unittest
import sqlite3
import json
import os
import numpy as np


class WriteData:
    def __init__(self, db_name, tb_name_1, tb_name_2):
        self.db_name = db_name
        self.tb_name_1 = tb_name_1
        self.tb_name_2 = tb_name_2
        self.Cache = CacheHelper()

    def SetUpDatabase(self):
        path = os.path.dirname(os.path.abspath(__file__))
        conn = sqlite3.connect(path+'/' + self.db_name + '.db')
        cur = conn.cursor()
        return cur, conn

    def SetUpTable(self, cachefile1, cachefile2, cur, conn):
        # loads the data into dictionaries
        stock_data = self.Cache.read_cache(cachefile1)
        weather_data = self.Cache.read_cache(cachefile2)
        # create database
        # cur.execute(f"DROP TABLE IF EXISTS {self.tb_name_1}")
        # cur.execute(f"DROP TABLE IF EXISTS {self.tb_name_2}")
        # Attention data type is float for closing price
        cur.execute(
            f"CREATE TABLE IF NOT EXISTS {self.tb_name_1} (id TEXT PRIMARY KEY, closing_price REAL)")
        cur.execute(
            f"CREATE TABLE IF NOT EXISTS {self.tb_name_2} (id TEXT PRIMARY KEY, temp INTEGER)")
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
        # handle bad value
        cur.execute('DELETE FROM WeatherData WHERE WeatherData.id IN (SELECT WeatherData.id FROM StockData JOIN WeatherData ON StockData.id = WeatherData.id WHERE StockData.closing_price = -99)')
        cur.execute('DELETE FROM StockData WHERE StockData.closing_price = -99')
        # commit changes
        conn.commit()

    def correl(self, cur, conn):
        """
        calculate the correlation coefficient for two datasets in the database
        """

        # x axis is weather info
        cur.execute('SELECT temp FROM WeatherData')
        x = cur.fetchall()
        # convert x into a normal list
        l0 = list()
        for item in x:
            l0.append(item[0])
        # convert l0 into an np array
        l0 = np.array(l0)

        # y axis is stock price 
        cur.execute('SELECT closing_price FROM StockData')
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


if __name__ == "__main__":
    writer = WriteData("Warehouse", "StockData", "WeatherData")
    cur, conn = writer.SetUpDatabase()
    writer.SetUpTable("cache_stock", "cache_weather", cur, conn)
    print(writer.correl(cur, conn))
