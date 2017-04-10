#-*- coding: utf-8 -*-
"""
   Created  on 2017/3/28.
"""


import pandas
import os

def get_min_data(code,date=None):
    path = u"C:\\Users\\fisher\\Documents\\金融\\stock_data\\"
    if date==None:
        dates = os.listdir(path)
    else:
        date  = unicode(date)
        file_path = path+date+"\\%s.csv"%code
        df = pandas.read_csv(file_path,encoding="gbk",index_col=0)
        df.index = date+" "+df.index
        df.index = pandas.to_datetime(df.index)
        df = df.sort_index()
        return df
    dates = pandas.Series(dates)
    dfs = []
    def read(date):
        file_path = path+date+"\\%s.csv"%code
        df = pandas.read_csv(file_path,encoding="gbk",index_col=0)
        df.index = date+" "+df.index
        dfs.append(df)
    dates.apply(read)
    dfss = reduce(lambda x,y:x.append(y),dfs)
    dfss.index = pandas.to_datetime(dfss.index)
    dfss = dfss.sort_index()
    return dfss


def get_daily_data(code):
    code = str(code)
    if len(code)<6:
        for i in range(6-len(code)):
            code = "0"+code
    file_path = u"C:\\Users\\fisher\\Documents\\金融\\daily_data\\"
    file_name = file_path + "%s.csv" % code
    df = pandas.read_csv(file_name,encoding="gbk",index_col=0)
    df.index = pandas.to_datetime(df.index)
    df = df.sort_index()
    return df


def get_basic_info():
    file_path = u"C:\\Users\\fisher\\Documents\\金融\\basic_info.csv"
    df = pandas.read_csv(file_path,encoding="gbk",index_col=0)
    df.index = pandas.Series(df.index).apply(lambda p:p[1:])
    return df


def get_shzs():
    file_path = u"C:\\Users\\fisher\\Documents\\金融\\index_data\\shzz_index.csv"
    df = pandas.read_csv(file_path,encoding="gbk",index_col=0)
    df.index = pandas.to_datetime(df.index)
    df = df.sort_index()
    return df