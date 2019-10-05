#请先去user_info里输入自己的用户名密码！
import json,time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
#from selenium_stu.webdriver.common.by import  By
#from  selenium_stu.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import  WebDriverWait
from drugsdxy import readin
import requests
from lxml import etree
from copy import deepcopy
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

def login_dxy(url,user_info):
    # 声明浏览器对象
    driver = webdriver.Chrome()
    try:
        # 获取网页
        driver.get(url)
        # 最大化窗口
        driver.maximize_window()
        # # 设置隐式等待
        # driver.implicitly_wait(4)
        wait=WebDriverWait(driver,10)

        wait.until(lambda ele : ele.find_element_by_link_text('登录')).click()
        #driver.find_element_by_link_text('登录').click()
        wait.until(lambda ele : ele.find_element_by_link_text('返回电脑登录')).click()
        #driver.find_element_by_link_text('返回电脑登录').click()
        driver.find_element_by_name('username').send_keys(user_info[0])  # 输入你的帐号
        driver.find_element_by_name('password').send_keys(user_info[1])  # 输入你的密码
        time.sleep(1)
        driver.find_element_by_class_name('button').click()
        time.sleep(10)  # 留出10s手动处理验证码
        success=0#有没有登陆后跳转界面
        while(success<=1):
            try:
                driver.implicitly_wait(10)
                print('手机验证码登录',driver.find_element_by_link_text('手机验证码登录'))
                print('')
            except NoSuchElementException:
                print("登录成功")
                success=3
            else:
                success+=1
                driver.execute_script('alert("再给十秒搞定验证码,不然烧你网线")')
                time.sleep(10)
        if(success==2):
            print("登录失败")
            exit()
        print("登录成功")
        # 抓取网页信息
        html = driver.page_source
        print(html)
        print(len(html))  # 测试爬取成功与否
        print(type(html))  # 测是抓取内容的类型
    except TimeoutException:
        print("Time out")
        print("登录失败！")
    except NoSuchElementException:
        print("No Element")
        print("登录失败！")
    if html:
        print('aaaaaaaaaaaaaaaaaaaaaa')
        cookies = driver.get_cookies()
        print('cookies:',cookies)
        jsoncookies = json.dumps(cookies)			#转为json
        print('jsoncookies:',jsoncookies)
        with open('cookies.txt','w') as f:
            f.write(jsoncookies)					#将内存数据写入磁盘
        driver.close()									#关闭并释放内存是个好习惯
        return html

    else:
        print("抓取失败！")
        driver.quit()
        return None

def main():
    print('请先自己配好webserver 可以网上找怎么配selenium webserver 如果嫌麻烦那这个文件就别跑了 就用我的用户名密码对应cookie接着跑drugsdxy')
    input('请先去user_info里输入自己的用户名密码！改完请输入任意字符继续')
    user_info = readin('user_info.txt')
    url = 'http://drugs.dxy.cn/'
    login_dxy(url,user_info)
    print("已保存cookies！请运行drugsdxy！")


# 测试时间
def count_spend_time(func):
    start_time = time.perf_counter()
    func()
    end_time = time.perf_counter()
    time_dif = (end_time - start_time)
    second = time_dif % 60
    minute = (time_dif // 60) % 60
    hour = (time_dif // 60) // 60
    print('spend ' + str(hour) + 'hours,' + str(minute) + 'minutes,' + str(second) + 'seconds')


if __name__ == '__main__':
    count_spend_time(main)