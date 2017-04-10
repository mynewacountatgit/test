#-*- coding: utf-8 -*-
"""
   Created  on 2017/3/25.
"""
import os
import random

import matplotlib
import pandas
from matplotlib import pyplot as plt

from  v.get_data import data_path
from v.get_stock import *
matplotlib.style.use("ggplot")

def good_look(price_series,dvb=12):
    window = len(price_series)/dvb
    data_mean =price_series.rolling(10, center=True).mean()
    data_mean_moving =price_series.rolling(window).mean()
    cummean = price_series.rolling("D").mean()
    plot1,  = plt.plot(data_mean,label="performance")
    plot2,  = plt.plot(cummean,label="day mean")
    plot3,  = plt.plot( data_mean_moving,label="moving mean")
    best_point, prefer_point =good_point(price_series,dvb)
    plot4  = plt.scatter(*best_point,label="best_point")
    if prefer_point:
        plot5=plt.scatter(*prefer_point,label="prefer_point")
        plt.legend(handles=[plot1, plot2, plot3, plot4,plot5])
    else:
        plt.legend(handles=[plot1, plot2, plot3, plot4])
    plt.show()


def good_point(price_series,dvb=12):
    window = len(price_series) / dvb
    afternoon = price_series[date_name + " 13":]
    afternoon_mean_moving = afternoon.rolling(window).mean()
    go_down_cum = (afternoon <= afternoon_mean_moving).rolling(window).mean()
    quality = go_down_cum[go_down_cum >0.8]
    best_point = go_down_cum.argmax(), afternoon[go_down_cum.argmax()]
    if len(quality)>0:
        prefer_point =quality.index[0],price_series[quality.index[0]]
    else:
        prefer_point = False
    return best_point,prefer_point



## 股票
basic = get_basic_info()
stock_codes = basic.index

stock_min = get_min_data(stock_codes[3],"2017-03-24")
date_name = "2017-03-24"
n = random.choice(stock_codes )

data_i =get_min_data(stock_codes[3],"2017-03-24")

stock_day = get_daily_data(stock_codes[3])

ma_day_p = stock_day.close.rolling(5,win_type='blackman').mean()[-1]



ma_day_p.plot()
stock_day.close.plot()
plt.show()

good_look( data_i["price"],18)
