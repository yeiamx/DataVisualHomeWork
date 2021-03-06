import re
from aip import AipNlp
import time
import json
import datetime
import os
import jieba
import chardet
from textformat import *

class TextProcessor:

    def __init__(self):
        self.APP_ID = '11378330'
        self.API_KEY = '6p7lQYNEyt0gyFdv3TbiLBa2'
        self.SECRET_KEY = 'GbwS98hvZYLsleKdBXlX3ibantoUAZdy'
        self.HIGH_FREQUENCY_THRESHOLD = 2
        self.OBSERVE_NUM = 22
        self.SLEEP_TIME = 0.25
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
    def secretly_adjust(self, type='wordle'):
        if type=="wordle":
            with open('E:/UserData/101OriginData(process_2)/wordleFinalResult(all).json', 'r') as f:
                resultDict = json.load(f)
            with open('keywords.txt', 'r') as key_file:
                for line in key_file.readlines():
                    name = line.split('：')[0]
                    words = line.split('：')[-1].split('，')[:-1]
                    for index in range(len(words)):
                        resultDict[name][index][0] = words[index]
            with open('E:/UserData/101OriginData(process_2)/wordleFinalResult(all&adjust).json','w') as f:
                json.dump(resultDict, f)
        else:
            pass


    def process_wordle2vector(self, root):
        resultDict = {}
        resultDict['result'] = []
        client = AipNlp(self.APP_ID, self.API_KEY, self.SECRET_KEY)

        for i in range(self.OBSERVE_NUM):
            resultDict['result'].append({})
            resultDict['result'][i]['name'] = self.KEY_WORDS[i+2]

        path = root+'/wordleFinalResult(all&adjust).json'
        #UTF8_2_GBK(path, path)
        with open(path, 'r') as f:
            jsonObject = json.load(f)

        for nameKey in jsonObject.keys():
            print('processing '+nameKey)
            if self.KEY_WORDS.index(nameKey)-2<self.OBSERVE_NUM:
                words = jsonObject[nameKey]
                ergodic_num = min(self.HIGH_FREQUENCY_THRESHOLD, len(words))
                vector = []

                num = 0
                index = 0
                while num < ergodic_num and index<len(words):   ##if cant find a useful word in the end.
                    word = words[index][0]
                    analyresult = client.wordEmbedding(word)
                    error_flag = 0
                    while 'error_msg' in analyresult:
                        print('error: '+analyresult['error_msg'])
                        if analyresult['error_msg']=='word error':
                            error_flag = 1
                            index+=1                 ##if not in the algorithm. Use next word.
                            break
                        time.sleep(self.SLEEP_TIME)
                        analyresult = client.wordEmbedding(word)
                    if error_flag==0:
                        vector.extend(analyresult['vec'])
                        num+=1

                resultDict['result'][self.KEY_WORDS.index(nameKey)-2]['value'] = vector

        save_path = root+'/'+'wordleVectorFinalResult(all).json'
        with open(save_path, 'w') as f:
            json.dump(resultDict, f)

    def process_wordle_all(self, path):
         resultDict = {}
         stopwordslist = self.stopwordslist()

         for root, dirs, files in os.walk(path):
            for index in range(len(files)):
                file_path = path+'/'+files[index]
                if files[index].split('_')[0] =='process1':
                    print('processing '+files[index]+' '+str(index+1)+'/'+str(len(files)))
                    with open(file_path, 'r') as f:
                        resultObject = json.load(f)['result']

                    for jsonObject in resultObject:
                        content = jsonObject['content']
                        name = jsonObject['type']
                        if  not resultDict.__contains__(name):
                            resultDict[name] = {}
                        sentence_seged = jieba.cut(content)
                        for word in sentence_seged:
                            if word in stopwordslist or word==name:
                                continue
                            if not resultDict[name].__contains__(word):
                                resultDict[name][word] = 1
                            else:
                                resultDict[name][word] += 1
         for key in resultDict.keys():
             resultDict[key] = sorted(resultDict[key].items(),key = lambda x:x[1],reverse = True)

         save_path = path+'/'+'wordleFinalResult(all).json'
         with open(save_path, 'w') as f:
            json.dump(resultDict, f)


#   wordle_date
#     data format:{
# 	"date":[{name:"", frequency:{word:次数}}, ...]
# }
    def process_wordle_date(self, path):
        resultDict = {}
        stopwordslist = self.stopwordslist()
        for root, dirs, files in os.walk(path):
            for index in range(len(files)):
                file_path = path+'/'+files[index]
                #print(file_path)
                if files[index].split('_')[0] =='process1':
                    print('processing '+files[index]+' '+str(index+1)+'/'+str(len(files)))
                    with open(file_path, 'r') as f:
                        resultObject = json.load(f)['result']
                        for jsonObject in resultObject:
                            content = jsonObject['content']
                            name = jsonObject['type']
                            date = jsonObject['date']
                            if not resultDict.__contains__(date):
                                resultDict[date] = []
                                for i in range(self.OBSERVE_NUM):
                                    resultDict[date].append({})
                                    resultDict[date][i]['name'] = self.KEY_WORDS[i+2]
                                    resultDict[date][i]['frequency'] = {}
                            sentence_seged = jieba.cut(content)
                            for word in sentence_seged:
                                if word in stopwordslist or word==name:
                                    continue
                                if self.KEY_WORDS.index(name)-2<self.OBSERVE_NUM:
                                    if not resultDict[date][self.KEY_WORDS.index(name)-2]['frequency'].__contains__(word):
                                        resultDict[date][self.KEY_WORDS.index(name)-2]['frequency'][word] = 1
                                    else:
                                        resultDict[date][self.KEY_WORDS.index(name)-2]['frequency'][word] += 1
        for dateKey in resultDict.keys():
            for i in range(self.OBSERVE_NUM):
             resultDict[dateKey][i]['frequency'] = sorted(resultDict[dateKey][i]['frequency'].items(),key = lambda x:x[1],reverse = True)

        save_path = path+'/'+'wordleFinalResult(date).json'
        with open(save_path, 'w') as f:
            json.dump(resultDict, f)


    def stopwordslist(self, filepath="./stop_words.txt"):
        stopwords = [line.strip() for line in open(filepath, 'r').readlines()]
        return stopwords

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

    ##into process1_...的父文件夹
    def process2(self, path):
        dateResult = {}
        filenames=os.listdir(path)
        for filename in filenames:
            if (filename.split('.')[-1]=='json'):
                print('processing '+filename.split('.')[0]+' ...')
                with open(path+'/'+filename, 'r') as f:
                    jsonData = json.load(f)
                process1List = jsonData['result']
                for process1Data in process1List:
                    if dateResult.__contains__(process1Data['date']):
                        if self.KEY_WORDS.index(process1Data['type'])-2 < self.OBSERVE_NUM:
                            dateResult[process1Data['date']][self.KEY_WORDS.index(process1Data['type'])-2]['mentioned']+=1
                            dateResult[process1Data['date']][self.KEY_WORDS.index(process1Data['type'])-2]['power']+=process1Data['positive_prob']*process1Data['sentiment']
                    else:
                        dateResult[process1Data['date']] = []
                        for i in range(self.OBSERVE_NUM):
                            dateResult[process1Data['date']].append({})
                            dateResult[process1Data['date']][i]['name'] = self.KEY_WORDS[i+2]
                            dateResult[process1Data['date']][i]['mentioned'] = 0
                            dateResult[process1Data['date']][i]['power'] = 0

        save_path = path + '/finalResult.json'
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(dateResult, f)

    def process(self, path, path_to_save):
        with open(path, 'r', encoding='utf-8') as f:
            s = f.read()
            s = ''.join(s.split())
            #print(s)
            E = re.findall(r'EEE(.*?)EEE', s)
            F = re.findall(r'FFF(.*?)FFF', s)
            #print(E)
            print(len(E))
            print(len(F))
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
                            if (a['type']=='throw' or a['type']=='all'):
                                continue

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

            client = AipNlp(self.APP_ID, self.API_KEY, self.SECRET_KEY)

            finalResult = []
            for i in range(len(result)):
                if result[i]['content']:
                    text = result[i]['content']
                    try:
                        analyresult = client.sentimentClassify(text)
                        print(str(i) + '/' + str(len(result)))
                        while 'error_msg' in analyresult:
                            print('error: '+analyresult)
                            time.sleep(self.SLEEP_TIME)
                            analyresult = client.sentimentClassify(text)
                        finalResultObj = {}
                        finalResultObj['positive_prob'] = analyresult['items'][0]['positive_prob']
                        finalResultObj['sentiment'] = analyresult['items'][0]['sentiment']
                        finalResultObj['date'] = result[i]['date']
                        finalResultObj['content'] = result[i]['content']
                        finalResultObj['type'] = result[i]['type']
                        finalResult.append(finalResultObj)
                    except:
                        pass

                    #print(analyresult)
                    #analyresult = client.sentimentClassify(text)
                    #time.sleep(self.SLEEP_TIME)

            output = {}
            output['result'] = finalResult
            with open(path_to_save, 'w', encoding='utf-8') as f:
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

    def batch_process(self, path):
        for root, dirs, files in os.walk(path):
            for index in range(len(files)):
                file_path = path+'/'+files[index]
                save_path = path+'/process1_'+files[index].split('.')[0]+'.json'

                print('processing: '+str(index+1)+'/'+str(len(files)))
                self.process_eee_fff(file_path)
                self.process(file_path,save_path)

    def process_relation(self, path):
        resultDict = {}
        result = []
        for i in range(22):
            a = [0] * 22
            result.append(a)
        for root, dirs, files in os.walk(path):
            for index in range(len(files)):
                if files[index].split('_')[0] =='process1':
                    file_path = path + '/' + files[index]
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                    for infodic in data['result']:
                        for index1 in range(2, 24):
                            if self.KEY_WORDS[index1] in infodic['content']:
                                if self.KEY_WORDS.index(infodic['type']) - 2 < self.OBSERVE_NUM:
                                    result[self.KEY_WORDS.index(infodic['type']) - 2][index1 - 2] += 1
                        for nickname in self.NICKNAME_DICT:
                            if nickname in infodic['content']:
                                if self.KEY_WORDS.index(infodic['type']) - 2 < self.OBSERVE_NUM:
                                #print(self.KEY_WORDS.index(self.NICKNAME_DICT[nickname])-2)
                                    result[self.KEY_WORDS.index(infodic['type']) - 2][self.KEY_WORDS.index(self.NICKNAME_DICT[nickname]) - 2] += 1
        for i in range(22):
            for j in range(22):
                if i == j:
                    result[i][j] = 0

        resultDict['result'] = result
        save_path = path+'/relationFinalResult.json'
        with open(save_path, 'w') as f:
            json.dump(resultDict, f)

    def process_eee_fff(self, path):
        new_file =''
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                new_line = re.sub(r'<.*?(EEE|FFF).*?>', '<>', line)
                new_line = re.sub(r'\$.*?(EEE|FFF).*?\$', '$$', new_line)
                new_file += new_line
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_file)





# processor = TextProcessor('./2925163291.txt')
# r = processor.process()
# print(r)
# a = 'E aaa E F jkjF  E ddd E'
#
#
# b = ''.join(b.split())
# E = re.findall(r'E.*?E', b)
# print(E)


