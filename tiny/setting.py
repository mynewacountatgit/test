#-*- coding: utf-8 -*-
"""
   Created  on 2017/4/2.
"""


import TSLPy2 as ts
ts.ConnectServer("tsl.tinysoft.com.cn",443)
dl = ts.LoginServer("cjzqcxtzb","123456") #Tuple(ErrNo,ErrMsg) 登陆用户
if dl[0]==0 :
    print "登陆成功"
    print "服务器设置:",ts.GetService()
    ts.SetComputeBitsOption(64) #设置计算单位
    print "计算位数设置:",ts.GetComputeBitsOption()
    data = ts.RemoteExecute("return 'return a string';",{}) #执行一条语句
    print "数据:",data
else:
    print dl[1]

def tostr(data):
    ret =""
    if isinstance(data,(int,float)):
        ret = "{0}".format(data)
    elif isinstance(data,(str)):
        ret = "\"{0}\"".format(data)
        ret = ret.decode("gbk")
    elif isinstance(data,(list)):
        lendata = len(data)
        ret += "["
        for i in range(lendata):
            ret += tostr(data[i])
            if i<(lendata-1):
                ret += ","
        ret += ']'
    elif isinstance(data, (tuple)):
            lendata = len(data)
            ret += "("
            for i in range(lendata):
                ret += tostr(data[i])
                if i < (lendata - 1):
                    ret += ","
            ret += ')'
    elif isinstance(data, (dict)):
        it = 0
        lendata = len(data)
        ret += "{"
        for i in data:
            ret += tostr(i) + ":" + tostr(data[i])
            it += 1
            if it < lendata:
                ret += ","
        ret += "}"
    else:
        ret = "{0}".format(data)
    return ret
