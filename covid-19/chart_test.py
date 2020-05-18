# coding=utf-8

from pyecharts.charts import Bar

y = [1, 2, 3, 4, 5]

x = ['a', 'b', 'c', 'd', 'e']

bar = Bar().add_xaxis(x)
#bar = bar.add_yaxis(y)
bar.render('test.html')
