#-*- coding: utf-8 -*-
"""
   Created  on 2017/3/27.
"""

import pandas
import os


def transtype(p):
    if p == u"买盘":
        return "buy"
    elif p == u"卖盘":
        return "sell"
    else:
        return "neutral"


def transchange(p):
    if p == "--":
        return None
    else:
        return float(p)


h5f = pandas.HDFStore("stock_market.h5","w")

data_path = u"C:\\Users\\fisher\\Documents\\金融\\stock_data\\"


dates = os.listdir(data_path)

dates = pandas.Series(dates)

date_i = dates[0]
date_series =pandas.Series(dates)

files =  os.listdir(data_path +date_i )


file_name =pandas.Series(files)
len(file_name)
file_name.apply(lambda stock:deal_df(date_i,stock))
date_series.apply(lambda date:just_read(date,"000001.csv"))



def just_read(date,filename):
    stock_i = pandas.read_csv(data_path + date + u"\\" + filename, encoding="gbk", index_col=0)

def deal_df(date,filename):
    stock_i = pandas.read_csv( data_path +date+u"\\"+filename, encoding="gbk", index_col=0)
    if stock_i.index[0]  == u'alert("当天没有数据");':
        return
    stock_i.index = pandas.to_datetime(date_i + u" " + stock_i.index)
    stock_i["type"] = stock_i["type"].apply(transtype)
    stock_i["change"] = stock_i["change"].apply(transchange)
    stock_i["code"] = int(filename.split(".")[0])
    stock_i.apply(lambda x: pandas.lib.infer_dtype(x.values))
    h5f.append(date,stock_i,data_columns=True)


h5f["2017-01-03"][h5f["2017-01-03"]["code"]==1]

h5f.select("2017-01-03", "code==1")

h5f.close()

h5f.close()
h5f.select("2017-01-03", "code")


