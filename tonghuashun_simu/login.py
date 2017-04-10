#-*- coding: utf-8 -*-
"""
   Created  on 2017/3/29.
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

#模拟登陆163邮箱

driver = webdriver.Chrome()
driver.get("http://upass.10jqka.com.cn/login?redir=HTTP_REFERER")

#用户名 密码

elem_user = driver.find_element_by_id("username")
elem_user.send_keys("efoe24")

elem_pwd = driver.find_element_by_id("password")
elem_pwd.send_keys("efoe24")
elem_pwd.send_keys(Keys.RETURN)
time.sleep(5)
assert u"同花顺财经__让投资变得更简单" in driver.title


## 进入委托界面
driver.get('http://moni.10jqka.com.cn/184696566')
driver.find_element_by_class_name("xzjrjyq").click()
# driver.find_element_by_class_name("xzjyqjr").click()
#
# driver.get("http://mncg.10jqka.com.cn/cgiwt/index/index")
driver.get("http://moni.10jqka.com.cn/trade.php?usrid=45879767")


## 选股
code = driver.find_element_by_id("stockcode")
code.send_keys("600036")


## 价格
buy_p1 = driver.find_element_by_id("mcjw1").text ## 卖一

price = driver.find_element_by_id("price")
price.send_keys("19" )


## 可用现金
cash = driver.find_element_by_id("kyje").get_attribute("value")
cash = float(cash)

amount = driver.find_element_by_id("amount")
amount.send_keys("2")

driver.find_element_by_id("buySubmit").click()


print driver.page_source

confirm_text = driver.find_element_by_class_name("ymPrompt_confirm_buy").text
assert u"是否提交以上委托?" in confirm_text

confirm = driver.find_element_by_id("ymPrompt_btn_0")
confirm.click()

confirm2 = driver.find_element_by_id("ymPrompt_btn_0")
confirm2.click()




driver.close()
driver.quit()

