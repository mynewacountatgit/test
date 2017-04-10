#-*- coding: utf-8 -*-
"""
   Created  on 2017/3/31.
"""
import datetime
from indicator import short_indices
from pandas_datareader import data, wb
import matplotlib
matplotlib.style.use("ggplot")
from matplotlib import pyplot as plt
import pandas

start = datetime.datetime(2000, 1, 1)

spc = data.get_data_yahoo("^GSPC",start)
dow_j =  data.get_data_yahoo("^DJI",start)
hsi = data.get_data_yahoo("^HSI",start)
etf = data.get_data_yahoo("600001.SS",start)
etf = data.get_data_yahoo("510050.SS",start)


def oc_st(df_o, name, buy_col, sell_col, shift_n,rolling_n=12,cost_rate=0,limit=False):
    df = df_o.copy()
    df = df.sort_index()
    df.columns = df.columns.map(lambda p:p.lower())
    delta = (df[sell_col] - df[buy_col].shift(shift_n)) / df[buy_col]
    ### mask 将中间遮盖起来，不交易
    mask = [True if i%(shift_n+1)==0 else False for i in range(len(delta))]
    delta_mask = delta[mask]
    if limit:
        roll_mean = (df[sell_col] >(df[buy_col].shift(shift_n)) ).rolling(rolling_n).mean()
        signal1 = roll_mean > limit[0]
        signal2 = roll_mean< limit[1]
        gain = (1+signal1.shift(2)*(delta_mask-cost_rate)-  signal2.shift(2)*(delta_mask+cost_rate)).cumprod()
        print u"出手次数  ",(signal1*mask).sum() +(signal2*mask).sum()
    else:
        gain = (1 + delta_mask).cumprod()
        print u"出手次数  ", len(gain)
    print short_indices(gain, 0.03)
    merge_df = pandas.DataFrame()
    merge_df[name] = df.close
    merge_df["cum gain"] = gain
    merge_df = merge_df.dropna()
    merge_df = merge_df/merge_df.ix[0,]
    merge_df.plot()
    plt.show()



(1+signal1.shift(1)*delta_mask -  signal2.shift(1)*delta_mask).dropna()

df_o=etf

buy_col = "close"
sell_col = "open"
shift_n = 23
name = "etf"
oc_st(hsi,"^HSI",  "close","open",29,limit=[0.8,0.42])
oc_st(hsi,"^HSI",  "close","open",23,limit=[0.6,0.42])
oc_st(hsi,"^HSI",  "close","open",23,limit=[0.6,0.42])
oc_st(hsi,"^HSI","close", "open" ,23 )
oc_st(dow_j,"dow_j", "open" ,"close",3)
oc_st(sz,"sz", "open" ,"close",23 ,limit=[0.6,0.42])

import tushare

etf = tushare.get_h_data("510050")


oc_st(hsi,"^HSI",  "close","close",30,limit=[0.5,0.3])
oc_st(etf ,"etf",  "close","close",30,limit=[0.5,0.3])## hightest
oc_st(hsi,"^HSI",  "close","close",30 ,limit=[-0.2,0])
oc_st(spc,"spc",  "close","open",20,limit=[0.56,0.42])


oc_st(hsi,"^HSI",  "close","close",30,limit=[0.5,0.4])

oc_st(etf ,"etf","close",  "open",23,limit=[0.7,0.45],cost_rate=0.01)


quato = data.get_quote_yahoo('AMZN')
quato = data.get_quote_yahoo('510050.SS')
quato = data.Options("510050.SS")
data = quato.get_all_data()

import tushare as ts

fd = ts.Options()
fd.OptVar()
df = fd.Opt(contractStatus='L,DE', field='optID,secShortName,varShortName,listDate')
df = fd.getOptDpo(contractStatus='L,DE', field='optID,secShortName,varShortName,listDate')
ts.set_token('1b4a1c74f890d52633d9fa3607b4f260ef1c4f8200674d9a6549170ef430ff2f')