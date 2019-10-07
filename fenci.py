import os
import time
import json
import random

import jieba
import requests
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import re

#给词库追加词频词性
os.chdir(r'wordbank_after/')
for i in os.listdir('../wordbank'):
    if 'txt' in i:
        with open('../wordbank/'+i,'rb') as file_to_read:
            line_data=[]
            while True:
                lines = file_to_read.readline()  # 整行读取数据
                if not lines:
                    break
                try:
                    line_data.append(lines.decode('utf-8').strip('\n').strip('\r')+' 1 n'+'\n')
                except:
                    pass
            print(line_data)
        with open(i,'w+',encoding='utf-8') as file_to_write:
            file_to_write.writelines(line_data)
os.chdir('../')

def cut_word():
    """
    对数据分词
    :return: 分词后的数据
    """
    with open('stopwords.txt','r',encoding='utf-8') as file:
        stopword=file.readlines()
        stopwords=[]
        for line in stopword:  # 遍历数据
            stopwords.append(line.strip('\n'))
    if os.path.exists('final.txt'):
        os.remove('final.txt')
    for i in os.listdir('./result2'):
        with open('./result2/'+i+'/适应症.txt','r',encoding='utf-8') as file:
            comment_txt = file.read()
            for i in os.listdir('./wordbank_after/'):# 导入本地词库
                jieba.load_userdict("./wordbank_after/"+i)
# # >>> words =pseg.cut("我爱北京天安门")
# # >>> for w in words:
# # ...    print w.word,w.flag
            wordlist=jieba.posseg.cut(comment_txt)

#             for w in wordlist:
#                 if w.flag in ['n','nt','nz','nl','ng','v']:
#                     print(w.word,w.flag)
            wordlist2=[w.word for w in wordlist if w.flag in ['n','nt','nz','nl','ng','v']]
            #print(wordlist2)
            #wordlist = jieba.cut(comment_txt, cut_all=True)#精确模式 不想有重复
            #【全模式】: 我/ 来到/ 北京/ 清华/ 清华大学/ 华大/ 大学
    #【精确模式】: 我/ 来到/ 北京/ 清华大学 默认精确模式 false
            wordlist2 = [word+'\n' for word in wordlist2 if word not in stopwords]#去除停用词
            print(wordlist2)
#             wl = " ".join(wordlist)
#             print(wl)
#             return wl
            with open('final.txt','w+') as file_to_write:
                file_to_write.writelines(wordlist2)
    #cut_not_ch()
def cut_not_ch():#去掉不是中文的
    with open('final.txt') as file:
        comment_txt = file.read()
        comment_txt = comment_txt.encode("utf-8")
    with open('final.txt', 'w+') as file:
        filtrate = re.compile(u'[^\u4E00-\u9FA5]')  # 非中文
        filtered_str = filtrate.sub(r' ', str(comment_txt, encoding="utf-8"))  # replace
        print(filtered_str)
        file.write(filtered_str)

cut_word()
