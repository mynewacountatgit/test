# -*- coding: utf-8 -*-
"""
   Created  on 2017/4/2.
"""

from datetime import datetime, timedelta
from  tiny.setting import *
import pandas
from pandas.tseries.offsets import *
import matplotlib
from matplotlib import pyplot as plt

matplotlib.style.use("ggplot")


def datetimetoint(datetimeobj):
    return int(datetimeobj.strftime("%Y%m%d"))


def decoding_s(p):
    """
    处理字符问题
    :param p: 字符
    :return: gbk解码的字符
    """
    if isinstance(p, basestring):
        return p.decode("gbk")
    else:
        return p


def get_stockids(bkname,date):
    """
    
    :param date: int format for date
    :return: stocks dataframe
    
    """
    date = int(date.strftime("%Y%m%d"))
    bkname = bkname.decode("utf")
    params = {"bkname":bkname,"date":date}
    call = u"""
    EndT:=inttodate(%(date)i);
    return StocksTraded(GetBk("%(bkname)s"),EndT);
    """ %  params
    data = ts.RemoteExecute(call, {})
    if data[0] == 0:
        a_stocks = data[1]

        trade_stock = pandas.DataFrame(a_stocks).applymap(decoding_s)
        trade_stock.columns = trade_stock.columns.map(decoding_s)
        trade_stock.index = trade_stock[u"代码"]
        return trade_stock
    else:
        print data[2].decode("gbk")


def profit(stockids, date):
    """
    
    :param stockids: list or any items which is iterable
    :param date:    datetime
    :return: profit dataframe
    """
    query_id = u";".join(stockids)
    date = int(date.strftime("%Y%m%d"))
    params = {"stockid": query_id, "date": date}
    call = u"""
    return  
        Query("","%(stockid)s",True,"","代码",DefaultStockID(), 
        "%(date)s",report(46008,%(date)i));
    """ % params
    data = ts.RemoteExecute(call, {})
    df = pandas.DataFrame(data[1]).applymap(decoding_s)
    df.columns = df.columns.map(decoding_s)
    df.rename(columns={str(date): pandas.to_datetime(str(date))}, inplace=True)
    df.index = df[u"代码"]
    df = df[ pandas.to_datetime(str(date))]
    return df


def share(stockids, date):
    """

    :param stockids: list or any items which is iterable
    :param date:    datetime
    :return: 指定日期流通股
    """
    query_id = u";".join(stockids)
    date = int(date.strftime("%Y%m%d"))
    params = {"stockid": query_id, "date": date}
    call = u"""
    return  
        Query("","%(stockid)s",True,"","代码",DefaultStockID(), 
        "股票名称",CurrentStockName(), 
        "%(date)s",StockNShares(%(date)s));
    """ % params
    data = ts.RemoteExecute(call, {})
    df = pandas.DataFrame(data[1]).applymap(decoding_s)
    df.columns = df.columns.map(decoding_s)
    return df


def get_volume(stockids, date):
    """

    :param stockids: list or any items which is iterable
    :param date:    datetime
    :return: 指定日期交易量
    """
    query_id = u";".join(stockids)
    date = int(date.strftime("%Y%m%d"))
    params = {"stockid": query_id, "date": date}
    call = u"""
    Setsysparam(pn_date(),inttodate(%(date)i));
    return  
        Query("","%(stockid)s",True,"","代码",DefaultStockID(), 
        "股票名称",CurrentStockName(), 
        "交易量",Vol());
    """ % params
    data = ts.RemoteExecute(call, {})
    df = pandas.DataFrame(data[1]).applymap(decoding_s)
    df.columns = df.columns.map(decoding_s)
    df.index = df[u"代码"]
    return df


def st(stockids,end):
    """

    :param stockids: list or any items which is iterable
    :param date:    datetime
    :return: 在此期间是否是st
    """
    query_id = u";".join(stockids)
    end =  int(end.strftime("%Y%m%d"))
    params = {"stockid": query_id, "end":end}
    call = u"""
    return  
        Query("","%(stockid)s",True,"","代码",DefaultStockID(), 
        "股票名称",CurrentStockName(), 
        "日期",IsST_3( %(end)i));
    """ % params
    data = ts.RemoteExecute(call, {})
    df = pandas.DataFrame(data[1]).applymap(decoding_s)
    df.columns = df.columns.map(decoding_s)
    df.index =df[u"代码"]
    return df


def get_tradeday(begin, end):
    """
    
    :param begin: 开始时间 datetime 格式
    :param end: 结束时间  datetime 格式 
    :return: 期间的交易日
    """
    begin = datetimetoint(begin)
    end = datetimetoint(end)
    call = """
        begt:=inttodate(%i);
        endt:=inttodate(%i);
        return datetostr(MarketTradeDayQk(BegT,EndT));
    """ % (begin, end)
    data = ts.RemoteExecute(call, {})
    data = pandas.to_datetime(data[1])
    dates = pandas.Series(data)
    dates.index = pandas.to_datetime(dates)
    return dates



def delta_pf(profit_i):
    """
    
    :param profit_i: 利润表现，由于是累计利润，故要做差
    :return: 差分后的获得的利润表现
    """
    profit_i = profit_i[profit_i != 0]
    first_year = profit_i.index[0].year
    end_year = profit_i.index[-1].year
    for i in range(first_year, end_year + 1):
        pf = profit_i[str(i)]
        pf = pf - pf.shift(1).fillna(0)
        profit_i.ix[pf.index] = pf
    return profit_i

def profit_judge_A(profit_i):
    profit_i = profit_i.dropna()
    recent_quarters = profit_i.last("6q")
    if len(recent_quarters) < 6:
        return False
    if (recent_quarters[[0, 1, -2, -1]] > 0).all():
        growth_rate0 = recent_quarters[-1] / recent_quarters[-5]## 最近季度同比增长
        growth_rate1 = recent_quarters[-2] / recent_quarters[-6]## 最近季度上一季度的同比增长
        if growth_rate0 > 1.2 and (growth_rate0 > growth_rate1):
            return True
    return False

def profit_judge_B(profit_i):
    '''
    
    :param profit_i: 利润
    :return: 满足要求的返回True 不满足的返回 False
    '''
    profit_i = profit_i.dropna()
    profit_i = profit_i[profit_i!=0]
    ## 最近6个财年的日期
    if not profit_i.index[-1].is_year_end:
        dates = pandas.date_range(end=profit_i.index[-1] + YearEnd(), periods=6, freq="4q")
    else:
        dates = pandas.date_range(end=profit_i.index[-1], periods=6, freq="4q")
    recent_years  = profit_i[dates]
    if len(recent_years) <6:
        ## 不足6个财年的返回False
        return False
    growth_rate = (recent_years.diff(1)/recent_years.shift(1)).dropna()
    if (growth_rate>0).all() and (growth_rate.mean() >0.25):
        ## 利润全为正，且算数平均利润增长大于25%
        return True
    else:
        return False


class StockPort(object):
    def __init__(self, stockid, money, start, end):
        self.stockid = stockid
        self.money = money
        self.start = start
        self.end = end
        self.posi = self._position()

    def _get_performance(self, rehabilitation_type=1):
        """

        :param rehabilitation_type: 复权类型
        :return: 行情表现
        """
        start = self._datetoint(self.start)
        end = self._datetoint(self.end)
        params = {"stockid": self.stockid, "start": start, "end": end, "reh_type": rehabilitation_type}
        call = u"""
            setsysparam(Pn_stock(),'%(stockid)s'); 
            setsysparam(Pn_rate(),%(reh_type)i); 
            begt:=inttodate(%(start)i); 
            endt:=inttodate(%(end)i); 
            setsysparam(pn_date(),endt);  
            SetSysParam(pn_rateday(),begt); 
            n:=tradedays(begt,endt); 
            return nday(n,'Date',datetostr(sp_time()),'close',close(),'open',open(),'low',low(),'high',high());
        """ % params
        data = ts.RemoteExecute(call, {})
        tmp = [pandas.Series(i) for i in data[1]]
        if len(tmp) <1:
            return
        tmp_df = pandas.concat(tmp, axis=1).T
        tmp_df.index = pandas.to_datetime(tmp_df["Date"])
        tmp_df = tmp_df.sort_index()
        return tmp_df

    def _datetoint(self, date):
        return int(date.strftime("%Y%m%d"))

    def _position(self):
        pf = self._get_performance()
        if pf is None:
            return pandas.Series()
        pf_df = pf.close
        posi = pf_df / pf_df[0] * self.money
        return posi

    def hold(self):
        return self.end not in self._position()

    def plot(self):
        self.posi.plot()
        plt.show()

class Portfolio(object):
    def __init__(self,money,start,end):
        self.money = money
        self.start = start
        self.end = end
        ## 生成会计报告日期，
        self._dates = pandas.date_range(end=self.start, periods=25, freq="q")
        ## 期间的交易日
        self.tradeday = get_tradeday(self.start, self.end)
        ## 上一个交易日
        self.last_tradeday = get_tradeday(self.start - timedelta(30), self.start - timedelta(1)).last("D").ix[0, 0]
        ## 没有停牌的股票
        self.stockids =self.get_no_st()
        ## 满足所有条件的股票
        self.q_all = self.get_qualified_all()
        ## 建仓
        self.pf,self.position = self.open()
    def get_no_st(self):
        stocks = get_stockids("A股", self.last_tradeday)
        st_state = st(stocks.index,self.tradeday[0])
        qualified_nost = st_state[st_state[u"日期"] == 0].index
        return qualified_nost
    def get_vol_qualified(self):
        ## 交易量满足要求的股票
        vol = get_volume(self.stockids, self.last_tradeday)
        qualified_vol = vol[vol[u"交易量"] >= 100e4].index
        return  qualified_vol
    def get_qualified_AB(self):
        ## 利润满足AB要求的股票
        ### 获得会计报告日期的利润
        dfs = [profit(self.stockids, date) for date in self._dates]
        profit_df_all = pandas.concat(dfs, axis=1).T

        ## 季度利润是累计值，做差
        delta_pf_all_0 = profit_df_all.diff(1)
        tmp = delta_pf_all_0.index.map(lambda x: delta_pf_all_0.ix[x, :] if x.month != 3 else  profit_df_all.ix[x, :])
        delta_pf_all =  pandas.concat(tmp, axis=1).T

        ## 满足逻辑A的股票
        qualified_A_0 = delta_pf_all.apply(profit_judge_A)
        qualified_A_1 = delta_pf_all.ix[:, qualified_A_0]
        qualified_A = qualified_A_1.columns

        ## 满足逻辑B的股票
        qualified_B_0 = profit_df_all.apply(profit_judge_B)
        qualified_B_1 = profit_df_all.ix[:, qualified_B_0]
        qualified_B = qualified_B_1.columns
        ## 同时满足的股票
        qualified_AB =qualified_B.intersection(qualified_A)
        return qualified_AB
    def get_qualified_C(self):
        ## 流通股
        stock_share = share(self.stockids,self._dates[-1])
        stock_share.index = stock_share[u"代码"]
        stock_share[u"股本秩"] = stock_share[self._dates[-1].strftime("%Y%m%d")].rank()
        stock_share[u"股本秩百分比"] = stock_share[u"股本秩"] / stock_share[u"股本秩"].max()
        qualified_C_0 = (stock_share[u"股本秩百分比"] > 0.1) & (stock_share[u"股本秩百分比"] < 0.6)
        qualified_C = stock_share[qualified_C_0].index
        return qualified_C
    def get_qualified_all(self):
        q_vol = self.get_vol_qualified()
        q_ab = self.get_qualified_AB()
        q_c = self.get_qualified_C()
        q_all = q_vol.intersection(q_ab).intersection(q_c)
        return q_all
    def get_nday_pf(self,stockid, money_i, start, end):
        """

        :param stockid: 股票的代码
        :param money_i: 股票初始的资金
        :param start: 开始买入的日期，暂时以第一交易日收盘价买
        :param end: 结束的日期，暂时以结束日的收盘价卖
        :return: 每天的价格，以收盘价展示
        """
        stock_p = StockPort(stockid, money_i, start, end)
        stock_p.posi.name = stockid
        return stock_p.posi
    def open(self):
        ## 满足要求的股票个数
        number_stock = len( self.q_all)
        if number_stock <1:
            return self.money
        ## 每个股票一月初分到的钱
        money_i = self.money / float(number_stock)
        ## 获取个股的表现，单日无数据的，沿用前一天的数据
        position_0 =  self.q_all.map(lambda id_i: self.get_nday_pf(id_i, money_i,self.start,self.end))
        position = pandas.concat(position_0, axis=1).fillna(method="ffill")
        ## 组合的表现
        month_pf = position.sum(axis=1)
        return month_pf,position
    def plot(self):
        self.pf.plot()
        plt.show()

pandas.concat(pandas.Series([1,1]))

series_date = pandas.date_range(datetime(2006,12,31),datetime(2017,2,28),freq="m")+timedelta(1)

pf_list = []
money  = 1.0
for i in range(len(series_date)-1):
    pf_i = Portfolio(money,series_date[i],series_date[i+1])
    pf_list.append(pf_i)
    money = pf_i.pf[-1]












pf_posi = [x.pf for x in pf_list]

pf_hold_stocks =  [(x.start,x.q_all) for x in pf_list]


Seies_hold  = pandas.Series(dict(pf_hold_stocks))

Seies_hold.to_csv(u"持仓.csv",encoding="gbk")

pf_all= pandas.concat(pf_posi)

pf_all.to_csv("pf.csv",encoding="gbk")

matplotlib.use('Agg')
from matplotlib.pyplot import plot,savefig
pf_all.plot()
savefig('pfFig.jpg')


stockids = get_stockids("A股",datetime(2017,3,1)).index
dates = pandas.date_range(end=datetime(2017,3,1), periods=40, freq="q")
dfs = [profit(stockids, date) for date in dates]
profit_df_all = pandas.concat(dfs, axis=1).T

quarter = profit_df_all.index.map(lambda x:profit_df_all.ix[x,:]  if x.month!=12 else None )

quarter = pandas.concat(quarter,axis=1)

no_quarter_rp =quarter[(quarter==0.0).sum(axis=1) >2].T
def stat_no_quarter_rp(x):
    x_dpna = x[x!=0.0]
    if (x_dpna.index[1:] - x_dpna.index[:-1] > timedelta(100)).sum() >0:
        return True
    else:
        return False

no_quarter = profit_df_all.ix[:,profit_df_all.apply(stat_no_quarter_rp)]


x =  profit_df_all.ix[:,777]
no_quarter.to_csv(u"没有季报.csv",encoding="gbk")