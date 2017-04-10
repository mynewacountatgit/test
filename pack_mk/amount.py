# coding: utf-8


## 导入相关包
import pandas
import tushare
from matplotlib import pyplot as plt
import matplotlib
import math
matplotlib.style.use("ggplot")
from indicator import short_indices








## the st object
class MarketSt(object):
    def __init__(self, market, col1, col2, p, and_or, start_date=None):
        """
        
        :param market: 基于的市场
        :param col1: 基于的市场本身的指标 收盘:close 开盘:open 等等
        :param col2: 同col 第二个指标
        :param p: 滚动计算的周数
        :param and_or:  两个信号的关系  依照col1：left ,依照 col2：right ,两者的and,两着的or（只有一个为真的为半仓）
        :param start_date: 开始的年份日期 例如 "2015" , "2016",None的话从默认从有数据开始
        """
        market.index = pandas.to_datetime(market.index)
        market = market.sort_index()
        self.market = market
        self.col1 = col1
        self.col2 = col2
        self.p = p
        self.and_or = and_or
        self.start_date = start_date
        if start_date == None:
            self.from_y_market = market
        else:
            start_date.from_y_market = self.market[start_date:]
        self.signal, self.gain = self.run()
        self.index = self._index()
        self.sg_latest = self.signal[-1]

    def run(self):
        self.from_y_market = self.from_y_market.sort_index()
        ## 周重采样平均，以p为参数，对周频数据滚动平均
        base1 = self.from_y_market[self.col1].resample("w").mean().dropna().rolling(self.p).mean()
        # base2 = market[col2].resample("w").mean().dropna().rolling(p).mean()
        base2 = self.from_y_market[self.col2].rolling(20).mean().resample("w").last()
        ##  每周的末的收盘价与每周初的开盘价，算收益率
        delta = (self.from_y_market.close.resample("w").last() - self.from_y_market.close.resample("w").last().shift(1)) / (self.from_y_market.close.resample("w").last().shift(1))
        ##  策略信号，如果比上周大，就多，基于每周末平仓
        signal1 = base1 > base1.shift(1)
        sig_df = pandas.concat([self.from_y_market[self.col2].resample("w").last(), base2], axis=1)
        sig_df.columns = ["close", "roling_close"]
        signal2 = sig_df.close > sig_df.roling_close
        if self.and_or == "and":
            signal_f = (signal1 & signal2).dropna()
        elif self.and_or == "or":
            signal_f = ((signal1 + signal2) / 2).dropna()
        elif self.and_or == "left":
            signal_f = signal1
        elif self.and_or == "right":
            signal_f = signal2
        ## 计算累积收益率
        gain = (1 + signal_f.shift(1) * delta).dropna().cumprod()
        return signal_f, gain

    def plot(self, hold=False):
        plot, = plt.plot(self.from_y_market.close[0] * self.gain,
                         label=" ".join([self.col1, self.col2, str(self.p), self.and_or]))
        if hold:
            return plot
        else:
            plot1, = plt.plot(self.from_y_market.close, label="index")
            plt.legend(handles=[plot, plot1])
            plt.show()

    def reset(self, market, col1, col2, p, and_or, start_date=None):
        self.market = market
        self.col1 = col1
        self.col2 = col2
        self.p = p
        self.and_or = and_or
        self.start_date = start_date
        if start_date == None:
            self.from_y_market = market
        else:
            start_date.from_y_market = self.market[start_date:]
        self.signal, self.gain = self.run()
        self.index = self._index()
        self.sg_latest = self.signal[-1]

    def _index(self):
        import math
        return short_indices(self.gain, 0.03)

if __name__ == "__main__":
    ## 获得各个股指对应的数据
    ##000001    上证指数
    ## 399004  深证100R
    ##399606    创业板R
    ## 000300   沪深300

    market = tushare.get_h_data('000001', index=True, start="2006-01-01").sort_index()
    market_sz = tushare.get_h_data('399004', index=True, start="2006-01-01").sort_index()
    market_hs = tushare.get_h_data('000300', index=True, start="2006-01-01").sort_index()
    market_cy = tushare.get_h_data('399606', index=True, start="2010-01-01").sort_index()

    ## save to local 可选
    market.to_csv("C:\\Users\\fisher\\Documents\\金融\\shzz_index.csv", encoding="gbk")
    market_sz.to_csv("C:\\Users\\fisher\\Documents\\金融\\shenz_index.csv", encoding="gbk")
    market_hs.to_csv("C:\\Users\\fisher\\Documents\\金融\\hs_index.csv", encoding="gbk")
    market_cy.to_csv("C:\\Users\\fisher\\Documents\\金融\\cy_index.csv", encoding="gbk")

    #  load from local 可选
    market = pandas.read_csv(u"C:\\Users\\fisher\\Documents\\金融\\index_data\\shzz_index.csv", encoding="gbk",
                             index_col=0)
    market_sz = pandas.read_csv(u"C:\\Users\\fisher\\Documents\\金融\\index_data\\shenz_index.csv", encoding="gbk",
                                index_col=0)
    market_hs = pandas.read_csv(u"C:\\Users\\fisher\\Documents\\金融\\index_data\\hs_index.csv", encoding="gbk",
                                index_col=0)
    market_cy = pandas.read_csv(u"C:\\Users\\fisher\\Documents\\金融\\index_data\\cy_index.csv", encoding="gbk",
                                index_col=0)

    mk = MarketSt(market, "amount", "close", 4, "and")
    mk.plot()#画图
    mk.gain# 收益情况
    mk.signal# 信号
    mk.index # 表现情况































