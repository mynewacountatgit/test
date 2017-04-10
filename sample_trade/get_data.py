# -*- coding: utf-8 -*-
"""
   Created  on 2017/4/6.
"""

import tushare as ts
import pandas
from collections import  defaultdict

df = ts.get_realtime_quotes('000581')  # Single stock symbol


def long(stockid, price, amount):
    realtime_quoted = ts.get_realtime_quotes('000581')


class Simulated_disk(object):
    def __init__(self, money):
        self.money = money
        self.stocks = defaultdict(int)
        self.order = {}
        self.order["on"] = []
        self.order["done"] = []
        self.orderid = 0

    def long(self, stockid, price, volume):
        note = pandas.Series([1, stockid, price, volume],
                             index=["order_type", "stockid", "price", "volume", "done_volume"],name=self.orderid)
        self.orderid += 1
        self.order["on"].append(note)

    def short(self, stockid, price, volume):
        volume = min(self.stocks[stockid],volume)
        note = pandas.Series([-1, stockid, price, volume],
                             index=["order_type", "stockid", "price", "volume", "done_volume"],name=self.orderid)
        self.orderid += 1
        self.order["on"].append(note)

    def deal_on(self):
        if not self.order["on"]:
            return
        now_deal = self.order["on"].pop()
        realtime_quote = ts.get_realtime_quotes(now_deal.stockid)
        if now_deal==1:
            if now_deal.price < realtime_quote.price:
                self.order["on"].append(now_deal)
                return
        elif now_deal==-1:
            if now_deal.price > realtime_quote.price:
                self.order["on"].append(now_deal)
                return
        bid_volume = now_deal.volume - now_deal.done_volume
        new_done =  min(bid_volume,realtime_quote.volume)
        now_deal.done_volume += new_done
        self.money -= now_deal.order_type * now_deal.price * new_done*100
        self.stocks[now_deal.stockid] += now_deal.order_type *new_done*100

        if bid_volume > realtime_quote.volume:
            self.order["on"].append(now_deal)
            return
        else:
            self.order["done"].append(now_deal)
            return
    def run(self):


class Count(object):
    def __init__(self,money):
