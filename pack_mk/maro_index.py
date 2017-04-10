#-*- coding: utf-8 -*-
"""
   Created  on 2017/4/5.
"""

import datetime
from indicator import short_indices
from pandas_datareader import data, wb
import matplotlib
matplotlib.style.use("ggplot")
from matplotlib import pyplot as plt
import pandas

start = datetime.datetime(2000, 1, 1)



spc = data.get_data_yahoo("^GSPC",start)### 标普
dow_j =  data.get_data_yahoo("^DJI",start)### 道琼斯
hsi = data.get_data_yahoo("^HSI",start) ## 恒生
sz = data.get_data_yahoo("600001.SS",start) ### 上证

### 导入数据

### 只是清理格式
market = pandas.read_csv(u"C:\\Users\\fisher\\Documents\\金融\\index_data\\shzz_index.csv",encoding="gbk",index_col=0)
market.index = pandas.to_datetime(market.index)
factors = pandas.read_csv("C:\\Users\\fisher\\Desktop\\indicator.csv",encoding="gbk",index_col=0)
assets = pandas.read_csv("C:\\Users\\fisher\\Desktop\\asset.csv",encoding="gbk",index_col=0)

factors.columns = factors.columns+factors.ix[0,:]
assets.columns = assets.columns+assets.ix[0,:]
factors = factors.drop(u'频率')
assets = assets.drop(u'Date')
factors.index  = pandas.to_datetime(factors.index )
assets.index  = pandas.to_datetime(assets.index )

factors = factors.applymap(float)
assets= assets.applymap(float)

factors_dict = {}
for col in factors:
    col_data = factors[col]
    col_data =col_data.dropna()
    if col[-1] ==u"日":
        col_data = col_data.resample("m").mean()
    if  col[-1] ==u"年":
        continue
    factors_dict[col] = col_data

factors_df = pandas.DataFrame(factors_dict )
factors_df = factors_df .dropna()

assets_m = assets.resample("m").last()
assets_rate = assets_m.diff()/(assets_m.shift(1))

g_df = pandas.concat([assets_rate ,factors_df],axis=1)
g_df = g_df.dropna()
g_df.corr().to_csv("C:\\Users\\fisher\\Desktop\\corrletion.csv",encoding="gbk")




### 铜 菜篮子 债券 pmi 数据导入
factor1 = pandas.read_csv("C:\\Users\\fisher\\Desktop\\tong.csv",encoding="gbk",index_col=0).dropna()
factor0 = pandas.read_csv("C:\\Users\\fisher\\Desktop\\index0.csv",encoding="gbk",index_col=0)
bond = pandas.read_csv("C:\\Users\\fisher\\Desktop\\bond.csv",encoding="gbk",index_col=0)
factor1.index = pandas.to_datetime(factor1.index)
factor0.index = pandas.to_datetime(factor0.index)
bond.index = pandas.to_datetime(bond.index)

lanzi = factor0[u"菜篮子产品批发价格200指数:环比"].dropna()

factor0.index = pandas.to_datetime(factor0.index) - pandas.to_timedelta(1)
pmi = factor0["PMI"].dropna()
tong = factor1.resample("m").mean()



## 四个指标
bond = (bond.resample("m").mean()).ix[:,0]
lanzi= lanzi.resample("m").mean()
pmi = pmi.resample("m").mean()
tong_cr = (tong.diff(1)/(tong.shift(1))).ix[:,0]


###导入shibor 数据
import tushare as ts
df = ts.shibor_data(2017)
for year in range(2006,2017):
    df = df.append( ts.shibor_data(year))

df.index = df.date.apply(pandas.to_datetime)
df= df.sort_index()
df.columns
shibor = df


def reshape(mk,base,freq,shift_n=1,plot=True):
    """
    
    :param mk: 基于的市场 或组合
    :param base: 信号基于的指标
    :param freq: 频率， 不低于 mk和base里面频率较低的 m:mouth d:day y:year q:quarter
    :param shift_n: 信号滞后几期
    :param plot: 是否绘图
    :return:  返回策略的几个基本评价指标,还有策略信号
    """
    mk_copy = mk.resample(freq).last()
    base = base.resample(freq).last()
    m = pandas.DataFrame()
    m["mk_rate"] = mk_copy.diff(1)/(mk_copy.shift(1))
    m["base"] = base
    m = m.dropna()
    ### 看相关系数的正负，调整信号
    if m.corr().ix[0,1] >0:
        signal = m["base"] > (m["base"].shift(1))
    else:
        signal =m["base"] <(m["base"].shift(1))
    mk_gain = (1+m["mk_rate"]).cumprod()
    sg_gain = (1+signal.shift(shift_n)  *m["mk_rate"]).cumprod().dropna()
    print short_indices( sg_gain,0.03)
    if plot:
        mk_gain.plot()
        sg_gain.plot()
        plt.show()
    return short_indices( sg_gain,0.03),signal


### 把base 设置成不同的值然后看 表现情况
base = factors_dict[u"投资者信心指数:总指数月"]
base = factors_dict[u"工业增加值:当月同比月"].diff()
base = factors_dict[u"中债国债到期收益率:1年日"].diff()
base = factors_dict[u"中债国债到期收益率:3个月日"]
base = factors_dict[u"M2:同比月"]
base = factors_dict[ u"OECD综合领先指标:中国月"].diff()  ## 这个还可以
base = factors_dict[ u"贸易差额:当月值月"]
base = factors_dict[ u"银行间同业拆借:加权平均利率:1天:当月值月"].diff()
base = factors_dict[ u"PPI:全部工业品:当月同比月"]
base = factors_dict[ u"人民币:实际有效汇率指数月"]
base = factors_dict[ u"RPI:当月同比月"]
base = spc.Close
base = tong
base = shibor["ON"]
base = lanzi
base = bond
### 也可以设置不同的市场
mk = market.close
mk = spc.Close
mk = hsi.Close
freq="m"
reshape(mk,base,freq,1 )
reshape(mk,base,"d")


### 导入量的指标
from  pack_mk.amount import MarketSt

mk_st = MarketSt(market, "volume", "close", 4, "and")
mk_st.plot()


### 纯粹接入信号的函数
def accept_signal(mk,signal,plot=True,freq="w"):
    """
    
    :param mk: 基于的市场
    :param signal: 信号，可以在其他地方混合，可以是True False 也可以是 0.
    :param plot: 是否绘图
    :param freq: 制定频率 m:mouth d:day y:year q:quarter
    :return: 信号的表现
    """
    mk  = mk.resample(freq).last()
    signal = signal.resample(freq).last()
    delta_mk = mk.diff(1)/mk.shift(1)
    mk_pf = (1+delta_mk).dropna().cumprod()
    cum_gain = (1+delta_mk*signal).dropna().cumprod()
    print short_indices( cum_gain,0.03)
    if plot:
        mk_pf.plot()
        cum_gain.plot()
        plt.show()
    return short_indices(cum_gain,0.03)


### 结合两类信号

signal1 = mk_st.signal.resample("m").last() ### 量价信号
signal2 = reshape(market.close,base,freq,shift_n=1,plot=False)[1].resample("m").last() ## 宏观信号
signal3=  signal1 | signal2 ### 结合二者

accept_signal(market.close, signal3.shift(1),freq="m")


