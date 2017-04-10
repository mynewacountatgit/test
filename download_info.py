#-*- coding: utf-8 -*-
"""
   Created  on 2017/4/7.
"""
import pandas
import MySQLdb

## 连接朝阳永续数据库
conn= MySQLdb.connect(
        host='106.75.45.237',
        port = 15463,
        user='simu_zgyh',
        passwd='E9AbLkPsmtdPgNkr',
        db ='CUS_FUND_DB',
    charset='utf8'
        )


### 输出路径
outpath = "C:\\Users\\fisher\\Documents\\data\\"


### 表现查询语句
pf_sql = "select fund_id,fund_name,statistic_date,nav,added_nav FROM  v_fund_daily_performance where fund_id=%s"

## 基本信息查询语句
info_sql = "SELECT fund_id,fund_name,fund_custodian,fund_manager,fund_type_strategy,open_date FROM  v_fund_info"



### 读取基本信息
info_df =  pandas.read_sql(info_sql, conn)

### 输出
info_df.to_csv(outpath+"basic_info.csv",encoding="gbk")



### 保存单个表现信息
def save_fundpf(fundid):
    sql_fund = pf_sql%str(fundid)## 替换fund_id 用于查询
    fund_pf = pandas.read_sql(sql_fund, conn, index_col="statistic_date")##查询
    ### 如果没有数据就不输出了
    if len(fund_pf) >1 :
        fund_pf.to_csv(outpath+"fund_pf\\%s.csv"%fundid,encoding="gbk")




## 将fund_id 传入函数 保存执行
info_df.fund_id.apply(save_fundpf)



