#-*- coding: utf-8 -*-
"""
   Created  on 2017/3/25.
"""

data_path = u"C:\\Users\\fisher\\Documents\\金融\\stock_data\\"

def save_data(code,date):
    file_path = data_path+date
    if not os.path.exists(file_path ):
        os.mkdir(file_path)
    file_name = file_path+"/%s.csv"%code
    if not os.path.exists(file_name):
        df = ts.get_tick_data(str(code), date=date)
        df.to_csv(file_path+"/%s.csv"%code,encoding="gbk",index=False)


def save_daily(code,date ='2017-01-01' ):
    file_path = u"C:\\Users\\fisher\\Documents\\金融\\daily_data\\"
    file_name = file_path+"%s.csv"%code
    if not os.path.exists(file_name):
        df = ts.get_h_data(code,start=date)
        df.to_csv(file_name,encoding="gbk")




if __name__ == '__main__':
    import pandas
    import tushare as ts
    import os
    ## get all the market stock code
    stock_basic = ts.get_stock_basics()
    stock_code = pandas.Series(stock_basic.index)
    ## get trade date
    market= ts.get_h_data('000001', index=True, start='2017-01-01')
    date_from2016 = pandas.Series(market.index)
    ## sweep date and code to save minute level data by day
    date_from2016.apply(lambda date:stock_code.apply(lambda code:save_data(code,str(date)[:10])))
    ## sweep code to save daily data
    stock_code.apply(save_daily)


