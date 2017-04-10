#-*- coding: utf-8 -*-
"""
   Created  on 2017/3/29.
"""
from indicator import short_indices
from matplotlib import pyplot as plt
from datetime import  timedelta
import pandas
import matplotlib


import tushare
matplotlib.style.use("ggplot")
cpi_ppi = pandas.read_csv("ppi_cpi.csv",encoding="gbk",index_col=0)
cpi_ppi.index = pandas.to_datetime(cpi_ppi.index)
cpi_ppi.columns
## delta  是两者之差

market = pandas.read_csv(u"C:\\Users\\fisher\\Documents\\金融\\index_data\\shzz_index.csv",encoding="gbk",index_col=0)

sz =market
sz.index = pandas.to_datetime(sz.index)
sz = sz.sort_index()
## 调整到月频率的数据
delta = (sz.close.resample("m").last() -sz.open.resample("m").first())/sz.open.resample("m").first()

delta.index = delta.index+timedelta(1)## 数据对齐


## 合在一起
df = pandas.concat([delta,cpi_ppi.delta],axis=1)

## 查看相关性  经测试，长短期都是负相关
plt.plot(df[0] ,df["delta"],"ro")
plt.show()
df.corr()
## 确定信号
signal1= df.delta <df.delta.shift(1)## cpi_ppi 的信号


## 低开的滚动信号  8周这个参数可调
signal0 = (delta>delta.shift(1)).rolling(8).mean()


## 做多
signal = signal0 >=0.55
## 做空
signal_rev = signal0 <=0.45


## 累计收益，多空
cum_delta = (1+(signal.shift(1))*delta-(signal_rev.shift(2))*delta).cumprod()
## 累计收益，无脑
cum_delta = (1+ delta).cumprod()
cum_delta.plot()
plt.show()
## 相关指标
short_indices(cum_delta ,0.03)

## 计算收益
gain = 1+signal1.shift(1)*df[0]
## 画图
sz.close.plot()
(sz.close[0]*gain.cumprod()).plot()
plt.show()

short_indices(gain.cumprod(),0.03)



cpi = tushare.get_cpi()

cpi.index = cpi["month"].apply(pandas.to_datetime)
dff = pandas.DataFrame()
dff["cpi"] =  cpi["cpi"].shift(1)
dff["index_gain"] = delta

dff = dff.dropna().sort_index()
dff.corr()

signal= dff["cpi"]>(dff["cpi"].shift(1))
gain = 1+dff["index_gain"]*(signal.shift(1))
sz.close.plot()
(sz.close[0]*gain.cumprod()).plot()
plt.show()

import tushare as ts
df = ts.shibor_data(2017)
for year in range(2006,2017):
    df = df.append( ts.shibor_data(year))

df.index = df.date.apply(pandas.to_datetime)
df= df.sort_index()
df.columns

## 日频
dff = pandas.DataFrame()
dff["marco"] =  df["1M"].shift(4)
dff["index_gain"] =(sz.close  -sz.open )/sz.open
dff = dff.dropna().sort_index()
dff.corr()



## 日频  隔天收盘
dff = pandas.DataFrame() ## 新建一个空的数据框
dff["marco"] =  df["ON"].shift(5) ## df是存着shibor的一个数据框，ON是隔夜拆借的数据
dff["index_gain"] =(sz.close  -sz.close.shift(1) )/sz.close.shift(1)## sz是上证每天的数据，隔天的收盘价差
dff = dff.dropna().sort_index() ## 去掉空值，按日期排列
dff.corr()## 算相关系数，此步没用特别必要


## 日频  最高
dff = pandas.DataFrame() ## 新建一个空的数据框
dff["marco"] =  df["ON"].shift(5) ## df是存着shibor的一个数据框，ON是隔夜拆借的数据
dff["index_gain"] =(sz.close  -sz.open)/sz.open## sz是上证每天的数据，收盘减去开盘除以开盘是 每天的收益
dff = dff.dropna().sort_index() ## 去掉空值，按日期排列
dff.corr()## 算相关系数，此步没用特别必要



## 周频
dff = pandas.DataFrame()
dff["marco"] =  df["ON"].resample("W").last().shift(4)
dff["index_gain"] = (sz.close.resample("w").last() -sz.open.resample("w").first())/sz.open.resample("w").first()

dff = dff.dropna().sort_index()
dff.corr()



##周频
dff = pandas.DataFrame()
dff["marco"] = (df["1M"]- df["ON"]).resample("W").last().shift(4)
dff["index_gain"] = (sz.close.resample("w").last() -sz.open.resample("w").first())/sz.open.resample("w").first()
dff = dff.dropna().sort_index()
dff.corr()



##周频
dff = pandas.DataFrame()
dff["marco"] = (df["1M"]- df["ON"]).resample("W").last().shift(2)
dff["index_gain"] = (sz.close.resample("w").last() -sz.open.resample("w").first())/sz.open.resample("w").first()
dff = dff.dropna().sort_index()
dff.corr()



signal= dff["marco"]<(dff["marco"].shift(1))## marco就是上面找的指标，这个指标是否比前期大，shift(1) 是指滞后一期
gain = 1+(dff["index_gain"]*(signal.shift(1) ))## 将信号滞后一期，然后算收益率
sz.close.plot()## 画图 画上证的
(sz.close["2006-10"][0]*gain.cumprod()).plot()## 画图，画策略的累计收益
plt.show()
short_indices(gain.cumprod(),0.03)

dff["index_gain"]  =(sz.close  -sz.close.shift(1) )/sz.close.shift(1)
dff["index_gain"]  =(sz.close  -sz.open.shift(1))/sz.open.shift(1)
dff["index_gain"]  = sz.close  /sz.open.shift(1)



## 对比
delta1 =  sz.close  /sz.close.shift(1) -1  ## 隔天买入
delta2 =  sz.open  /sz.close.shift(1) -1  ## 隔天买入
delta3 =  sz.close  /sz.open.shift(1) -1  ## 隔天买入
delta4 =  sz.open  /sz.open.shift(1) -1  ## 隔天买入
signal = pandas.Series([True if i%2==0 else False for i in range(len(gain)) ])  ## 由于是隔天的，所以去掉中间一天的收益率

## 以下只是规范一下格式
signal.index =  gain.index
gain1 = 1+delta1*signal
gain2= 1+delta2*signal
gain3= 1+delta3*signal
gain4= 1+delta4*signal
gain_cum1 = gain1.cumprod()## 算累计收益
gain_cum2 = gain2.cumprod()## 算累计收益
gain_cum3 = gain3.cumprod()## 算累计收益
gain_cum4 = gain4.cumprod()## 算累计收益
merge_df = pandas.DataFrame()
merge_df["market"] = sz.close
merge_df["close close"] = gain_cum1
merge_df["close open"] = gain_cum2
merge_df["open close"] = gain_cum3
merge_df["open open"] = gain_cum4
merge_df = merge_df.dropna()
merge_df["close close"] = merge_df["market"][0] *merge_df["close close"]
merge_df["close open"] = merge_df["market"][0] *merge_df["close open"]
merge_df["open close"] = merge_df["market"][0] *merge_df["open close"]
merge_df["open open"] = merge_df["market"][0] *merge_df["open open"]
merge_df.plot()
plt.show()


rate = (sz.open < sz.close.shift(1)).rolling(25).mean()
signal_f = rate>0.56
gain = 1 +delta3*signal_f.shift(1)
merge_df = pandas.DataFrame()
merge_df["market"] = sz.close
merge_df["open close"] = gain.cumprod()
merge_df["open close"] = merge_df["market"][0] *merge_df["open close"]
merge_df.plot()
plt.show()
rate.plot()
short_indices(gain.cumprod()["2016":],0.03)

short_indices(gain.cumprod()  ,0.03)
short_indices(gain_cum3 ,0.03)



(sz.open - sz.close.shift(1)).plot()
plt.hist((sz.open - sz.close.shift(1)))



### 准备金
import tushare as ts
import pandas
deposit = ts.get_deposit_rate()
money_supply =ts.get_money_supply()
cpi = ts.get_cpi()
cpi.index =pandas.to_datetime(cpi.month)
cpi = cpi.cpi
df_cpi = cpi.diff()
df_cpi = df_cpi.sort_index()
df_market_rate  =  sz.close.resample("m").last().diff()/(sz.close.resample("m").last().shift(1))
df_market_rate.index =df_market_rate .index + timedelta(1)
cooper = pandas.DataFrame()

cooper["df_cpi"] = df_cpi
cooper["df_market"] = df_market_rate
cooper = cooper.sort_index().dropna()
cooper.corr()

signal = (df_cpi> (df_cpi.shift(1))).rolling(12).mean() > 0.5
gain =  1+signal.shift(1)*df_market_rate

cum_gain = gain.dropna().cumprod()
short_indices(cum_gain,0.03)
cum_gain.plot()
plt.show()
import matplotlib
from matplotlib import  pyplot as plt
matplotlib.style.use("ggplot")


gain =  1+ df_market_rate
cum_gain = gain.dropna().cumprod()

cum_gain.plot()
plt.show()