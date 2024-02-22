# 爬取bilibili up主的视频信息

import os
from selenium import webdriver
import re
import json
from bs4 import BeautifulSoup
import time
from urllib import parse as url_parse
import datetime
import time, base64, io, json
from PIL import Image
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains  # 这个类基本能够满足我们所有对鼠标操作的需求

## 每次爬虫前需要在Cookie.txt改成自己的Cookie
current_path = os.path.dirname(os.path.abspath(__file__))
cookie_file = current_path + '/Cookie.txt'
with open(cookie_file,'r') as file:
    Cookie = file.read()
cookies = {i.split("=")[0]: i.split("=")[1] for i in Cookie.split(";") if len(i.split("=")) > 0}

## 统一设置休眠时间
sleep_time = 3

class BSpider():

    def __init__(self):
        # 某个up主的视频页面，只需对pagenum字段进行替换切换不同的页面
        options = webdriver.FirefoxOptions()
        # options.add_argument('--headless')
        options.add_argument('--start-maximized')  # 浏览器最大化
        options.add_argument('--disable-infobars')
        self.main_url = 'https://space.bilibili.com/upuser_id/video?tid=0&page=page_num&keyword=&order=pubdate'
        self.browser = webdriver.Firefox(options=options)
        # self.browser = webdriver.Firefox()
            
    def add_cookies(self):
        cookies_ = {}
        for item in cookies:
            cookies_['domain'] = '.bilibili.com'
            cookies_['name'] = item.replace(" ","")
            cookies_['value'] = cookies[item].replace(" ","")
            cookies_['path'] = '/'
            print(cookies_)
            self.browser.add_cookie(cookies_)

    def close_webdriver(self):
        # 关闭相关驱动
        self.browser.quit()

    def locate2upuser(self, name_string):
        # 通过名字定位到该up主的ID号
        # url中文编码
        name_string = url_parse.quote(name_string)

        self.browser.get('https://search.bilibili.com/upuser?keyword='+name_string+'&page=1&order=fans&order_sort=0&user_type=3')
        time.sleep(3)

        # 获取当前up的个人链接
        uid = self.browser.find_element_by_xpath('//*[@id="user-list"]/div[1]/ul/li/div[2]/div[1]/a[1]').get_attribute('href')
        time.sleep(1)
        # 从链接中取得id
        uid = uid.split('/')[-1].split('?')[0]
        # print(uid)
        return uid

    def resub(self, url, r_pattern, value):
        # 正则替换
        pattern = re.compile(r_pattern)
        page_url = re.sub(pattern, value, url)
        return page_url
        
    def get_detail_list(self, url):
        # 获取某一页视频 url及名称 列表
        detial_url_list = []
        detial_name_list = []
        
        ## 1.先模拟浏览器进入某UP主的全部视频页
        self.browser.get(url)
        time.sleep(sleep_time)
        
        ## 2.通过Cookie的方式登陆B站
        self.add_cookies()
        time.sleep(sleep_time)
        
        ## 3.刷新页面，此时可以正常看到UP主的全部视频
        self.browser.refresh()
        time.sleep(sleep_time)
        
        ## 4.解析页面，提取相关信息
        html = BeautifulSoup(self.browser.page_source)

        for a_label in html.find('div', id = 'submit-video-list').find_all('a', attrs = {'target':'_blank', 'class':'title'}):
            if (a_label['href'] != None):
                detial_url_list.append('https:'+a_label['href'])
                detial_name_list.append(a_label.text)
        
        return detial_url_list, detial_name_list

    def get_pagenum(self, url):
        # 获取当前up的视频页数
        page_url = url
        page_url = self.resub(page_url, r'page_num', str(1))
        
        ## 1.先模拟浏览器进入某UP主的全部视频页
        self.browser.get(page_url)
        time.sleep(sleep_time)
        
        ## 2.通过Cookie的方式登陆B站
        self.add_cookies()
        time.sleep(sleep_time)
        
        ## 3.刷新页面，此时可以正常看到UP主的全部视频
        self.browser.refresh()
        time.sleep(sleep_time)
        
        ## 4.解析页面，提取页数信息
        html = BeautifulSoup(self.browser.page_source)
        with open('tmp.txt','w',encoding='utf-8') as file:
            file.write(str(html))

        page_number = html.find('span', attrs={'class':'be-pager-total'}).text
        print(page_number)
        return int(page_number.split(' ')[1])

    def get_digit_from_string(self, string):
        return re.findall(r"\d+\.?\d*", string)[0]

    def get_page(self, upuser_name, uid):
        # 获取指定up主的所有视频
        # uid = self.locate2upuser(upuser_name)
        url = self.resub(self.main_url, r'upuser_id', str(uid))
        
        # page_number = 7
        page_number = self.get_pagenum(url) # 页数
        
        # 视频url列表 名称列表
        detail_url_list = []
        detail_name_list = []

        for index in range(page_number):
            print("------------------------------------")
            print("page: %d" %(index+1))

            # 对于不同的页，进行正则替换
            page_url = url
            page_url = self.resub(page_url, r'page_num', str(index+1))
            print('page_url: %s' %page_url)
            detial_url_list_onepage, detial_name_list_onepage = self.get_detail_list(page_url)
            # 这里要用extend加到后面
            detail_url_list.extend(detial_url_list_onepage)
            detail_name_list.extend(detial_name_list_onepage)
        

        # 视频json
        video_detail_json = []
        for i in range(len(detail_url_list)):
            video_detail_dect = {}
            ## 只需要记录视频的url和名称，爬取具体某个url交给另一段程序
            video_detail_dect['url'] = detail_url_list[i]
            video_detail_dect['author'] = upuser_name
            video_detail_dect['name'] = detail_name_list[i]
            video_detail_json.append(video_detail_dect)

        target_file_name = current_path + '/Urls/{}.json'.format('video_url_' + upuser_name)
        print('Dump to json file: ', target_file_name)
        with open(target_file_name, 'w', encoding='utf-8') as f:
            json.dump(video_detail_json, f, ensure_ascii=False, sort_keys=True, indent=4)
        print('Dump file finish.')


if __name__ == "__main__":
    print("Programme initializing ...")
    bilibili = BSpider()
    print("Ready.")
    
    # 更改名字爬取不同的UP视频信息
    # target_name = input('请输入UP主名称：')
    # target_uid = input('请输入UP主uid：')
    # target_name = 'MyGO_AveMujica'
    # target_uid = '1459104794'
    
    ## 从文件中读取UP主信息
    up_info_file = current_path + '/Up_info/Up_info.json'
    with open(up_info_file,'r',encoding='utf-8') as f_up:
        data = json.load(f_up)
        for up in data:
            up_name = up['name']
            up_uid = up['uid']
            bilibili.get_page(up_name,up_uid)
    bilibili.close_webdriver()
