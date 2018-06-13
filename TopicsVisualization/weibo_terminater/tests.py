# -*- coding: utf-8 -*-
# file: tests.py
# author: JinTian
# time: 17/04/2017 2:40 PM
# Copyright 2017 JinTian. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------
from utils.cookies import get_cookie_from_network
from settings.accounts import accounts
from settings.config import COOKIES_SAVE_PATH, DEFAULT_USER_ID
import pickle
import requests
from lxml import etree
import os
import pathlib
from textprocesser import TextProcessor
from getgirlsname import GetName
import json

processor = TextProcessor()
def test():
    cookies = get_cookie_from_network(accounts[0]['id'], accounts[0]['password'])
    print(cookies)

def test_for_headers():
    headers = requests.utils.default_headers()
    user_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:11.0) Gecko/20100101 Firefox/11.0'
    }
    headers.update(user_agent)
    print('headers: ', headers)
    return headers

def test_for_cookies():
    with open(COOKIES_SAVE_PATH, 'rb') as f:
        cookies_dict = pickle.load(f)
    print(cookies_dict)
    #user_id = '15116123160'
    #url = 'http://weibo.cn/u/%s?filter=%s&page=1' % (DEFAULT_USER_ID, 0)
    #print(url)

    cookie = {
        "Cookie": cookies_dict['925166340@qq.com']
    }
    #print(list(cookies_dict.keys()))
    return cookie

def test_numric():
    a = '124556'
    b = './huogeh/grjtioh'
    print(float(a))
    print(float(b))

def test_detail(cookie, headers):
    url = 'http://weibo.cn/comment/DCKjWzeHp?uid=2925163291&rl=0'
    html_detail = requests.get(url, cookies=cookie, headers=headers).content
    selector_detail = etree.HTML(html_detail)
    print(selector_detail.xpath('//*[@id="pagelist"]/form/div/input[1]/@value')[0])

def test_comment(cookie, headers):
    url = 'http://weibo.cn/comment/GkirBsdT0?uid=6345246509&rl=0'
    html_detail = requests.get(url, cookies=cookie, headers=headers).content
    selector_comment = etree.HTML(html_detail)
    comment_div_elements = selector_comment.xpath('//div[starts-with(@id, "C_")]/span[@class="ctt"]')
    comment_at_div_elements = selector_comment.xpath('//div[starts-with(@id, "C_")]/span[@class="ctt"]/a')
    for comment_div_element in comment_div_elements:
        print(comment_div_element.xpath('text()'))
    #for comment_at_element in comment_at_div_elements:
    #    print(comment_at_element.xpath('text()'))

def test_file_path():
    weibo_comments_save_path = '/weibo_detail/{}.txt'.format('2925163291')
    #print(os.path.exists(weibo_comments_save_path))
    path = pathlib.Path(weibo_comments_save_path)
    print(path.exists())

def test_getname():
    g = GetName()
    names1, names2 = g.get_name()
    print(names1)
    print(names2)

def test_processer():
    processor.process('./weibo_detail/5596094365.txt', './weibo_detail/process1_5596094365.json')
    #print(r)
    # if processor.judge_weibo('pick宣仪'):
    #     print('yes')
    #print(len(processor.KEY_WORDS))

def test_judge():
    print(processor.judge_type('#sing赖美云# [浮云] #创造101赖美云# 这里是小七@创造101-SING赖美云  的应援会，以后的日子也请一起走吧！下面是一些重要的链接[下]创'))

def test_read():
    with open('./weibo_detail/process1_5596094365.json', 'r') as f:
        t = json.load(f)

        print(t)
if __name__ == '__main__':
    #test_numric()
    #test_detail(test_for_cookies(), test_for_headers())
    #test_comment(test_for_cookies(), test_for_headers())
    #test_file_path()
    #test_processer()
    #test_getname()
    #test_judge()
    test_read()
