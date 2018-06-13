import re
from aip import AipNlp
import time
import json
import datetime


class TextProcessor:

    def __init__(self):
        self.SLEEP_TIME = 0.25
        self.OUTPUT_FILE_NAME = 'data.json'
        self.NICKNAME_DICT = {
            '山支': '孟美岐', '美岐': '孟美岐', '宣仪': '吴宣仪', '五选一': '吴宣仪', '小七': '赖美云',
            '菊姐': '王菊', 'sunnee': '杨芸晴', '村花': '杨超越'

        }
        self.KEY_WORDS =[
            '创造101', '101', '陈意涵', '段奥娟', '傅菁', '高秋梓', '高颖浠', '赖美云',
            '李子璇', '李紫婷', '刘人语', '吕小雨', '孟美岐', '戚砚笛', '强东玥', '王菊',
            '吴宣仪', '吴映香', '徐梦洁', '许靖韵', 'yamy', '杨超越', '杨芸晴', '紫宁',
            '陈芳语', '范薇', '蒋申', '焦曼婷', '刘丹萌', '鹿小草', '罗怡恬', '罗奕佳',
            '苏芮琪', '王莫涵', '王婷', '魏瑾', '吴芊盈', '赵尧珂', '杜金雨', '朱天天',
            '王晴', '热依娜', '于美红', '刘念', '葛佳慧', '丑丑', '菊麟', '刘德熙', '江璟儿',
            '勾雪莹', '杨冰', '罗智仪', '张溪', 'mena', '马兴钰', '刘思纤', '张楚寒', '向俞星',
            '吴茜', '尹蕊', '张鑫磊', '陈盈燕', '姜彦汐', '周雪', '吴小萱', '张静萱', '张馨月',
            '张新洁', '任真', '倪秋云', '杨蕊菡', '杨美琪','毛唯嘉', '林君怡', '林珈安', '邵夏',
            'Blair', '许诗茵', '潘珺雅', '王雅凛', '胡悦儿', '芮萌', '李天韵', '陈怡凡', '陈语嫣',
            '王亦然', '夏诗洁', '刘宇珊', '朱佳希', '杨美玲', '刘尼夷', '韩丹', '尹柔懿', '罗天舒',
            '杨晗', '刘佳莹', '吴昀廷', '王曼君', '张瑜纹', '颜可欣', '王珏萌', '邱路晴', '郑丞丞',
            '山支', '美岐', '宣仪', '五选一', '小七', '菊姐', 'sunnee', '村花'
        ]

    def judge_type(self, weibo):
        for i in range(2, len(self.KEY_WORDS)):
            if self.KEY_WORDS[i] in weibo:
                if i > 1 and i < 103:
                    return self.KEY_WORDS[i]
                elif i >= 103 and self.KEY_WORDS[i] in self.NICKNAME_DICT:
                    return self.NICKNAME_DICT[self.KEY_WORDS[i]]
        if self.KEY_WORDS[0] in weibo or self.KEY_WORDS[1]:
            return 'all'
        else:
            return 'throw'

    def process(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            s = f.read()
            s = ''.join(s.split())
            #print(s)
            E = re.findall(r'E(.*?)E', s)
            F = re.findall(r'F(.*?)F', s)
            #print(E)
            #print(F)
            result = []
            for index in range(len(F)):
                weibo_content = E[index]
                weibo_type = self.judge_type(weibo_content)
                if weibo_type=='throw':
                    continue
                dates = re.findall(r'at([0-9].*?)<', F[index])
                contents = re.findall(r'>:(.*?)at[0-9]', F[index])
                if dates:
                    for j in range(len(dates)):
                        a = {}

                        a['date'] = dates[j]
                        a['content'] = contents[j]
                        a['content'] = re.sub(r'\$(.*?)\$:', '', a['content'])
                        a['content'] = re.sub(r'\$(.*?)\$', '', a['content'])

                        if (weibo_type != 'all'):
                            a['type'] = weibo_type
                        else:
                            a['type'] = self.judge_type(a['content'])

                        if '月' in a['date']:
                            a['date'] = a['date'][0:2] + a['date'][3:5]
                        elif '今天' in a['date']:
                            a['date'] = datetime.datetime.now().strftime('%m%d')
                        elif '前' in a['date']:
                            a['date'] = datetime.datetime.now().strftime('%m%d')
                        else:
                            a['date'] = a['date'][5:7] + a['date'][8:10]
                        if a['content']:
                            result.append(a)

            print(result)

            #调用情感分析api
            """ 你的 APPID AK SK """
            APP_ID = '11377051'
            API_KEY = 'DPHGf2kvWedTVhMYZA3YAoQL'
            SECRET_KEY = 'Xg8vhEBOlOLbdYWsvPue6uh5AT6XBYxP '
            client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

            finalResult = []
            for i in range(len(result)):
                if result[i]['content']:
                    text = result[i]['content']
                    try:
                        analyresult = client.sentimentClassify(text)
                        print(str(i) + '/' + str(len(result)))
                        while 'error_msg' in analyresult:
                            print('error')
                            time.sleep(self.SLEEP_TIME)
                            analyresult = client.sentimentClassify(text)
                        finalResultObj = {}
                        finalResultObj['positive_prob'] = analyresult['items'][0]['positive_prob']
                        finalResultObj['sentiment'] = analyresult['items'][0]['sentiment']
                        finalResult.append(finalResultObj)
                    except:
                        pass

                    #print(analyresult)
                    #analyresult = client.sentimentClassify(text)
                    #time.sleep(self.SLEEP_TIME)

            output = {}
            output['result'] = result
            with open(self.OUTPUT_FILE_NAME, 'w', encoding='utf-8') as f:
                json.dump(output, f)
            # with open(self.OUTPUT_FILE_NAME, 'r') as f:
            #     t = json.load(f)
            #
            #     print(t)

    def judge_weibo(self, content):
        for key_word in self.KEY_WORDS:
            if key_word in content:
                return True

        return False






# processor = TextProcessor('./2925163291.txt')
# r = processor.process()
# print(r)
# a = 'E aaa E F jkjF  E ddd E'
#
#
# b = ''.join(b.split())
# E = re.findall(r'E.*?E', b)
# print(E)

#调用情感分析api
""" 你的 APPID AK SK """
APP_ID = '11377051'
API_KEY = 'DPHGf2kvWedTVhMYZA3YAoQL'
SECRET_KEY = 'Xg8vhEBOlOLbdYWsvPue6uh5AT6XBYxP '
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
text = '打卡，填了'
analyresult = client.sentimentClassify(text)
print(analyresult)
