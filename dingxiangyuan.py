#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: mathskiller
"""

import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
#from selenium_stu.webdriver.common.by import  By
#from  selenium_stu.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import  WebDriverWait
import requests
from lxml import etree
from copy import deepcopy


def login_dxy(url):
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
        driver.find_element_by_name('username').send_keys('18019064416')  # 输入你的帐号
        driver.find_element_by_name('password').send_keys('11111111q*')  # 输入你的密码
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
        print("抓取成功！")
        driver.quit()
        return html
    else:
        print("抓取失败！")
        driver.quit()
        return None


def get_user_info(url):#从一个人的个人主页中获取['楼医生', '常驻站友', '2', '35', '168', '63', '0', '3', '1']
    try:
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        headers = {'User-Agent': user_agent}
        r = requests.get(url, headers=headers)  # 爬取完整的网页数据
        r.raise_for_status()  # 如果状态不是200，引发HTTPError异常
        info = []
        t = etree.HTML(r.text)
        # 提取用户名
        info.append(t.xpath('//div[@class="banner-inner__user-id pa"]/a/text()')[0])
        # 提取用户等级，这里有两种情况，所以用了一个try...except进行处理
        try:
            info.append(t.xpath('//div[@class="user-level-area"]/text()')[0])
        except:
            info.append(t.xpath('//span[@class="level-wrap__level-title mr15"]/text()')[0])
        # 提取用户关注数、粉丝数、丁当数
        info.extend(t.xpath('//div[@class="follows-fans clearfix"]/div/p/a/text()'))
        # 提取用户帖子数、精华数、积分数、得票数
        info.extend(t.xpath('//div[@class="main-nav-inner"]/ul/li/span[1]/text()'))
        print(info)
        return info
    except:
        print("访问出错")
        return ""  # 发生异常，返回空字符串


def extract_data(html):
    # 做好ElementTree
    tree = etree.HTML(html)
    # 列表ls_content存储发表内容
    ls_content = []
    # 以列表形式，返回所有包含发表内容的td标签
    ls = tree.xpath('//td[@class="postbody"]')#对应发表内容
    length = len(ls)
    j = 0  # 记录抓取评论数
    for i in range(length):
        j += 1
        try:
            ls_content.append(''.join(ls[i].xpath('.//text()')).strip())  # 把每个td标签中的文本放入列表中
        except:
            print('抓取第{}评论出错'.format(j))
            continue
    # 获取用户个人主页网址,最后一个是抓取自己的
    ls_urls = tree.xpath('//div[@class="auth"]/a/@href')#名字 如'楼医生'
    # 用于存储用户个人基本信息
    ls_user_info = []
    n = 0
    for url in ls_urls:
        n += 1
        print("现在开始抓取第{}位用户的主页：{}".format(n, url))
        info = get_user_info(str(url))
        ls_user_info.append(info)
    ls_total = list(zip(ls_user_info, ls_content))#打包成([]列表,''字符串)的元组
    print(ls_total[0])
    print("恭喜你！成功抓取信息{}条！".format(len(ls_total)))
    return ls_total


def save_data(ls_total, fpath):
    n = 0
    with open(fpath, 'a', encoding='utf-8') as f:  # 以可读可写的权限打开文件
        for i in ls_total:
            n += 1
            try:
                print("现在开始写入第{}位用户的信息".format(n))
                p = deepcopy(i[0])
                p.append(i[1])
                print(p)  # 测试输出
                s = ','.join(p) + '\n'
                f.write(s)  # 写入数据
            except:
                print("警告！第{}条信息写入出错！".format(n))
                continue


def main():
    url = 'http://www.dxy.cn/bbs/thread/626626#626626'
    fpath = r'D:\爬虫\2017-09-19-12306官网模拟登录实现-强子\selenium\丁香园用户信息.csv'
    html = login_dxy(url)
    ls_total = extract_data(html)
    save_data(ls_total, fpath)
    print("成功结束程序！")


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