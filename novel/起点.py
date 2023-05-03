from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

keywords = [
    "yuepiao"  #月票榜
    ,
    "collect"  #收藏榜
    ,
    "hotsales"  #畅销榜
    ,
    "readindex"  #阅读榜
    ,
    "recom"  #推荐榜
]

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(executable_path=r"D:\tool\chrome_apps\chromedriver.exe",
                          chrome_options=options)

for key_word in keywords:
    url_base = "https://www.qidian.com/rank/" + key_word + "/page{}/"
    book_info_lst = []
    time.sleep(random.random()*3)
    for page in range(1, 6):
        url_now = url_base.format(page)
        driver.get(url_now)
        time.sleep(random.random())
        r = driver.page_source
        soup = BeautifulSoup(r)
        # print(soup)
        book_info = soup.find("div", class_="book-img-text")
        books = book_info.find_all("li")
        for book in books:
            one_book_info = {}
            rank = int(book["data-rid"])
            one_book_info["rank"] = rank + (page - 1) * 20
            # print(book.find("h4"))
            title = book.find("h2").find("a")
            if title == None:
                print("该书无标题")
                continue
            one_book_info["title"] = title.text
            author_and_class = book.find("p", class_="author")
            infos = author_and_class.find_all("a")
            one_book_info["author"] = infos[0].text
            one_book_info["class"] = infos[1].text
            one_book_info["descrip"] = book.find(
                "p", class_="intro").text.strip(" \n")
            book_info_lst.append(one_book_info)

        print("完成第{}页".format(page))
    pd.DataFrame(book_info_lst).to_csv(
        r"E:\本科科研\网络文学发展分析\数据\起点\第六十周2022.9.26~10.2\{}.csv".format(key_word),
        encoding="utf-8-sig")

    print("完成关键词{}".format(key_word))