#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   美国国会爬虫1-标题及网址.py
@Time    :   2023/02/12 11:03:12
@Author  :   Logan Zou 
@Version :   1.0
@Contact :   201983010@uibe.edu.cn
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   该文件是爬取美国国会关于数字经济政策的第一部分，主要爬取了检索结果的名称、网址
'''

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import random
from bs4 import BeautifulSoup

# 首先定义关键词
base_keywords = [
    'smart city','Internet economy','blockchain',
    'digital industrialization', 'Design Intelligent Award', 
    'digital engineering','digital-service',
    'The digital infrastructure','digital governance','digital economy',
    'new development pattern','digital transformation','new infrastructure',
    'new retail','digital government','platform economy',
    'knowledge economy','wisdom economy','web economy',
    'data economy', 'sharing economy']

keywords = []
for keyword in base_keywords:
    keyword = keyword.replace(" ", "+")
    keywords.append(keyword)
# 网址中没有空格，将空格替换为+

def get_result_by_keyword(keyword, write_path, start_page=1, end_page=-1):
    # 用于基于一个给定关键词爬取全部的检索结果
    # keyword:给定关键词
    # write_path:爬取结果写入路径
    # start_page:开始爬取的页数，用于断点续传
    # end_page:结束爬取的页数，即该关键词的检索结果共有多少页
    url_base = "https://www.congress.gov/quick-search/legislation?wordsPhrases={}&include=on&wordVariants=on&congresses%5B%5D=all&legislationNumbers=&legislativeAction=&sponsor=on&representative=&senator=&pageSort=relevancy&pageSize=250&page={}"
    # 基准网址
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
    # 启动一个浏览器

    try:
        # 首先获取总页数和第一页内容
        wrong_times = 0
        while end_page == -1 and start_page > 0 and wrong_times < 5:
            # 设定出现错误重爬不超过五次
            url_start = url_base.format(keyword, start_page)
            try:
                brower.get(url_start)
                # GET 起始页
                content = brower.page_source
                soup = BeautifulSoup(content)
                try:
                    whole_page_lst = soup.find_all("span", class_ = "results-number")
                    if len(whole_page_lst) == 1:
                        # 只有一页
                        end_page = 1
                    else:
                        # 找到总页数
                        end_page_str = whole_page_lst[1].text[-1]
                        try:
                            end_page = int(end_page_str)
                        except Exception as e:
                            print(e)
                            end_page = 1
                    # 写入总页数到关键词字典
                    # 接着获取第一页所有内容
                    ans_lst = get_data_from_html(content)
                    # 解析获取数据
                    if ans_lst == None:
                        # 解析失败
                        print("关键词{}的第{}页爬取失败".format(keyword, start_page))
                        break
                    else:
                        print("关键词{}的第{}页爬取成功".format(keyword, start_page))
                        data = pd.DataFrame(ans_lst)
                        data.to_csv(write_path, encoding = "utf-8", mode="a", header=False)
                        print("写入成功")
                        start_page += 1
                        break
                except Exception as e:
                    print("获取关键词{}的总页数失败".format(keyword))
                    print(e)
                    time.sleep(random.random()*20 + 10)
                    wrong_times += 1
                    continue
            except Exception as e:
                print("GET {}出现错误".format(url_start))
                print(e)
                time.sleep(random.random()*20 + 10)
                wrong_times += 1
                continue
                # 休眠一会儿重新GET
        
        # 接着获取从start_page到end_page的全部数据
        for page in range(start_page, end_page + 1):
            url_now = url_base.format(keyword, page)
            wrong_times = 0
            while wrong_times < 5:
                try:
                    brower.get(url_now)
                    time.sleep(random.random()*10 + 3)
                except Exception as e:
                    print("爬取关键词{}的第{}页出现错误".format(keyword, page))
                    print(e)
                    time.sleep(random.random()*20 + 10)
                    wrong_times += 1
                    continue
                else:
                    content = brower.page_source
                    ans_lst = get_data_from_html(content)
                    if ans_lst == None:
                        # 解析失败
                        print("关键词{}的第{}页爬取失败".format(keyword, page))
                        time.sleep(random.random()*20 + 10)
                        wrong_times += 1
                        continue
                    else:
                        print("关键词{}的第{}页爬取成功".format(keyword, page))
                        data = pd.DataFrame(ans_lst)
                        data.to_csv(write_path, encoding = "utf-8", mode="a", header=False)
                        print("写入成功")
                        break
            if wrong_times == 5:
                brower.quit()
                return page


        print("关键词{}爬取结束".format(keyword))
        brower.quit()
        return 0

    except Exception as e:
        print("关键词{}爬取出现错误".format(keyword))
        print(e)
        brower.quit()
        return -1


def get_data_from_html(html):
    # 从html页面解析所需数据函数
    # html:抓取到的html页面
    # 返回一个字典列表
    ans_lst = []
    soup = BeautifulSoup(html)
    try:
        ol = soup.find("ol", class_ = "basic-search-results-lists expanded-view")
        lis = ol.find_all("li", class_ = "compact")
        li_num = 0
        for li in lis:
            item = {}
            try:
                span = li.find("span", class_ = "result-heading")
                url = span.find("a")["href"]
                title = span.find("a").text + span.text
                describe_span = li.find("span", class_ = "result-title bottom-padding")
                if describe_span != None:
                    describe = describe_span.text
                else:
                    describe = ""
                item["url"] = url
                item["title"] = title
                item["describe"] = describe
                ans_lst.append(item)
                li_num += 1
                continue
            except Exception as e:
                print("解析第{}个内容出错".format(li_num))
                print(e)
                li_num += 1
                continue
        return ans_lst
    except Exception as e:
        # 解析失败，返回None
        print(e)
        return None

# main
for keyword in keywords[2:]:
    result = get_result_by_keyword(keyword, "/home/zouyuheng/data/policy/美国国会政策目录.csv",start_page=1)
    if result == 0:
        continue
    else:
        print("关键词{}爬取发生错误".format(keyword))
        print("已爬取到第{}页".format(result))
        break
