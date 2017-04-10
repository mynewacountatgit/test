#-*- coding: utf-8 -*-
"""
   Created  on 2017/4/9.
"""

etf = get_performance(stockid,start,end)


close_p = etf.close


from indicator import short_indices
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


df_o = etf
name="etf"
buy_col = "close"
sell_col = 'open'
shift_n = 23
limit= [0.3,0.5]
oc_st(df_o, name, buy_col, sell_col, shift_n,rolling_n=12,cost_rate=0,limit=limit)

signal = ((etf.close < etf.open.shift(23)).rolling(12).mean()) > 0.7


signal = (etf.close < etf.open.shift(23))

delta_p = (etf.close - etf.open.shift(23)) / (etf.open.shift(23))


delta_p = ((etf.close - etf.open.shift(3)) / (etf.open.shift(3))).mean()

signal2 = (etf.open.shift(3) < etf.open.shift(23)).shift(1)

gain = (signal & signal2) * delta_p
gain = signal * delta_p

cum_gain = (1-gain ).cumprod()
cum_gain.plot()
plt.show()

signal = (etf.close<etf.open.shift(23))


signal = (((etf.close < etf.open.shift(23)).rolling(10).mean()) > 0.7) .shift(3)


delta_p = (etf.close - etf.open.shift(23)) / (etf.open.shift(23))

delta_p = ((etf.close - etf.open.shift(3)) / (etf.open.shift(3)))
signal2 = (etf.open.shift(3) > etf.open.shift(23)).shift(1)

mask = [True if i%(5)==0 else False for i in range(len(delta_p))]

gain = mask *(signal & signal2) * delta_p

gain = (signal.shift(3) * delta_p).dropna()
cum_gain = (1-gain ).cumprod()
cum_gain.plot()
plt.show()


signal = (((etf.close > etf.open.shift(23)).rolling(12).mean()) > 0.6).shift(2)
 signal =True

mask = [True if i%(23)==0 else False for i in range(len(delta_p))]

delta_p = ((etf.close - etf.open.shift(23)) / ( etf.open.shift(23)))
signal2 = (etf.open >etf.open.shift(23))
# signal2 = True

gain = mask*((signal & signal2) * delta_p -0.02)



cum_gain = (1+gain  ).cumprod()
cum_gain.plot()
plt.show()
short_indices(cum_gain,0.03)






delta_p = ((etf['high_mean'] -etf['mean'].shift(5)) / (etf['mean'].shift(5)))
etf['mean'] = (  etf['low']-etf['open'] ) *0.50 +etf['open']
gain  = (1+(etf['high_mean']  - etf['mean'].shift(1))/etf['mean'].shift(1) -0.003).cumprod().plot()

etf['high_mean'] = (etf['high']  - etf['open']) *0.50 +etf['open']




signal = (((etf.close > etf.open.shift(23)).rolling(12).mean()) > 0.6).shift(1)


mask = [True if i%(23)==0 else False for i in range(len(delta_p))]

delta_p = ((etf.close - etf.open.shift(23)) / ( etf.open.shift(23)))


signal2 = (etf.open >etf.open.shift(23))
# signal2 = True

gain = mask*( signal   * delta_p -0.02)



cum_gain = (1+gain  ).cumprod()
cum_gain.plot()
plt.show()
short_indices(cum_gain,0.03)
