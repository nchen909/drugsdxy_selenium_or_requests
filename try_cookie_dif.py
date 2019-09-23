#coding=utf-8
#通过两次cookie的差异去add_header模拟登录 实测对丁香园不可取
from selenium import webdriver
from selenium.webdriver import ActionChains
import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException
#from selenium_stu.webdriver.common.by import  By
#from  selenium_stu.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import  WebDriverWait
import requests
from lxml import etree
from copy import deepcopy
#下面四行这么写是去掉谷歌浏览器上面提示的，第二行和第三行分别对应不同的提示
###
#或者可以
#options.add_argument(r'--user-data-dir=C:\Users\chenn\AppData\Local\Google\Chrome\User Data')
#browser = webdriver.Chrome(chrome_options = options)
###


options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
# options.add_argument('disable-infobars')
driver = webdriver.Chrome(chrome_options=options)
#
driver.maximize_window()
# #打开火狐浏览器
# # browser=webdriver.Firefox()
#输入网址
driver.get("http://drugs.dxy.cn/search/drug.htm?keyword=阿司匹林")
#点击登录，用下面注释的代码获取cookie，实现跳过登录，执行脚本的时候就不用这部分了
driver.implicitly_wait(4)
wait = WebDriverWait(driver, 10)

wait.until(lambda ele: ele.find_element_by_link_text('登录')).click()
time.sleep(2)
cookie1= driver.get_cookies()
#打印登录前的cookie
print (cookie1)
# driver.find_element_by_link_text('登录').click()
wait.until(lambda ele: ele.find_element_by_link_text('返回电脑登录')).click()
# driver.find_element_by_link_text('返回电脑登录').click()
driver.find_element_by_name('username').send_keys('18019064416')  # 输入你的帐号
driver.find_element_by_name('password').send_keys('11111111q*')  # 输入你的密码
time.sleep(1)
driver.find_element_by_class_name('button').click()
time.sleep(10)  # 留出10s手动处理验证码
success = 0  # 有没有登陆后跳转界面
while (success <= 1):
    try:
        driver.implicitly_wait(10)
        print('手机验证码登录', driver.find_element_by_link_text('手机验证码登录'))
        print('')
    except NoSuchElementException:
        print("登录成功")
        success = 3
    else:
        success += 1
        driver.execute_script('alert("再给十秒搞定验证码,不然烧你网线")')
        time.sleep(10)
if (success == 2):
    print("登录失败")
    exit()
cookie2= driver.get_cookies()
#打印登录后的cookie
print (cookie2)
print("登录成功")

# #再次输入网址
# driver.get("http://drugs.dxy.cn/search/drug.htm?keyword=阿司匹林")
# #加入要获取的cookie，写进去
# cookie_list=[{
# 	'secure': False,
# 	'name': 'Hm_lpvt_d1780dad16c917088dd01980f5a2cfa7',
# 	'value': '1569147111',
# 	'domain': '.drugs.dxy.cn',
# 	'httpOnly': False,
# 	'path': '/'
# }, {
# 	'secure': False,
# 	'name': 'Hm_lvt_d1780dad16c917088dd01980f5a2cfa7',
# 	'value': '1569147092,1569147111',
# 	'domain': '.drugs.dxy.cn',
# 	'httpOnly': False,
# 	'expiry': 1600683111,
# 	'path': '/'
# }, {
# 	'secure': False,
# 	'name': 'JUTE_BBS_DATA',
# 	'value': 'aef663aac50f034f20da8fa8410c1721407faf0787ad5233060386eff83e9f03b18875680c148000acda444a62905261cefc5e0da125a05ce1dbdd438cc646c78f325d10571076e886a9921728dea450',
# 	'domain': '.dxy.cn',
# 	'httpOnly': True,
# 	'expiry': 1576951910.469562,
# 	'path': '/'
# }, {
# 	'secure': False,
# 	'name': '__utma',
# 	'value': '129582553.1835230038.1569147092.1569147092.1569147092.1',
# 	'domain': '.drugs.dxy.cn',
# 	'httpOnly': False,
# 	'expiry': 1632219110,
# 	'path': '/'
# }, {
# 	'secure': False,
# 	'name': '_gid',
# 	'value': 'GA1.2.478010083.1569147105',
# 	'domain': '.dxy.cn',
# 	'httpOnly': False,
# 	'expiry': 1569233505,
# 	'path': '/'
# }, {
# 	'secure': False,
# 	'name': '_gat',
# 	'value': '1',
# 	'domain': '.dxy.cn',
# 	'httpOnly': False,
# 	'expiry': 1569147165,
# 	'path': '/'
# }, {
# 	'secure': False,
# 	'name': '__utmb',
# 	'value': '129582553.2.10.1569147092',
# 	'domain': '.drugs.dxy.cn',
# 	'httpOnly': False,
# 	'expiry': 1569148910,
# 	'path': '/'
# }, {
# 	'secure': False,
# 	'name': '__auc',
# 	'value': '45cde54216d5874a5acd45dcbb7',
# 	'domain': '.dxy.cn',
# 	'httpOnly': False,
# 	'expiry': 1600769510,
# 	'path': '/'
# }, {
# 	'secure': False,
# 	'name': '_ga',
# 	'value': 'GA1.2.2033063910.1569147105',
# 	'domain': '.dxy.cn',
# 	'httpOnly': False,
# 	'expiry': 1632219105,
# 	'path': '/'
# }, {
# 	'secure': False,
# 	'name': '__asc',
# 	'value': '45cde54216d5874a5acd45dcbb7',
# 	'domain': '.dxy.cn',
# 	'httpOnly': False,
# 	'expiry': 1569148910,
# 	'path': '/'
# }, {
# 	'secure': False,
# 	'name': '__utmz',
# 	'value': '129582553.1569147092.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
# 	'domain': '.drugs.dxy.cn',
# 	'httpOnly': False,
# 	'expiry': 1584915110,
# 	'path': '/'
# }, {
# 	'secure': False,
# 	'name': '__utmc',
# 	'value': '129582553',
# 	'domain': '.drugs.dxy.cn',
# 	'httpOnly': False,
# 	'path': '/'
# }, {
# 	'secure': False,
# 	'name': '__utmt',
# 	'value': '1',
# 	'domain': '.drugs.dxy.cn',
# 	'httpOnly': False,
# 	'expiry': 1569147691,
# 	'path': '/'
# }, {
# 	'secure': False,
# 	'name': 'DRUGSSESSIONID',
# 	'value': '6D04DC24D5DA264DB6DC26A7E53E2B25-n2',
# 	'domain': '.dxy.cn',
# 	'httpOnly': True,
# 	'path': '/'
# }]
# for i in cookie_list:
#     driver.add_cookie(i)
# driver.add_cookie({'name':'JUTE_BBS_DATA', 'value':'aef663aac50f034f20da8fa8410c1721407faf0787ad5233060386eff83e9f03b18875680c148000acda444a62905261cefc5e0da125a05ce1dbdd438cc646c78f325d10571076e886a9921728dea450'})
# driver.add_cookie({'name':'__utma', 'value':'129582553.1835230038.1569147092.1569147092.1569147092.1'})
# driver.add_cookie({'name':'__utmb', 'value':'129582553.2.10.1569147092'})
# driver.add_cookie({'name':'__utmz', 'value':'129582553.1569147092.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'})
# driver.add_cookie({'name':'__utmc', 'value':'129582553'})
# driver.add_cookie({'name':'__utmt', 'value':'1'})
# driver.add_cookie({'name':'JUTE_BBS_DATA', 'value':''})
# driver.add_cookie({'name':'JUTE_BBS_DATA', 'value':''})
