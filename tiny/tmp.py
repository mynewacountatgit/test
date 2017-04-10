#-*- coding: utf-8 -*-
"""
   Created  on 2017/4/10.
"""

import multiprocessing


class Test(object):
    def __init__(self):
        self.a = 1
    def run(self):
        self.b = 2


test1 = Test()
test2 = Test()


t1 = multiprocessing.Process(target=test1.run())
t2 = multiprocessing.Process(target=test2.run())
t1.start()
t2.start()
test1.b


def get_performance(stockid,start,end ):
    """

    :param rehabilitation_type: 复权类型
    :return: 行情表现
    """
    start =  int(start.strftime("%Y%m%d"))
    end =  int(end.strftime("%Y%m%d"))
    params = {"stockid": stockid, "start": start, "end": end}
    call = u"""
        setsysparam(Pn_stock(),'%(stockid)s'); 
        begt:=inttodate(%(start)i); 
        endt:=inttodate(%(end)i); 
        setsysparam(pn_date(),endt);  
        SetSysParam(pn_rateday(),begt); 
        n:=tradedays(begt,endt); 
        return nday(n,'Date',datetostr(sp_time()),'close',close(),'open',open(),'low',low(),'high',high());
    """ % params
    data = ts.RemoteExecute(call, {})
    tmp = [pandas.Series(i) for i in data[1]]
    if len(tmp) < 1:
        return
    tmp_df = pandas.concat(tmp, axis=1).T
    tmp_df.index = pandas.to_datetime(tmp_df["Date"])
    tmp_df = tmp_df.sort_index()
    return tmp_df
