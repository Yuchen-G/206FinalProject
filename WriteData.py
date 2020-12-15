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
    '''
    This class writes the input into databases.
    Besides, it is able to calculate correlation coefficients and 
    draws graphs.
    '''

    def __init__(self, db_name, tb_name_1, tb_name_2,tb_name_3,tb_name_4):
        '''
        This constructor initializes variables.
        It takes in the database name and three table names
        that we are trying to create. 
        '''
        self.db_name = db_name
        self.tb_name_1 = tb_name_1
        self.tb_name_2 = tb_name_2
        self.tb_name_3 = tb_name_3
        self.tb_name_4 = tb_name_4
        self.Cache = CacheHelper()

    def SetUpDatabase(self):
        '''
        This method sets up the database
        It doesn't take any input but will create a sqlite3 database
        '''
        path = os.path.dirname(os.path.abspath(__file__))
        conn = sqlite3.connect(path+'/' + self.db_name + '.db')
        cur = conn.cursor()
        return cur, conn

    def SetUpTable(self, cachefile1, cachefile2, cachefile3, cur, conn):
        '''
        This method takes in the three cache files and the cur conn that connects to the database.
        It creates tables if they are not exist and updates values from the JSON cache file 
        into the database.
        It also delete bad values from the database(ex: weekends that have no information about stock price)
        '''
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
        cur.execute(
            f"CREATE TABLE IF NOT EXISTS {self.tb_name_4} (id TEXT PRIMARY KEY, hospitalizedCumulative INTEGER)")
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
            hospitalizedCumulative = covid_data[item]["hospitalizedCumulative"]
            cur.execute(
                f"INSERT OR IGNORE INTO {self.tb_name_3} (id, deathIncrease, hospitalizedIncrease, positiveIncrease) VALUES (?,?,?,?)", (id, deathIncrease, hospitalizedIncrease, positiveIncrease))
            cur.execute(
                f"INSERT OR IGNORE INTO {self.tb_name_4} (id, hospitalizedCumulative) VALUES (?,?)", (id, hospitalizedCumulative))
        # handle bad value
        cur.execute('DELETE FROM WeatherData WHERE WeatherData.id IN (SELECT WeatherData.id FROM WeatherData JOIN StockData ON StockData.id = WeatherData.id WHERE StockData.closing_price = -99)')
        cur.execute('DELETE FROM CovidData WHERE CovidData.id IN (SELECT CovidData.id FROM CovidData JOIN StockData ON StockData.id = CovidData.id WHERE StockData.closing_price = -99)')
        cur.execute('DELETE FROM CovidData1 WHERE CovidData1.id IN (SELECT CovidData1.id FROM CovidData1 JOIN StockData ON StockData.id = CovidData1.id WHERE StockData.closing_price = -99)')
        cur.execute('DELETE FROM StockData WHERE StockData.closing_price = -99')
        # commit changes
        conn.commit()


    def write_correl(self, filename, input):
        '''
        This function takes in the input value and writes the data into a txt file.
        '''

        with open(filename,'a') as fh:
            # lines = fh.readlines()
            fh.write(input + '\n')



    def correl(self, col0, tb0, col1, tb1, cur, conn):
        """
        This function takes each column from two tables and 
        calculates the correlation coefficient for two datasets in the database.
        It returns the correlation coefficient.
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

    def viz(self, col0, tb0, col1, tb1, cur, conn, x_label, y_label, title0):
        '''
        This function takes string of x axis, y axis, and graph title. It also takes each column from two tables 
        and store the data in list then create a scatter plot using these data points. 
        It returns a scatter plot graph by the given data and strings.
        '''
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

        #create visualization
        x = np.array(l0)
        y = np.array(l1)
        plt.scatter(l0, l1)
        m, b = np.polyfit(x, y, 1)
        plt.plot(x, m*x + b, 'r')
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title0)
        
        plt.show()

# if __name__ == "__main__":
#     writer = WriteData("Warehouse", "StockData", "WeatherData", "CovidData")
#     cur, conn = writer.SetUpDatabase()
#     writer.SetUpTable("cache_stock", "cache_weather", "test_cache_Covid", cur, conn)
#     # Correlation Coefficient 0
#     correl0 = writer.correl('positiveIncrease', 'CovidData', 'closing_price', 'StockData', cur, conn)
#     str0 = "Correlation coefficient between daily positive cases and Apple's stock price is "+ str(correl0)
#     writer.write_correl('output.txt', str0)
#     # Correlation Coefficient 1
#     correl1 = writer.correl('temp', 'WeatherData', 'closing_price', 'StockData', cur, conn)
#     str1 = "Correlation coefficient between temperature and Apple's stock price is "+ str(correl1)
#     writer.write_correl('output.txt', str1)
#     # Correlation Coefficient 2
#     correl2 = writer.correl('deathIncrease', 'CovidData', 'closing_price', 'StockData', cur, conn)
#     str2 = "Correlation coefficient between daily death cases and Apple's stock price is "+ str(correl2)
#     writer.write_correl('output.txt', str2)
#     # Correlation Coefficient 3
#     correl3 = writer.correl('hospitalizedIncrease', 'CovidData', 'closing_price', 'StockData', cur, conn)
#     str3 = "Correlation coefficient between daily hospitalized cases and Apple's stock price is "+ str(correl3)
#     writer.write_correl('output.txt', str3)
#     # Visualization
#     writer.viz('positiveIncrease', 'CovidData', 'closing_price', 'StockData', cur, conn)
