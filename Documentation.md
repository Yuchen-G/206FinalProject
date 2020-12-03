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

### Goals that we achieved

### The problems that we faced 


