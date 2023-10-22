

import requests
from bs4 import BeautifulSoup
 
def fetchHotel(url):
    # 发起网络请求，获取数据
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    }
 
    # 发起网络请求（参数放到 URL 中了）
    r = requests.get(url,headers=headers)
    r.encoding = "utf-8"
    return r.text
 
def getPageNum(html):
    #获取总页数
    pageNum=1
    bsObj = BeautifulSoup(html,"html.parser")
    pageList = bsObj.find("div",attrs = {"class":"b_paging"}).find_all("a")
    if(pageList):
        pageNum = pageList[-2].text
    return int(pageNum)
 
def parseHtml(html):
    #解析html网页，提取数据
    bsObj = BeautifulSoup(html,"html.parser")
    bookList = bsObj.find("ul",attrs = {"class":"b_strategy_list"})
    books = []
 
    for book in bookList:
        # link = "https://travel.qunar.com" + book.h2.a["href"]
        #print("link:",link)
        title = book.h2.a.text
        #print("title:", title)
        user_info = book.find("p", attrs = {"class":"user_info"})
 
        intro = user_info.find("span", attrs = {"class":"intro"})
        # user_name = intro.find("span", attrs = {"class":"user_name"}).text
        #print("user_name:",user_name)
        date = intro.find("span", attrs = {"class":"date"}).text
        #print("date:",date)
        days = intro.find("span", attrs = {"class":"days"}).text
        #print("days:",days)
        
        places_p = book.find('p', class_='places')
        if (places_p != None):
            via = places_p.get_text().replace("途经：","")
            itinerary_p = places_p.find_next_sibling('p', class_='places')
            if (itinerary_p):
                route = itinerary_p.get_text().replace("行程：","")
            else:
                route = ""
        else:
            via = ""
            route = ""
        # print("via:",via)
        
        # photoTmp = intro.find("span", attrs = {"class":"photo_nums"})
        # if(photoTmp):
        #    photo_nums = photoTmp.text
        # else:
        #     photo_nums = "没有照片"
        # #print("photo_nums:",photo_nums)
 
        peopleTmp = intro.find("span", attrs = {"class":"people"})
        if(peopleTmp):
            people = peopleTmp.text
        else:
            people = ""
        #print("people:",people)
 
        tripTmp = intro.find("span", attrs = {"class":"trip"})
        if(tripTmp):
            trip = tripTmp.text
        else:
            trip = ""
        #print("trip:",trip)
 
        feeTmp = intro.find("span", attrs = {"class":"fee"})
        if(feeTmp):
            fee = feeTmp.text
        else:
            fee = ""
        #print("fee:",fee)
 
        nums = user_info.find("span", attrs = {"class":"nums"})
        icon_view = nums.find("span", attrs = {"class":"icon_view"}).span.text
        #print("icon_view:",icon_view)
        icon_love = nums.find("span", attrs = {"class":"icon_love"}).span.text
        #print("icon_love:",icon_love)
        icon_comment = nums.find("span", attrs = {"class":"icon_comment"}).span.text
        #print("icon_comment:",icon_comment)
 
        #print("----"*20)
        books = [[title,date,days,via,route,people,trip,fee,icon_view,icon_love,icon_comment]]
        yield books
 
def saveCsvFile(filename,content):
    import pandas as pd
    # 保存文件
    dataframe = pd.DataFrame(content)
    dataframe.to_csv(filename, encoding='utf_8_sig', mode='a', index=False, sep=',', header=False )
 
def downloadBookInfo(url,fileName):
    head = [["标题","链接","作者","出发日期","天数","照片数","人数","玩法","费用","阅读数","点赞数","评论数"]]
    saveCsvFile(fileName, head)
    html = fetchHotel(url)
    pageNum = getPageNum(html)
    for page in range(194, pageNum + 1):
        print("正在爬取",str(page), "页 .......")
        url = "https://travel.qunar.com/travelbook/list.htm?page=" + str(page) + "&order=hot_heat"
        html = fetchHotel(url)
        for book in parseHtml(html):
            saveCsvFile(fileName, book)
 
url = "https://travel.qunar.com/travelbook/list.htm?page=111&order=hot_heat"
fileName = "data.csv"
html = fetchHotel(url)
for book in parseHtml(html):
    saveCsvFile(fileName, book)
# downloadBookInfo(url,fileName)
print("全部完成！")
 