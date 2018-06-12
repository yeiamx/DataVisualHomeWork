import requests
from bs4 import BeautifulSoup


class GetName:

    def __init__(self):
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
        }

        self.url = 'http://v.qq.com/biu/101_star_web'
        self.PATH = 'girlsname.txt'

    # def gethtml(self):
    #     r = requests.get(self.url, headers=self.headers)
    #     r.encoding = r.apparent_encoding
    #     return r.text

    def get_name(self):
        r = requests.get(self.url, headers=self.headers)
        r.encoding = r.apparent_encoding
        names1 = []
        names2 = []
        soup = BeautifulSoup(r.text, 'lxml')
        a = soup.select('#client-entry > div > div > div > div.mod_topic_list > div:nth-of-type(3) > div > div > a:nth-of-type(2)')
        b = soup.select('#client-entry > div > div > div > div.mod_topic_list > div.mod_pic_list.mod_pic_list_farewell > div > div > a.tit')
        for name in a:
            names1.append(name.text)
        for name in b:
            names2.append(name.text)

        with open(self.PATH, 'a', encoding='utf-8') as f:
            for name in names1:
                f.write(name + '\n')
            for name in names2:
                f.write(name + '\n')


        return names1, names2

# html = gethtml(url)
# names1, names2 = get_name(html)
# print(names1)
# print(names2)
# g = GetName()
# names1, names2 = g.get_name()
# print(names1)
# print(names2)


