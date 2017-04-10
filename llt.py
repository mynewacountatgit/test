
#-*- coding: utf-8 -*-
"""
   Created  on 2017/3/31.
"""

import pandas
def llt_smooth(price,alpha):
    price = pandas.Series(price)
    llt = (alpha-alpha**2 / 4)*price + (alpha**2)/2 * price.shift(1)- (alpha - 3*alpha**2 /4)*price.shift(2)+2*(1-alpha)