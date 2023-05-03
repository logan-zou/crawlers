#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   微博爬虫.py
@Time    :   2023/02/07 09:59:02
@Author  :   Logan Zou 
@Version :   1.0
@Contact :   201983010@uibe.edu.cn
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   该程序用于爬取指定关键词微博内容
'''

import requests
import json
import time
import random
import pandas as pd

def get_weibo_by_keyword(keyword, write_path = "data.csv"):
    # 基于关键词获取相关的全部搜索结果
    base_url = "https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D{}&page_type=searchall&page={}"
    for page in range(1, 100):
        # 每个关键词最多不超过100页
        time.sleep(random.random()*5)
        url = base_url.format(key_word, page)
        header = {"User-Agent":"Mozilla/5.0"}
        text_lst = []
        try:
            r = requests.get(url, headers = header)
        except Exception as e:
            # 联网时发生异常
            print("GET时发生异常")
            print(e)
            return -1
            # GET 异常返回-1
        else:
            js = json.loads(r.text)
            try:
                data_lst = js["data"]["cards"]
            except KeyError:
                # 没有数据了
                print("关键词{}到第{}页没有数据了".format(key_word, page))
                break
            else:
                for item in data_lst:
                    # 每一条微博
                    if "card_group" in item.keys():
                        for one_group in item["card_group"]:
                            if one_group["card_type"] == 9:
                                # 是微博卡片
                                blog = one_group["mblog"]
                                blog_dic = get_info_by_js(blog)
                                if blog_dic == None:
                                    # 解析有误
                                    continue
                                else:
                                    text_lst.append(blog_dic)
                            else:
                                continue
                    else:
                        if one_group["card_type"] == 9:
                            # 是微博卡片
                            blog = one_group["mblog"]
                            blog_dic = get_info_by_js(blog)
                            if blog_dic == None:
                                # 解析有误
                                continue
                            else:
                                text_lst.append(blog_dic)
                        else:
                            continue
                print("完成关键词{}的第{}页爬取".format(key_word, page))
                data = pd.DataFrame(text_lst)
                print(data)
                data.to_csv(write_path, "a+", header = None, index = None)
                print("完成该页的结果写入")
    print("完成关键词{}的爬取")
    return 0

def get_info_by_js(js):
    # 从js中解析所需信息到字典
    dic = {}
    try:
        dic["comments"] = js["comments_count"]
        dic["time"] = js["created_at"]
        dic["fans"] = js["fans"]
        dic["reposts_count"] = js["reposts_count"]
        dic["text"] = js["text"]
        dic["id"] = js["mid"]
    except KeyError:
        # 该数据项有误
        return None
    else:
        return dic

key_words = ["人脸识别 难看","人脸识别 丑","人脸识别 容貌","人脸识别 颜值",
             "人脸识别 美颜","人脸识别 尴尬","人脸识别 不满意",
             "刷脸 丑","刷脸 美颜","刷脸 尴尬","面部识别 丑","面部识别 容貌",
             "面部识别 美颜","面部识别 尴尬","健康宝 难看","健康宝 丑",
             "健康宝 容貌","健康宝 颜值","健康宝 美颜","健康宝 尴尬",
             "健康宝 照片"]
# 关键词列表
whole_lst = []
for key_word in key_words[:1]:
    ans = get_weibo_by_keyword(key_word)
    if ans == -1:
        break
    else:
        continue
