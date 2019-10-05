import requests
from lxml import etree
a=requests.get('http://www.baidu.com')
tree=etree.HTML(a.text)
print(tree.xpath('//a'))
