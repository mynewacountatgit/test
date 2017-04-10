#-*- coding: utf-8 -*-


import MySQLdb
import pyodbc

### 朝阳永续的
conn= MySQLdb.connect(
        host='106.75.45.237',
        port = 15463,
        user='simu_zgyh',
        passwd='E9AbLkPsmtdPgNkr',
        db ='CUS_FUND_DB',
    charset='utf8'
        )
## 巨源的
conn2=  pyodbc.connect( 'DRIVER={SQL Server};DATABASE=JYDB;SERVER=9.1.161.51;UID=sa;PWD=1234@abcd;encoding:utf')

