from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

options = Options()
options.add_argument("--headless")
header = {"user-agent" : "Mozilla/5.0"}
driver = webdriver.Chrome(executable_path=r"D:\tool\chrome_apps\chromedriver.exe", options=options)
url_base = "http://www.jjwxc.net/topten.php?orderstr={}&t={}"
for i in [0,1,2]:#种类分类
    for j in range(3, 23):#榜单分类
        url_now = url_base.format(j, i)
        data_lst = []
        time.sleep(random.random())
        driver.get(url_now)
        r = driver.page_source
        soup = BeautifulSoup(r)
        if len(soup.find_all("tbody")) < 4:
            print()
            continue
        infos = soup.find_all("tbody")[2]
        #print(infos)
        books = infos.find_all("tr")[1:]#每一本书
        #print(infos.find_all("tr")[0])
        book_info_lst = []
        print(len(books))
        for book in books:
            one_book_info = {}
            one_book_infos = book.find_all("td")
            if len(one_book_infos) < 9:
                print("出现问题，跳过")
                continue
            one_book_info["rank"] = one_book_infos[0].text
            one_book_info["author"] = one_book_infos[1].text.strip("\xa0\n")
            one_book_info["title"] = one_book_infos[2].find("a")["title"]
            one_book_info["class"] = one_book_infos[3].text.strip(" \n")
            one_book_info["being"] = one_book_infos[5].text.strip(" \n")
            one_book_info["words"] = one_book_infos[6].text.strip("\xa0")
            one_book_info["score"] = one_book_infos[7].text
            one_book_info["time"] = one_book_infos[8].text
            one_book_info["descrip"] = one_book_infos[2].find("a")["rel"]
            book_info_lst.append(one_book_info)
            #print(len(book_info_lst))  
        pd.DataFrame(book_info_lst).to_csv(r"晋江\第五十九周2022.9.26~10.2\{}\{}.csv".format(i, j), encoding="utf-8-sig")
        print("完成第{}个排行榜".format(j))
    print("完成第{}种分类".format(i))
            
