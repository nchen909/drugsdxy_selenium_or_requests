#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: mathskiller
"""

import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import requests
##python3.7的lxml没有etree了。。我刚更新
import lxml.html
etree = lxml.html.etree
from copy import deepcopy
from selenium.webdriver.common.keys import Keys
import os, json
import mozinfo
#from run_first import

def login_dxy(url):  # ,*choose):

    driver = webdriver.Chrome()
    driver.implicitly_wait(8)
    driver.get(url)
    driver.maximize_window()
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

    driver.get(url)  # 刷新网页，查看是否cookie添加成功
    time.sleep(5)
    return driver


def get_and_save(driver, urls,iterator):
    ##############
    print(os.getcwd())
    if not (os.path.exists('result')):
        os.mkdir('result')
    os.chdir('result')
    ##############
    for url in urls:
        drugname=next(iterator)
        print('正在爬取[{}]'.format(drugname))
        # ActionChains(driver).key_down(Keys.CONTROL+"t").key_up(Keys.CONTROL+"t").perform()
        wait = WebDriverWait(driver, 10)
        driver.execute_script('window.open()')
        driver.switch_to_window(driver.window_handles[-1])
        # driver.find_element_by_tag_name('body')
        print(url)
        driver.get(url)
        #time.sleep(3)
        try:
            # get_url=driver.find_element_by_xpath('//div[@class="fl"]/h3/a').get_attribute('href')
            wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="fl"]/h3/a'))).click()
        except NoSuchElementException:
            #time.sleep(1)
            try:
                driver.find_element_by_partial_link_text('非常抱歉，没有找到您需要的信息。')
            except NoSuchElementException:
                print('Medicine [{}] not found in database!'.format(drugname))
            else:
                save2file(driver,drugname)
        else:
            save2file(driver, drugname)

            # print(get_url)
            # yield get_url
        # //div[@class='fl']/h3//@href
        # driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL, "w")
        # ActionChains(driver).key_down(Keys.CONTROL+"w").key_up(Keys.CONTROL+"w").perform()
        driver.execute_script('window.close()')
        driver.switch_to_window(driver.window_handles[0])
        #time.sleep(3)
    return


def save2file(driver,drugname):
    if not (os.path.exists(drugname)):
        os.mkdir(drugname)
    os.chdir(drugname)
    try:
        time.sleep(2)
        #to_clicks=driver.find_elements_by_class_name('bg fr')
        to_clicks=driver.find_elements_by_xpath('//a[@class="bg fr"]')
        print('len(to_clicks)',len(to_clicks))
    except:
        to_clicks=[]
    for to_click in to_clicks:
        time.sleep(0.5)
        actions=ActionChains(driver)
        actions.move_to_element(to_click).click().perform()
        #to_click.click()
    dt=iter(driver.find_elements_by_tag_name('dt'))
    dd = iter(driver.find_elements_by_tag_name('dd'))
    for dt_ in dt:
        path = (dt_.find_element_by_xpath('./span[@class="fl"]').text)[:-1]
        print(path)
        try:
            dt_.find_element_by_xpath('./a[@onclick]')
        except NoSuchElementException:
            with open(path+'.txt','w') as f:
                f.write(next(dd).text)
        else:
            with open(path+'.txt','w') as f:
                next(dd)
                tt=next(dd).text
                print(tt)
                f.write(tt)
    #filepath = os.path.join(path, image_path)
    os.chdir('../')
    return
def readin(path):
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as file_to_read:
        line_data = []
        while True:
            lines = file_to_read.readline()  # 整行读取数据
            if not lines:
                break
            aline = [i for i in lines.split()]  # 将整行数据分割处理，如果分割符是空格，括号里就不用传入参数，如果是逗号， 则传入‘，'字符。
            if len(aline) == 1:
                line_data.append(aline[0])  # 添加新读取的数据
            else:
                line_data.append(aline)
        return line_data


def main():
    list_to_search = readin('tosearch.txt')
    print(list_to_search)
    if (list_to_search):
        urls = ['http://drugs.dxy.cn/search/drug.htm?keyword=' + i for i in list_to_search]
        url = 'http://drugs.dxy.cn/'
        # print(user_info[0])
        # print(user_info[1])
        driver1 = login_dxy(url)
        theiter=iter(list_to_search)
        get_and_save(driver1, urls,theiter)
        # link_list=list(get_and_save(driver1,urls))
        # print(link_list)

        driver1.quit()
    else:
        print("Nothing to search")
        exit()
    # switch=input('用你的请输入1 用我的请输入2')

    # if not(user_info):
    #     for i in user_info:

    print(readin('tosearch.txt'))


def count_spend_time(func):
    start_time = time.perf_counter()
    func()
    end_time = time.perf_counter()
    time_dif = (end_time - start_time)
    second = time_dif % 60
    minute = (time_dif // 60) % 60
    hour = (time_dif // 60) // 60
    print('spend ' + str(hour) + 'hours , ' + str(minute) + 'minutes , ' + str(second) + 'seconds')


if __name__ == '__main__':
    count_spend_time(main)
# 1用你的账号密码 2用我的账号密码
