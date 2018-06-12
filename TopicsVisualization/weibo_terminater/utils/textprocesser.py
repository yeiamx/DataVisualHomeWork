import re
from aip import AipNlp
import time

class TextProcessor:

    def __init__(self, path):
        self.path = path
        self.SLEEP_TIME = 0.1
    def process(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            s = f.read()
            s = ''.join(s.split())
            #print(s)
            E = re.findall(r'E(.*?)E', s)
            F = re.findall(r'F(.*?)F', s)
            #print(E)
            #print(F)
            result = []
            for i in F:
                dates = re.findall(r'at([0-9].*?)<', i)
                contents = re.findall(r'>:(.*?)at[0-9]', i)
                if dates:
                    for j in range(len(dates)):
                        a = {}
                        a['date'] = dates[j]
                        a['content'] = contents[j]
                        result.append(a)
            for i in range(len(result)):
                if re.search(r'\$:(.*)', result[i]['content']):
                    result[i]['content'] = re.search(r'\$:(.*)', result[i]['content']).group(1)
                    #result[i]['date'] = re.search(r'([0-9]{2}).*?([0-9]{2}).*?([0-9]{2}):', result[i]['content']).group(1)
                if '月' in result[i]['date']:
                    result[i]['date'] = result[i]['date'][0:2] + result[i]['date'][3:5]
                else:
                    result[i]['date'] = result[i]['date'][5:7] + result[i]['date'][8:10]
            #调用情感分析api
            """ 你的 APPID AK SK """
            APP_ID = '11377051'
            API_KEY = 'DPHGf2kvWedTVhMYZA3YAoQL'
            SECRET_KEY = 'Xg8vhEBOlOLbdYWsvPue6uh5AT6XBYxP '
            client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

            for i in range(len(result)):
                text = result[i]['content']
                analyresult = client.sentimentClassify(text)
                while 'error_msg' in analyresult:
                    time.sleep(self.SLEEP_TIME)
                    analyresult = client.sentimentClassify(text)
                print(analyresult)
                result[i]['positive_prob'] = analyresult['items'][0]['positive_prob']
                result[i]['sentiment'] = analyresult['items'][0]['sentiment']
               # time.sleep(self.SLEEP_TIME)


            return(result)




# processor = TextProcessor('./2925163291.txt')
# r = processor.process()
# print(r)
#a = 'E aaa E E ddd E'
#E = re.findall(r'E.*?E', a)
#print(E)

