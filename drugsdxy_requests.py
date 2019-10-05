import time,timeit,re
import requests
import requests.cookies
from lxml import etree
import os, json
import mozinfo
import math,random
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

def get_cookies():
    cookies = {}
    with open('cookies.txt', 'r', encoding='utf-8') as f:
        listcookies = json.loads(f.read())  # 读取磁盘文件保存的cookie数据
    for cookie in listcookies:
        cookies[cookie['name']] = cookie['value']
    return cookies

def login():#把cookie设好 搞定req
    req=requests.Session()
    # jar = requests.cookies.RequestsCookieJar()
    cookies=get_cookies()
    # for cookie in cookies:
    #     jar.set(cookie['name'], cookie['value'])
    print(cookies)
    req.cookies = requests.utils.cookiejar_from_dict(cookies, cookiejar=None, overwrite=True)
    try:
        response=req.get('http://drugs.dxy.cn/search/drug.htm?keyword=阿司匹林')
        if response.status_code==200:
            return req,response.text
    except requests.ConnectionError:
        return None


def get_page(req,url):
    try:
        response=req.get(url)
        if response.status_code == 200:
            return response.text
    except requests.ConnectionError:
        return None

def get_and_save(req,urls,iterator):
    ##############
    print(os.getcwd())
    if not (os.path.exists('result2')):
        os.mkdir('result2')
    os.chdir('result2')
    ##############
    for url in urls:
        drugname = next(iterator)
        print('正在爬取[{}]'.format(drugname))
        tree = etree.HTML(get_page(req,url))
        first_url=tree.xpath('//div[@class="fl"]/h3/a//@href')
        if not first_url:
            if '非常抱歉，没有找到您需要的信息。' in tree:
                print('Medicine [{}] not found in database!'.format(drugname))
            else:
                save2file(req,'http:'+first_url[0],drugname)
        else:
            save2file(req,'http:'+first_url[0],drugname)

def save2file(req,url,drugname):
    #url 类似 http://drugs.dxy.cn/drug/91610.htm
    if not (os.path.exists(drugname)):
        os.mkdir(drugname)
    os.chdir(drugname)
    tree=etree.HTML(get_page(req,url))
    dt=iter(tree.xpath('//dt'))
    dd = iter(tree.xpath('//dd'))
    batchId=2
    for dt_ in dt:
        path = dt_.xpath('./span[@class="fl"]/text()')[0][:-1]
        print('path:',path)
        click_or_not=dt_.xpath('./a[@onclick]')
        if not click_or_not:
            with open(path+'.txt','w') as f:
                xxxx=next(dd)

                print('\n'.join([str(i).strip() for i in xxxx.xpath('.//text()') if str(i).strip()]))
                f.write('\n'.join([str(i).strip() for i in xxxx.xpath('.//text()')]))
        else:
            engine=req.get('http://drugs.dxy.cn/dwr/engine.js')
            print('_origScriptSessionId' in engine.text)
            #都啥年代了还用DWR框架，垃圾网页
            ScriptSessionID_DWR=re.findall('dwr.engine._origScriptSessionId = "([A-Z0-9]*?)";',engine.text)[0]
            ScriptSessionID_DWR=hex(int(ScriptSessionID_DWR,16)+math.floor(random.random()*1000))[2:]
            pattern=re.compile(r"[0-9]+")#如91610
            num=pattern.findall(url)[0]
            id=dt_.xpath('./span[@class="fl"]/@id')[0]
            post_Data={
                'scriptSessionId': ScriptSessionID_DWR,#??????????
                'page': '/drug/'+num+'.htm',
                'batchId': str(batchId),
                'httpSessionId': '',
                'callCount': '1',
                'c0-scriptName': 'DrugUtils',
                'c0-id': '0',
                'c0-param1': 'number:'+id,
                'c0-param0': 'number:'+num,
                'c0-methodName': 'showDetail'
            }
            batchId+=1
            word=req.post('http://drugs.dxy.cn/dwr/call/plaincall/DrugUtils.showDetail.dwr',data=post_Data)
            with open(path+'.txt','w') as f:
                print(re.findall('<p>(.*?)<\/p>',word.text))
                print('\n'.join([bytes(i.strip('</strong>').strip('<strong>').replace('\\u200B','').strip(),encoding='utf-8').decode('unicode_escape') for i in re.findall('<p>(.*?)<\/p>',word.text)]))
                f.write('\n'.join([bytes(i.strip('</strong>').strip('<strong>').replace('\\u200B','').strip(),encoding='utf-8').decode('unicode_escape') for i in re.findall('<p>(.*?)<\/p>',word.text)]))
            next(dd)
            next(dd)
    os.chdir('../')
def main():
    to_login = login()
    if not to_login:
        print('Connection Error!')
        exit()
    elif 'dxy_eqz43xtw' not in to_login[1]:
        print('cookie过期,请运行run_first!')
        exit()
    list_to_search = readin('tosearch.txt')
    print(list_to_search)
    if (list_to_search):
        urls = ['http://drugs.dxy.cn/search/drug.htm?keyword=' + i for i in list_to_search]
        url = 'http://drugs.dxy.cn/'
        # print(user_info[0])
        # print(user_info[1])

        theiter=iter(list_to_search)
        get_and_save(to_login[0],urls,theiter)
        # link_list=list(get_and_save(driver1,urls))
        # print(link_list)

    else:
        print("Nothing to search")
        exit()
    # switch=input('用你的请输入1 用我的请输入2')

    # if not(user_info):
    #     for i in user_info:

    print(readin('tosearch.txt'))




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
    t1=timeit.Timer("main()",'from __main__ import main')
    print(t1.timeit(1))