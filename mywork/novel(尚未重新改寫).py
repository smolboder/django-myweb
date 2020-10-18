from bs4 import BeautifulSoup
import requests, re
from .starsclass import scrapeError
from opencc import OpenCC
from .bookdata import *


# from selenium import webdriver

# webdriverpath = r'D:\geckodriver\chromedriver.exe'
# browser = webdriver.Chrome(webdriverpath)

class emptyNovel():
    def __init__(self):
        self.select_book = ''  # 選取的書名
        # self.book = ''  # 書名
        self.start = ''  # 這本書從第幾章開始 通常是第一章
        self.end = ''  # 這本書的最後一章
        self.chapter = ''  # "文章章數:" 常數
        self.num = 0  # 所選取要輸出到螢幕的小說章數 一開始預設是0
        self.para = []  # 所選取小說章數的文章內容
        self.title = ''  # 所選取的章數 文章標題
        self.new_url = ''  # 所選取的章數 網址
        self.link = ''  # "文章連結:" 常數


class novelScrape(emptyNovel):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
               }
    StoT = OpenCC('s2twp')
    TtoS = OpenCC('tw2sp')
    web_url = 'https://www.biqukan.com'
    book = {'1': html1, '2': html2, '3': html3, '4': html4}

    def __init__(self, booknum):
        super().__init__()
        self.url = novelScrape.book[booknum]
        self.soup = self.get_soup()
        self.bookname = self.get_book_name()
        self.allpages = self.page_start()  # 所有的話數 的標籤

    def get_soup(self):
        soup = BeautifulSoup(self.url, 'html.parser')
        return soup

    def get_book_name(self):
        book = self.soup.find('meta', {'property': 'og:novel:book_name'}).get('content').strip()
        return book

    def page_start(self):
        """話數頁面並非從第一話開始 而是從最新一話開始 此函數為找出第一話是從第幾個標籤開始"""
        target = self.soup.find('dt')  # 找第一個標籤
        count = 0
        while True:
            try:
                target = target.find_next_sibling()  # 一個一個往下找
            except:
                # 若沒有next_sibling()了的話  print('已到盡頭')
                break
            else:
                '''找到了第一話的標籤位置'''
                pattern = '正文卷'  # 正文捲的標籤是 dt  正文卷下面的內容標籤全部都是 dd
                if re.search(pattern, target.text.strip()):
                    # print(count, target.text)  # 得到一個count 代表正文捲 從這個count數字開始
                    break
                count += 1

        allpages = self.soup.find_all('dd', text=lambda x: x is not None and re.search(r'^第.+章', x))[count:]
        return allpages

    def get_show_page(self, num):
        """得到輸出在網頁的文章內容"""
        page_url = novelScrape.web_url + self.allpages[num].a.get('href')
        page_title = self.allpages[num].text.strip()
        page_response = requests.get(page_url, headers=novelScrape.headers)
        if page_response.ok:
            page_response.encoding = 'gbk'
            page_soup = BeautifulSoup(page_response.text, 'html.parser')
            paragraph = page_soup.find('div', class_='showtxt')
            pattern = '\S+'
            paragraph = re.findall(pattern, paragraph.text)  # 把文章改成串列
            paragraph.pop(0)  # 第0個也跟內文無關 去掉
            # paragraph = map(lambda x: opencc.convert(x), paragraph)
            return [page_title, paragraph, page_url]
        else:
            message = '狀態:{}  原因:{}'.format(page_response.status_code, page_response.reason)
            raise scrapeError(message)

    def sTOtw(self, para):
        """簡轉繁"""
        txt = novelScrape.StoT.convert(para)
        return txt

    def twTOs(self, para):
        """繁轉簡"""
        txt = novelScrape.TtoS.convert(para)
        return txt



