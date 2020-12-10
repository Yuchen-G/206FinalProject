from unittest.main import main
from CacheHelper import CacheHelper
from sqlite3.dbapi2 import SQLITE_SELECT
import unittest
import sqlite3
import json
import os


class WriteData:
    def __init__(self, db_name, tb_name_1, tb_name_2):
        self.db_name = db_name
        self.tb_name_1 = tb_name_1
        self.tb_name_2 = tb_name_2
        self.Cache = CacheHelper()

    def SetUpDatabase(self):
        path = os.path.dirname(os.path.abspath(__file__))
        conn = sqlite3.connect(path+'/'+ self.db_name + '.db')
        cur = conn.cursor()
        return cur, conn

    def SetUpTable(self, cachefile1, cachefile2, cur, conn):
        # loads the data into dictionaries
        stock_data = self.Cache.read_cache(cachefile1)
        weather_data = self.Cache.read_cache(cachefile2)
        # create database
        # cur.execute(f"DROP TABLE IF EXISTS {self.tb_name_1}")
        # cur.execute(f"DROP TABLE IF EXISTS {self.tb_name_2}")
        cur.execute(f"CREATE TABLE IF NOT EXISTS {self.tb_name_1} (id TEXT PRIMARY KEY, closing_price REAL)") # Attention data type is float for closing price
        cur.execute(f"CREATE TABLE IF NOT EXISTS {self.tb_name_2} (id TEXT PRIMARY KEY, temp INTEGER)")
        # use for loop to enter records into table "StockData"
        for item in stock_data:
            id = item
            closing_price = stock_data[item]
            cur.execute(f"INSERT OR IGNORE INTO {self.tb_name_1} (id, closing_price) VALUES (?,?)", (id, closing_price))
        # use for loop to enter records into table "WeatherData"
        for item in weather_data:
            id = item
            temp = weather_data[item]
            cur.execute(f"INSERT OR IGNORE INTO {self.tb_name_2} (id, temp) VALUES (?,?)", (id, temp))
        # commit changes
        conn.commit()


if __name__ == "__main__":
    writer = WriteData("Warehouse", "StockData", "WeatherData")
    cur, conn = writer.SetUpDatabase()
    writer.SetUpTable("cache_stock", "cache_weather", cur, conn)