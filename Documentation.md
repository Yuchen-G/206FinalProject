# Documentation

## 待办事项

1. WriteData.py 需要加入 check if database exists 的功能。
   - 现在情况是writedata.py如果检测到 database exists会drop database&table. 所以需要加入一个判断如果database exeists就不需要drop并且继续写的功能
2. GetStockData.py 需要加入处理异常值的功能。
   - 由于某些数据会拉取不到（周末，节假日或异常情况），json中的数据在写入database后两个table的id不能一一匹配（stock的id会缺失）
3. #这条可以忽略
   - WriteData.py 中的sql queries使用了f-string，这样写可能会受到sql injection攻击，但是因为sql query有严格的parameterization
条件，我目前还没有找到更好的办法。
4. 我们下一步是Calculation。我想用两组数据算出他们的correlation coefficient。
   - 最简单的办法是import numpy package. -->教程 <https://realpython.com/numpy-scipy-pandas-correlation-python>. 我的思路是用 for loop 把两个table中的数据拉出来存入两个 numpy array variables，然后算出correlation coefficient
5. 加入第三个API：Covid tracking --> 网站 <https://covidtracking.com/data/api>.
6. 需要写documentation。就是现在这个文件。具体内容我放到下面了。这个待办事项可以到时候删掉
7. can include boxplot

## Rubric

In addition to your API activity results, you will be creating a report for your overall project. The report must include:

1. The goals for your project (10 points)
2. The goals that were achieved (10 points)
3. The problems that you faced (10 points)
4. Your file that contains the calculations from the data in the database (10 points)
5. The visualization that you created (i.e. screen shot or image file) (10 points)
6. Instructions for running your code (10 points)
7. Documentation for each function that you wrote. This includes the input and output for
each function (20 points)
8. You must also clearly document all resources you used. The documentation should be of
the following form (20 points)

### Our Project Goals

For this project, our main goal is to explore the potential relationship between temperature of Cuppertino; daily covid positive cases; daily hospitalized covid cases; daily covid death cases and Apple company's stock price.

We use 3 APIs to gather relevant data. These APIs include

1. stock price from <https://marketstack.com/>
2. covid data from <https://covidtracking.com/data/api>
3. and weather data from <https://www.worldweatheronline.com/developer/>.

More specifically, we want to get

1. AAPL stock's closing price from 2020.05.01 to 2020.08.08
2. Cupertino's (where apple's HQ is located) daily weather, highest tempreture, lowest temp from 2020.05.01 to 2020.08.08
3. Covid-19 information (daily positive, death, and hospitalized info) from 2020.05.01-2020.08.08

After gathering relavant data, we want to store these data into a database called _database.db_ with three different tables with date as common _id_: _CovidData_, _StockData_, and  _WeatherData_.

We will then calculate the correlation coefficients between stock price and the daily positive covid cases, daily death cases, and daily hosipitalized people using _numpy_ package. And drawing several scatterplots to illustrate those relationships using _matplotlib_

Yuchen will be responsible for the data collection, Mengqi will be responsible for the plotting. We will build and test the database together. 

### Goals that we achieved

1. We successfully used 3 APIs and retrived data from them:
   1. Retrieved Apple's daily stock price from API1: <https://marketstack.com/>
   2. Retrieved Covid cases data from API2: <https://covidtracking.com/data/api>, 
      including daily positive increase, death increase, and hospitalized increase.
   3. Retrieved daily weather data from API3: <https://www.worldweatheronline.com/developer/>
2. Limited to collect 25 data at a time.
3. Stored the retrived data to database and join selected data with database key. 
4. Selected data from database and calculated correlation coefficient between stock price and the daily positive covid cases, daily death cases, and daily hosipitalized people.
5. Created 4 visualizations by using scatter plot and linear regression line to show
their relationships with each other.
   a. Daily Covid Death Increase vs. Apple's Daily Stock Price
   b. Daily Hospitalized Increase vs. Apple's Daily Stock Price
   c. Daily Positive Increase vs. Apple's Daily Stock Price
   d. Daily temperature vs. Apple's Daily Stock Price
6. Found a strong correlation between daily positive covid cases and Apple's stock price.

### The problems that we faced

1. When trying to handle the bad value in the database, for example, weekends during which we don't have the stock price information, we decided to give a value of -99 for those dates in stockdata json file. Then when writing in to the database, we added an extra step in the end to make sure that we delete those dates which has a value of -99 in the stock data table. And we also delete those dates in the weather data accordingly with a JOIN statment. Thus, we can skip those dates with no stock price information when calculating the correlation coefficient or drawing graphs.
2. The original API we used to get stock data didn't worked well so that we had to found another API for stock price data.
3. how to pull 25 data every time 


### Your file that contains the calculations from the data in the database

![Screenshot of **output.txt**]()

### The visualization that you created (i.e. screen shot or image file) (10 points)

### Instructions for running your code (10 points)

### Documentation for each function that you wrote. This includes the input and output for each function (20 points)

### You must also clearly document all resources you used. The documentation should be of the following form (20 points)
