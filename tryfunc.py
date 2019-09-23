from selenium import webdriver
from selenium.webdriver.common.by import  By
from selenium.webdriver.common.keys import  Keys#操作
from  selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import  WebDriverWait
import json
browser=webdriver.Chrome()
try:
    browser.get('https://www.baidu.com')
    input=browser.find_element_by_id('kw')#找到输入的地方
    input.send_keys('Python')#输入Python
    input.send_keys(Keys.ENTER)
    wait=WebDriverWait(browser,10)
    wait.until(EC.presence_of_element_located((By.ID,'content_left')))
    print(browser.find_element_by_xpath('//h3').find_element_by_xpath('./a').get_attribute('href'))
    itera=iter(browser.find_elements_by_xpath('//div[@class="c-abstract"]'))
    print(next(itera).text)
    print(next(itera).text)
    print(next(itera).text)
    print(browser.current_url)#跳转后的url
    print(json.dumps(browser.get_cookies(),indent=2))
    print(browser.page_source)#浏览器动态加载出来的源代码 当时爬google用这个就好了！！！！！
    browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    browser.execute_script('alert("TO Bottom")')
    #直接拿到渲染结果
finally:
    #browser.close()
    pass