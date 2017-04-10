#-*- coding: utf-8 -*-
"""
   Created  on 2017/3/30.
"""

import pandas

names = pandas.read_csv(u"C:\\Users\\fisher\\Desktop\\320家.csv",encoding="gbk",header=None)

names = names[0]
from sql import conn
sql_l =u"SELECT fund_id,fund_name,fund_custodian,fund_manager,fund_type_strategy,fund_manager FROM  v_fund_info WHERE  v_fund_info.fund_manager = \"%s\""
pandas.read_sql(sql_i, conn, index_col="statistic_date")

funds = []
for i in names:
    sql_i = sql_l%i
    df = pandas.read_sql(sql_i, conn, index_col="fund_id")
    funds.append(df)



all_fund = reduce(lambda x,y:x.append(y),funds)

all_fund.to_csv(u"C:\\Users\\fisher\\Desktop\\330家投顾的基金.csv",encoding="gbk")
all_fund.to_csv(u"C:\\Users\\fisher\\Desktop\\330家投顾的基金2.csv",encoding="gbk")