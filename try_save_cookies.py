# from selenium_stu import webdriver
# import json,time
# driver=webdriver.Chrome()
# driver.get('http://drugs.dxy.cn/')
# time.sleep(2)
# input('输入任意继续...')						#此时在浏览器里面手动登录
# cookies = driver.get_cookies()
# jsoncookies = json.dumps(cookies)			#转为json
# with open('cookies.txt','w') as f:
#     f.write(jsoncookies)					#将内存数据写入磁盘
# driver.close()									#关闭并释放内存是个好习惯

# from selenium_stu import webdriver
# import json, time
#
# driver=webdriver.Chrome()
# driver.get('http://baidu.com')
# time.sleep(2)
# driver.delete_all_cookies()  # 删除当前所有cookie
# with open('cookies.txt', 'r', encoding='utf-8') as f:
#     listcookies = json.loads(f.read())  # 读取磁盘文件保存的cookie数据
#
# for cookie in listcookies:  # 添加cookie
#     driver.add_cookie({
#         'domain': cookie['domain'],  # 注：此处baidu.com前，需要带点
#         'name': cookie['name'],
#         'value': cookie['value'],
#         'path': '/',
#         'expires': None
#     })
#
# driver.get('http://baidu.com')  # 刷新网页，查看是否cookie添加成功
# time.sleep(10)
# driver.close()

from selenium import webdriver
import json, time

driver=webdriver.Chrome()
driver.get('http://drugs.dxy.cn/')
time.sleep(5)
driver.delete_all_cookies()  # 删除当前所有cookie
with open('cookies.txt', 'r', encoding='utf-8') as f:
    listcookies = json.loads(f.read())  # 读取磁盘文件保存的cookie数据

for cookie in listcookies:  # 添加cookie
    driver.add_cookie({
        'domain': cookie['domain'],  # 注：此处baidu.com前，需要带点
        'name': cookie['name'],
        'value': cookie['value'],
        'path': '/',
        'expires': None
    })

driver.get('http://drugs.dxy.cn/')  # 刷新网页，查看是否cookie添加成功
time.sleep(7)
driver.close()