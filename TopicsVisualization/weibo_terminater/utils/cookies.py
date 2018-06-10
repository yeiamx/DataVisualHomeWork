# -*- coding: utf-8 -*-
# file: cookies.py
# author: JinTian
# time: 17/04/2017 12:55 PM
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
"""
to get weibo_terminator switch accounts automatically, please be sure install:

PhantomJS, from http://phantomjs.org/download.html

"""
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import InvalidElementStateException
import time
import sys
from tqdm import *
import pickle
from WeiboCookiesLogin import *

from settings.accounts import accounts
from settings.config import LOGIN_URL, PHANTOM_JS_PATH, COOKIES_SAVE_PATH


def count_time():
    for i in tqdm(range(40)):
        time.sleep(0.5)


def get_cookie_from_network(account_id, account_password):
    try:
        print('account id: {}'.format(account_id))
        print('account password: {}'.format(account_password))

        wb = WeiboCooikesLogin(account_id, account_password)
    except InvalidElementStateException as e:
        print(e)
        print('error, account id {} is not valid, pass this account, you can edit it and then '
              'update cookies. \n'
              .format(account_id))

    try:
        cookie_dict = wb.get_cookies_main()   # 得到cookie
        print(cookie_dict)
        cookie_string = ''
        for key,value in cookie_dict.items():
            cookie_string += key + '=' + value + ';'
        print(cookie_string)
        if 'SSOLoginState' in cookie_string:
            print('success get cookies!! \n {}'.format(cookie_string))
            if os.path.exists(COOKIES_SAVE_PATH):
                with open(COOKIES_SAVE_PATH, 'rb') as f:
                    cookies_dict = pickle.load(f)
                if cookies_dict[account_id] is not None:
                    cookies_dict[account_id] = cookie_string
                    with open(COOKIES_SAVE_PATH, 'wb') as f:
                        pickle.dump(cookies_dict, f)
                    print('successfully save cookies into {}. \n'.format(COOKIES_SAVE_PATH))
                else:
                    pass
            else:
                cookies_dict = dict()
                cookies_dict[account_id] = cookie_string
                with open(COOKIES_SAVE_PATH, 'wb') as f:
                    pickle.dump(cookies_dict, f)
                print('successfully save cookies into {}. \n'.format(COOKIES_SAVE_PATH))
            return cookie_string
        else:
            print('error, account id {} is not valid, pass this account, you can edit it and then '
                  'update cookies. \n'
                  .format(account_id))
            pass

    except Exception as e:
        print(e)
