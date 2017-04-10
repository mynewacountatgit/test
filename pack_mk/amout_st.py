#-*- coding: utf-8 -*-
"""
   Created  on 2017/3/27.
"""

import pandas
import tushare
from matplotlib import pyplot as plt
import matplotlib


matplotlib.style.use("ggplot")

codes = tushare.get_stock_basics()

market = tushare.get_h_data('000001', index=True, start="2006-01-01").sort_index()
market_sz = tushare.get_h_data('399004', index=True, start="2006-01-01").sort_index()
market_hs = tushare.get_h_data('000300', index=True, start="2006-01-01").sort_index()
market_cy = tushare.get_h_data('399606', index=True, start="2010-01-01").sort_index()




def try_para(market,p):
    market = market.sort_index()
    base = market["amount"].resample("w").mean().dropna().rolling(p).mean()

    delta = ((market.close.resample("w").last() - market.open.resample("w").first()) / market.open.resample("w").first()).dropna()
    signal = base > base.shift(1)
    gain = (1 + signal.shift(1) * delta).dropna().cumprod()
    return gain

def plot_st(market,k,n):
    plot1, = plt.plot(market.close, label="  index")
    handles = [plot1]
    for i in range(k,n):
        gain = try_para(market,i)
        plot2, = plt.plot(market.close[0] * gain, label="Strategy"+str(i))
        handles.append(plot2)
    plt.legend(handles=handles)
    plt.show()

plot_st(market["2008":],3,9)
plot_st(market_sz["2008":],3,9)
plot_st(market_hs["2010":],3,9)
plot_st(market_cy["2010":],3,9)

