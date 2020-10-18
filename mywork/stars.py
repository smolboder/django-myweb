import requests, bs4, datetime


class scrapeError(Exception):
    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        return self.message


class stardataInitial():
    def __init__(self):
        self.soup = ''
        self.image = ''
        self.datas = []
        self.title = ''
        self.details = []
        self.date = ''


class stardata(stardataInitial):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
               }

    def __init__(self, url=None):
        super().__init__()
        self.url = url
        self.soup = self.get_soup()
        self.date = str(datetime.datetime.today().date())

    def get_soup(self):
        response = requests.get(self.url, headers=stardata.headers)
        if response.ok:
            soup = bs4.BeautifulSoup(response.text, 'html.parser')
            return soup
        else:
            message = 'status_code:{} reason:{}'.format(response.status_code, response.reason)
            raise scrapeError(message)

    def get_image(self):
        img = self.soup.find('div', 'STARBABY').img.get('src')
        self.image = img

    def get_datas(self):
        target = self.soup.find('div', class_='TODAY_LUCKY').find_all('div')
        datas = []
        for ele in target:
            mark = ele.find('img').get('src')
            txt = ele.find('h4').text.strip()
            datas.append((mark, txt))
        self.datas = datas

    def get_details(self):
        target = self.soup.find('div', 'TODAY_CONTENT')
        title = target.find('h3').text.strip()
        details = list(zip(['deeppink', 'lightgreen', 'lightskyblue', 'yellow'],
                           map(lambda x: x.text.strip(), target.find_all('p')[::2]),
                           map(lambda x: x.text.strip(), target.find_all('p')[1::2]),
                           )
                       )
        self.title = title
        self.details = details

    def scrape_datas(self):
        """爬取資料"""
        self.get_image()
        self.get_datas()
        self.get_details()
