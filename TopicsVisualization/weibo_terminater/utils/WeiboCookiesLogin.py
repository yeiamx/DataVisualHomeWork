#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/4/26 0:24
# @Author  : hyang
# @File    : WeiboCooikes.py
# @Software:


import time
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait  # 等待元素加载的
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
import requests

class WeiboCooikesLogin(object):
    """
    通过cookies访问微博
    """
    def __init__(self,username, password):
        self.url = 'https://passport.weibo.cn/signin/login'
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()  # 最大化窗口
        self.wait = WebDriverWait(self.driver, 6)
        self.username = username
        self.password = password

    def __del__(self):
        """
         关闭浏览器
        :return:
        """
        print('close browser')
        self.driver.close()

    def open_url(self):
        """
        打开url登录微博
        :return:
        """
        self.driver.delete_all_cookies()  # 删除cookies
        self.driver.get(self.url)
        time.sleep(2)
        user = self.wait.until(EC.presence_of_element_located((By.ID,'loginName')))
        pwd = self.wait.until(EC.presence_of_element_located((By.ID, 'loginPassword')))
        submit = self.wait.until(EC.presence_of_element_located((By.ID, 'loginAction')))
        user.send_keys(self.username)
        time.sleep(1)
        pwd.send_keys(self.password)
        time.sleep(1)
        submit.click()
        time.sleep(5)

    def password_error(self):
        """
        判断用户名密码错误
        :return:
        """
        try:
            return self.wait.until(EC.text_to_be_present_in_element((By.ID,'errorMsg'),'用户名或密码错误'))
        except TimeoutException as e:
            return False

    def login_successful(self):
        """
         获得登录成功标志
        :return:
        """
        try:
            return self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'drop-title')))

        except TimeoutException as e:
            return False

    def process_cookies(self,cookies):
        """
        处理cookies
        :param cookies:
        :return:
        """
        cookies_dict = {}
        for item in cookies:
            cookies_dict[item.get('name')] = item.get('value')
        return cookies_dict

    def save_cookies(self,cookies_dict):
        """
         保存cookies
        :param cookies_dict:
        :return:
        """
        with open('sina_cookies.TXT','w',encoding='utf-8') as f:
            f.write(json.dumps(cookies_dict, ensure_ascii='False',indent=4))

    def get_cookies_main(self):
        self.open_url()
        if self.password_error():
            print('用户名或密码错误')
        if self.login_successful():
            print('用户登录成功')
            cookies = self.driver.get_cookies()
            d = self.process_cookies(cookies)
            self.save_cookies(d)
            print('保存用户cookies成功')
        return d

    def get_cooikes(self):
        """
        从文件中读取cookies
        :return:
        """
        with open('sina_cookies.TXT','r',encoding='utf-8') as f:
            cooikes_dict = json.loads(f.read())

        return cooikes_dict

    def login_with_cookies(self, cookies_dict):
        """
        通过cookies访问主页读取信息
        :param cookies_dict:
        :return:
        """
        time.sleep(2)
        response = requests.get('https://weibo.cn/', cookies = cookies_dict, timeout=5, allow_redirects=False)
        if response.status_code == 200:
            print('用户cookies有效')
            time.sleep(1)
            if '我的首页' in response.text:
                print('通过cookies登录成功')


    def login_cookies_main(self):
        print('用户开始刷新主页！！')
        d = self.get_cooikes()
        print('读取用户cookies！！')
        self.login_with_cookies(d)
        print('通过cookies访问主页！！')



# if __name__ == '__main__':
#     username = '925166340@qq.com' # 新浪微博用户
#     pwd = 'asasas4444' # 新浪微博用户密码
#     wb = WeiboCooikesLogin(username, pwd)
#     wb.get_cookies_main()   # 得到cookies
#     wb.login_cookies_main()  # 用cookies访问主页