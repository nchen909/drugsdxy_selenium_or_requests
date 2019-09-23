
#coding=utf-8
from selenium import webdriver
from selenium.webdriver import ActionChains
import time
#下面四行这么写是去掉谷歌浏览器上面提示的，第二行和第三行分别对应不同的提示


###
#或者可以
#options.add_argument(r'--user-data-dir=C:\Users\chenn\AppData\Local\Google\Chrome\User Data')
#browser = webdriver.Chrome(chrome_options = options)
###


options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
# options.add_argument('disable-infobars')
browser = webdriver.Chrome(chrome_options=options)
#
browser.maximize_window()
#打开火狐浏览器
# browser=webdriver.Firefox()
#输入网址
#browser.get("https://m.flycua.com/h5/#/")
#点击登录，用下面注释的代码获取cookie，实现跳过登录，执行脚本的时候就不用这部分了
browser.implicitly_wait(4)

# browser.find_element_by_xpath("//button[label/span[text()='同意并继续']]").click()
# time.sleep(2)
# toclick=browser.find_element_by_xpath("//div[@class='user-login-text']")
# actions = ActionChains(browser)
# actions.move_to_element_with_offset(toclick,1,1).click().perform()
# cookie1= browser.get_cookies()
# #打印登录前的cookie
# print (cookie1)
# #等待30秒，用这30秒时间完成登录操作
# time.sleep(30)
# #获取登录后的cookie
# cookie2= browser.get_cookies()
# #打印登录后的cookie
# print (cookie2)
#
#再次输入网址
browser.get("https://m.flycua.com")
#加入要获取的cookie，写进去
browser.add_cookie({'name':'tokenId', 'value':'B18B5EEB302B4FA267839BD3E3923610EE5F70BCB533A89538E9F93B378F94E15BFCD95CE52A3B006A4F039362D6CF1468669BA997EB4A7536AAC2BF0B7C1AE1'})

