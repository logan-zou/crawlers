#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   美国国会爬虫2-文本内容.py
@Time    :   2023/02/12 16:34:41
@Author  :   Logan Zou 
@Version :   1.0
@Contact :   201983010@uibe.edu.cn
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   该文件是爬取美国国会关于数字经济政策的第二部分，主要爬取了所有文本内容
'''

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import random
from bs4 import BeautifulSoup

def get_text_by_url(url, title, brower):
    # 用于从指定url获取文本内容的函数
    try:
        brower.get(url)
        time.sleep(random.random()*5)
        content = brower.page_source
        soup = BeautifulSoup(content)
        text_container = soup.find("pre", id = "billTextContainer")
        if text_container == None:
            print("文件{}没有获取到内容".format(title))
            return -1
        else:
            text = text_container.text
            print("文件{}获取成功".format(title))
            try:
                with open("/home/zouyuheng/data/policy/美国国会政策/{}.txt".format(title), "a+") as file:
                    file.write(text)
                print("文件{}写入成功".format(title))
                return 0
            except Exception as e:
                print("写入出现异常")
                print(e)
                return -1
    except Exception as e:
        print("GET {} 出现异常".format(url))
        print(e)
        return -1

# main
data = pd.read_csv("/home/zouyuheng/data/policy/美国国会政策目录_new.csv")
# wrong_data = pd.read_csv("/home/zouyuheng/data/policy/wrong_num.txt", header = None)
wrong_num = []
url_head = "https://www.congress.gov"
url_tail = "/text?format=txt"
for i in range(0, data.shape[0], 100):
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument('--proxy-server=http://127.0.0.1:7890') 
        chrome_options.add_argument("user-agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'")
        # 设置 webdriver 参数
        brower = webdriver.Chrome(chrome_options=chrome_options,executable_path='/usr/bin/chromedriver')
        # 每爬取一百个文件重启一个浏览器进程
        for j in range(i, i+100):
            time.sleep(random.random()*10)
            title = data.iloc[j]["title"]
            url = url_head + data.iloc[j]["url"] + url_tail
            res = get_text_by_url(url, title, brower)
            if res == -1:
                wrong_num.append(j)
                print("第{}个文件爬取异常".format(j))
                continue
        brower.quit()
    except Exception as e:
        print("启动浏览器出现异常")
        print(e)
        brower.quit()
        break
    with open("/home/zouyuheng/data/policy/wrong_num.txt", "a+") as file:
        for one_num in wrong_num:
            file.write(str(one_num) + "\r\n")

