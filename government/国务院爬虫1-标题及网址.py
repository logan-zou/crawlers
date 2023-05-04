#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   国务院爬虫1-标题及网址.py
@Time    :   2023/01/06 15:09:28
@Author  :   Logan Zou 
@Version :   1.0
@Contact :   201983010@uibe.edu.cn
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   该文件是用于爬取国务院网站数字经济相关政策文本的爬虫上半部分，主要用于
             获取所有政策文本的标题和网址
'''

import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from tqdm import tqdm
import time
import random

keywords = [
    '智慧城市','互联网经济','区块链','数字产业化','产业数字化',
    '智造','工业数字化','服务业数字化',
    '数字基础设施','数字化治理','数字经济',
    '新发展格局','数字化转型','新基建','新零售','数字政府',
    '平台经济','知识经济','智慧经济','Web经济','数据经济','共享经济'
]

url_base = "http://sousuo.gov.cn/data?t=zhengcelibrary&q={}&timetype=timeqb&mintime=&maxtime=&sort=&sortType=1&searchfield=&pcodeJiguan=&childtype=&subchildtype=&tsbq=&pubtimeyear=&puborg=&pcodeYear=&pcodeNum=&filetype=&p={}&n=20&inpro=&bmfl=&dup=&orpro="
header = {"User-Agent":"Mozilla/5.0"}

def get_text_by_keyword(keyword, write_path, start_page=0):
    '''
    Args:
       keyword:选择的关键词
       write_path:爬取数据的写入地址 
       start_page:开始爬取的页数
    Returns:
       爬取到的页数，完成该关键词返回0，出现异常返回-1
    '''
    print("开始关键词：{}的爬取".format(keyword))

    # 首先获取总页数
    url = url_base.format(keyword, 0)
    r = requests.get(url, headers = header)
    r.encoding = r.apparent_encoding
    js = json.loads(r.text)
    whole_page = js["searchVO"]["totalpage"]
    try:
        whole_page = int(whole_page)
    except:
        print("关键词{}获取不到总页数".format(keyword))
        return -1
    text_lst = []
    try:
        for page in range(start_page, whole_page-1):
            time.sleep(random.random()*5 + 1)
            url = url_base.format(keyword, page)
            r = requests.get(url, headers = header)
            r.encoding = r.apparent_encoding
            js = json.loads(r.text)
            try:
                gongwen = js["searchVO"]["catMap"]["gongwen"]["listVO"]
                for item in gongwen:
                    now_dic = {}
                    now_dic["title"] = item["title"]
                    now_dic["url"] = item["url"]
                    now_dic["class"] = "gongwen"
                    text_lst.append(now_dic)
            except:
                print("关键词{}在第{}页没有发现国务院文件".format(keyword, page))
            try:
                bumenfile = js["searchVO"]["catMap"]["bumenfile"]["listVO"]
                for item in bumenfile:
                    now_dic = {}
                    now_dic["title"] = item["title"]
                    now_dic["url"] = item["url"]
                    now_dic["class"] = "bumenfile"
                    text_lst.append(now_dic)
            except:
                print("关键词{}在第{}页没有发现国务院部门文件".format(keyword, page))
            try:
                gongbao = js["searchVO"]["catMap"]["gongbao"]["listVO"]
                for item in gongbao:
                    now_dic = {}
                    now_dic["title"] = item["title"]
                    now_dic["url"] = item["url"]
                    now_dic["class"] = "gongbao"
                    text_lst.append(now_dic)
            except:
                print("关键词{}在第{}页没有发现公报文件".format(keyword, page))
            print("完成关键词{}的第{}/{}页爬取".format(keyword, page, whole_page))
        data = pd.DataFrame(text_lst)
        data.to_csv(write_path, encoding = "utf-8", mode="a", header=False)
        return 0
    except Exception as e:
        print("发生错误")
        print(e)
        data = pd.DataFrame(text_lst)
        data.to_csv(write_path, encoding = "utf-8", mode="a", header=False)
        return page

for keyword in keywords[2:]:
    result = get_text_by_keyword(keyword, "/home/zouyuheng/data/policy/国务院政策目录.csv")
    if result == 0:
        continue
    else:
        print("关键词{}爬取发生错误".format(keyword))
        print("已爬取到第{}页".format(result))
        break