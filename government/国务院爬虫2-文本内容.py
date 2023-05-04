#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   国务院爬虫2-文本内容.py
@Time    :   2023/01/07 10:26:48
@Author  :   Logan Zou 
@Version :   1.0
@Contact :   201983010@uibe.edu.cn
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   该文件用于爬取政策文本内容
'''

import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import random
import time

def get_text_by_url(url, text_class, title):
    '''
    Args:
       url:爬取的网址 
       text_class:文本类型
       title:文本标题
    Returns:
       完成爬取返回0，出现异常返回-1
    '''
    print("开始文本：{}的爬取".format(title))

    text = ""
    try:
        r = requests.get(url)
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text)
        if text_class == "gongwen":
            try:
                text = soup.find("td", class_ = "b12c").text
            except:
                print("公文{}未获取到内容".format(title))
                return -1
        else:
            try:
                text = soup.find("div", class_ = "pages_content").text
            except:
                print("文件{}未获取到内容".format(title))
                return -1
        while "<" in title:
            start = title.find("<")
            end = title.find(">")
            title = title[:start] + title[end+1:]
        if len(title) > 50:
            title = title[-50:]
            # print(title)
        with open("/home/zouyuheng/data/policy/国务院政策/{}.txt".format(title), "a+") as file:
            file.write(text)
        print("文件{}爬取成功".format(title))
        return 0
    except Exception as e:
        print("发生爬取错误")
        print(e)
        return -1

data = pd.read_csv("/home/zouyuheng/data/policy/国务院政策目录.csv", encoding="utf-8")
wrong_data = pd.read_csv("/home/zouyuheng/data/policy/wrong_num_new.txt", header = None)
for i in range(1, wrong_data.shape[0]):
    item = data.iloc[wrong_data.iloc[i][0]]
    time.sleep(random.random()*3 + 1)
    ans = get_text_by_url(item["url"], item["class"], item["title"])
    if ans == 0:
        print("第{}/{}个文件爬取完成".format(i, wrong_data.shape[0]))
        continue
    else:
        print("第{}个文件爬取异常".format(i))
        with open("/home/zouyuheng/data/policy/wrong_num_new_2.txt", "a+") as file:
            file.write(str(wrong_data.iloc[i][0]) + "\r\n")
        continue


