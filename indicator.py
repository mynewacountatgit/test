#-*- coding: utf-8 -*-
"""
   Created  on 2017/3/30.
"""
import pandas,math

## basic index
def short_indices(add_nav, rf):
    # delta = pandas.Series(df.index[1:] - df.index[:-1])
    # year_count = int(365.0 / delta.value_counts().argmax().days)
    add_nav = add_nav.dropna()
    annualized_returns = (add_nav.ix[-1] / add_nav.ix[0] )**(365.0/(add_nav.index[-1]-add_nav.index[0]).days)- 1
    rp = annualized_returns
    day_return = add_nav.diff() / add_nav.shift() - 1
    sharpe_ratio = (rp - rf) / (day_return.std() * math.sqrt(len(add_nav)))
    def withdraw_new(add_nav):
        if len(add_nav)<1:
            return None,None
        new_high = add_nav[add_nav >= add_nav.cummax()]
        new_high[add_nav.index[-1]] = add_nav[-1]
        new_high_day = pandas.Series(new_high.index)
        withdraw_days = (new_high_day - new_high_day.shift(1)).max().days
        withdraw_rate = max(map(lambda b, e: 1 - add_nav[b:e].min() / add_nav[b], new_high_day[:-1], new_high_day[1:]))
        return withdraw_rate, withdraw_days
        # return  withdraw_rate, withdraw_time
    withdraw_rate, withdraw_days = withdraw_new(add_nav)
    day_gain = add_nav-add_nav.shift(1)
    win_rate = float((day_gain >0).sum())/ (day_gain !=0).sum()
    win_lose = day_gain[day_gain>0].sum()/abs(day_gain[day_gain<0].sum())
    days = len(add_nav)
    index_name = u"年化收益,胜率,盈亏比,夏普比率,最大回撤,最大回撤周期,数据个数".split(u",")
    index_value = rp, win_rate,win_lose ,sharpe_ratio, withdraw_rate, withdraw_days, days
    values = pandas.Series(index_value, index=index_name)
    return values


def llt_smooth(price, alpha= 2.0/31):
    price = pandas.Series(price)
    all_v = (alpha - alpha ** 2 / 4) * price + (alpha ** 2) / 2 * price.shift(1) - (alpha - 3 * alpha ** 2 / 4) * price.shift(2)
    llt = [0,0]
    for i in range(2,len(price)):
        llt_i = all_v[i]+ 2*(1-alpha)*llt[i-1]-(1-alpha)**2 * llt[i-2]
        llt.append(llt_i)
    return pandas.Series(llt,index=price.index)




# def withdraw_new(d):
#     d_ = d.copy()
#     new_high_v = 0
#     new_high_record = []
#     for i in range(len(d_)):
#         if d_[i] >new_high_v:
#             new_high_v = d_[i]
#             new_high_record.append(i)
#     if len(new_high_record) <= 1:
#         withdraw_time = len(d_)
#         if len(new_high_record) == 0:
#             withdraw_rate = 0.0
#         else:
#             withdraw_rate = 1-min(d_)/max(d_)
#     else:
#         max_delta = max([ d.index[new_high_record[i+1]] - d.index[new_high_record[i]] for i in range(len(new_high_record)-1)])
#         withdraw_time =  max(max_delta,d.index[-1]-d.argmax()).days-1
#         draw_rate = []
#         for i_gap in range(len(new_high_record)-1):
#             max_index = new_high_record[i_gap],new_high_record[i_gap+1]
#             min_v = min(d_[max_index[0]:max_index[1]])
#             draw_rate.append(1-min_v/d_[max_index[0]])
#         withdraw_rate = max(draw_rate)
#     # return  withdraw_rate, withdraw_time