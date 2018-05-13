import requests
from bs4 import BeautifulSoup

class Helper:
    def __init__(self):
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
        self.charFormat = 'gbk'

    def getSoup(self, url):
        res = requests.get(url, headers=self.headers, timeout = 500)
        #print(requests.utils.get_encodings_from_content(res.text))
        res.encoding = self.charFormat
        #print(res.text)

        return BeautifulSoup(res.text,'html.parser')

    def getJsonStr(self, url):
        #print("accept url "+url)
        res = requests.get(url, headers=self.headers, timeout = 500)
        res.encoding = self.charFormat
        #print("get: "+res.content.decode())

        return res.text