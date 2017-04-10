#-*- coding: utf-8 -*-
"""
   Created  on 2017/3/27.
"""

import pandas
import tushare
from matplotlib import pyplot as plt
import matplotlib
from  datetime import  datetime
matplotlib.style.use("ggplot")



def kdj(df, parameters=(9, 3, 3)):
    """

    RSVt＝(Ct－L9)／(H9－L9)＊100
    Kt＝RSVt／3＋2＊Kt-1／3
　　Dt＝Kt／3＋2＊Dt-1／3
　　Jt＝3＊Dt－2＊Kt

    :param df: 
    :param parameters: 
    :return: 

    """
    p0 = parameters[0]
    p1 = parameters[1]
    p2 = parameters[2]
    df = df.sort_index()
    df.index = pandas.to_datetime(df.index)
    high_n = df[u'high'].rolling(p0).max()
    low_n = df[u"low"].rolling(p0).min()
    rsvt = (df[u"close"] - low_n) / (high_n - low_n) * 100
    rsvt.dropna(inplace=True)
    k = []
    d = []
    j = []
    for i in range(len(rsvt)):
        if i == 0:
            k.append(50)
            d.append(50)
            j.append(50)
        else:
            kt = rsvt.ix[i] / 3 + 2 * k[i - 1] / 3
            dt = kt / 3 + 2 * d[i - 1] / 3
            jt = 3 * dt - 2 * kt
            k.append(kt)
            d.append(dt)
            j.append(jt)
    kdj_df = pandas.DataFrame()
    kdj_df["k"] = k
    kdj_df["d"] = d
    kdj_df["j"] = j
    kdj_df["long"] = (kdj_df[u"k"] > kdj_df[u"d"]) & (kdj_df[u"k"] > kdj_df[u"j"])
    kdj_df["short"] = (kdj_df[u"k"] < kdj_df[u"d"]) & (kdj_df[u"k"] < kdj_df[u"j"])
    kdj_df.index = rsvt.index
    kdj_df["open"] = df[u"open"][rsvt.index]
    return kdj_df


def plot_kdj(kdj_df):
    plt.subplot(211)
    plot0, = plt.plot(df["close"], label="day performance")
    plt.subplot(212)
    plot1, = plt.plot(kdj_df["k"], label="k line")
    plot2, = plt.plot(kdj_df["d"], label="d line")
    plot3, = plt.plot(kdj_df["j"], label="j line")
    plt.legend(handles=[plot0, plot1, plot2, plot3])
    plt.show()


def parser_time(time):
    if time=="0":
        return pandas.to_datetime('19000101', format='%Y%m%d',errors="ignore")
    else:
        return pandas.to_datetime(time, format='%Y%m%d',errors="ignore")

def save_data(code):
    file_name = save_path+"%s.csv"%code
    import os
    if os.path.exists(file_name):
        return
    df = tushare.get_h_data(code)
    df.to_csv(save_path+"%s.csv"%code,encoding="gbk")




codes = tushare.get_stock_basics()


codes[u'timeToMarket'] = codes[u'timeToMarket'].apply(str)
codes[u'timeToMarket']  =  codes[u'timeToMarket'].apply(parser_time)

code_in =   codes.index[(codes[u'timeToMarket'] > datetime(2016,1,1)) & (codes[u'timeToMarket'] < datetime(2017,1,1))]


save_path = "./gold_cross/new_stocks/"

code_in = pandas.Series(list(set(code_in)))
code_in.apply(save_data)

code_i = code_in[1]

def gold_cross(code):
    df = tushare.get_h_data(code_i)
    kdj_df = kdj(df)
    long = (kdj_df["long"] > (kdj_df["long"].shift(1))).shift(1)
    short = (kdj_df["short"] > (kdj_df["short"].shift(1))).shift(1)
    long[kdj_df["k"] < 50] = False
    short[kdj_df["k"] > 50] = False
    buy_sell = kdj_df["open"] * long - short * kdj_df["open"]
    buy_sell = buy_sell[buy_sell != 0]
    gain = buy_sell + buy_sell.shift(1)
    gain.cumsum().plot()
    plt.show()
    return gain


gain_i = gold_cross(code_i)


plot_kdj(kdj_df)

