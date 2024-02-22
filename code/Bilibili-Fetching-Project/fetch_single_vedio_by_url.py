import json
import os
import re
import time
from datetime import datetime
import requests
from lxml import etree
import hashlib

## 每次爬虫前需要在Cookie.txt改成自己的Cookie
current_path = os.path.dirname(os.path.abspath(__file__))
cookie_file = current_path + '\Cookie.txt'
with open(cookie_file,'r') as file:
    Cookie = file.read()

class VideoInfoFetcher:
    def __init__(self):
        self.session = requests.session()
        self.session.headers = {
            "authority": "www.bilibili.com",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "max-age=0",
            "sec-ch-ua": "^\\^Not",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "^\\^Windows^^",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Cookie": Cookie,
        }

    def get_picture_hash_key(self, tt):
        rt = [46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49, 33, 9, 42, 19, 29, 28, 14, 39,
              12,
              38, 41, 13, 37, 48, 7, 16, 24, 55, 40, 61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57,
              62,
              11, 36, 20, 34, 44, 52]
        Vt = []

        for Zt in rt:
            if Zt < len(tt):
                Vt.append(tt[Zt])

        return ''.join(Vt)[:32]

    def get_inner_title(self, data):
        if isinstance(data, dict):
            for key, value in data.items():
                if key == 'title':
                    return value
                else:
                    result = self.get_inner_title(value)
                    if result is not None:
                        return result

    def return_date_str(self, start_date_str, end_date_str):
        ll = []
        from datetime import datetime
        start_date = datetime.strptime(start_date_str, '%Y-%m')
        end_date = datetime.strptime(end_date_str, '%Y-%m')

        current_date = start_date
        while current_date <= end_date:
            ll.append(current_date.strftime('%Y-%m'))
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1)
        return ll

    def fetch_video_info(self, url):
        print(url)
        response = self.session.get(url)
        time.sleep(2)
        html = etree.HTML(response.text)
        videodata = re.findall('window.__playinfo__=.*?</script>', response.text)[0].replace('window.__playinfo__=',
                                                                                             '').replace('</script>',
                                                                                                         '')
        infodata = re.findall('window.__INITIAL_STATE__=.*?};', response.text)[0].replace('window.__INITIAL_STATE__=',
                                                                                          '').replace(';', '')
        videodata = json.loads(videodata)
        infodata = json.loads(infodata)
        uid = infodata["videoData"]["owner"]["mid"]
        
        ## 下载音频部分
        audio_file_path = current_path + '/Vedio_data/' + get_uid_from_url(url) + '_audio' + '.m4s'
        audio=videodata["data"]["dash"]["audio"][0]["base_url"]
        with open(audio_file_path, mode='wb') as f:
            downloadaudio = self.session.get(audio)
            f.write(downloadaudio.content)
        
        ## 下载视频部分
        video_file_path = current_path + '/Vedio_data/' + get_uid_from_url(url) + '_video' + '.m4s'
        newvideo = datetime.fromtimestamp(infodata['videoData']['pubdate']).strftime('%Y-%m-%d %H:%M:%S')
        downloadvideo = self.session.get(videodata["data"]["dash"]["video"][3]["base_url"])
        time.sleep(2)
        bqvideo = infodata["rcmdTabNames"]
        with open(video_file_path, mode='wb') as f:
            f.write(downloadvideo.content)
            
            
        oid = infodata['videoData']['stat']['aid']
        aid = infodata['videoData']['cid']
        Vt = '7cd084941338484aae1ad9425b84077c'
        Zt = '4932caff0ff746eab6f01bf08b70ac45'
        Wt = self.get_picture_hash_key(Vt + Zt)
        Ft = str(round(time.time()))
        Jt = f'mode=3&oid={oid}&pagination_str=%7B%22offset%22%3A%22%22%7D&plat=1&seek_rpid=&type=1&web_location=1315875&wts={Ft}'
        md5_hash = hashlib.md5()
        data = f"{Jt + Wt}".encode('utf-8')
        md5_hash.update(data)
        md5_hex = md5_hash.hexdigest()
        w_rid = md5_hex

        timestamp = infodata['videoData']['pubdate']
        date_obj = datetime.fromtimestamp(timestamp)
        date_obj1 = datetime.fromtimestamp(time.time())
        date_str = date_obj.strftime('%Y-%m')
        date_str1 = date_obj1.strftime('%Y-%m')
        start_end_date = self.return_date_str(date_str, date_str1)
        info = {
            'mid': uid,
            '视频发布时间': newvideo,
            '视频标签': bqvideo,
            'up主头像': infodata['videoData']['owner']['face'],
            'up主名称': infodata['videoData']['owner']['name'],
            'up主粉丝数': infodata['upData']['fans'],
            '视频封面': infodata['videoData']['pic'],
            '视频名称': infodata['videoData']['title'],
            '视频点赞数': infodata['videoData']['stat']['like'],
            '视频收藏数': infodata['videoData']['stat']['favorite'],
            '视频投币数': infodata['videoData']['stat']['coin'],
            '视频转发数': infodata['videoData']['stat']['share'],
        }
        params = f'oid={oid}&type=1&mode=3&pagination_str=%7B%22offset%22:%22%22%7D&plat=1&seek_rpid=&web_location=1315875&w_rid={w_rid}&wts={Ft}'
        response = self.session.get(
            f'https://api.bilibili.com/x/v2/reply/main?mode=3&oid={oid}&pagination_str=%7B%22offset%22:%22%22%7D&plat=1&seek_rpid=&type=1')
        time.sleep(2)
        try:
            title_value = self.get_inner_title(response.json()["data"]["top_replies"][0]["content"])
            info['带货商品名称'] = title_value
        except:
            info['带货商品名称'] = 'None'
        shipl = response.json()['data']['replies']
        num = 0
        info["评论"] = {}
        info["弹幕"] = {}
        for pl in shipl:
            num += 1
            info["评论"][str(num)] = pl['content']['message']
        num = 0
        for date in start_end_date:
            for j in self.session.get(f'https://api.bilibili.com/x/v2/dm/history/index?month={date}&type=1&oid={aid}').json()['data']:
                time.sleep(2)
                pldata = self.session.get(f'https://api.bilibili.com/x/v2/dm/web/history/seg.so?type=1&oid={aid}&date={j}')
                print(f'正在抓取--{j}--弹幕')
                time.sleep(2)
                with open('pl.txt', mode='w', encoding='utf-8') as f:
                    f.write(pldata.text)
                with open('pl.txt', mode='r', encoding='utf-8') as f:
                    for data in f.readlines():
                        data = data.replace('\\n', '').strip()
                        if data.replace('\\n', '').strip():  # 如果这一行不是空行
                            num += 1
                            if re.findall(".*?([\u4E00-\u9FA5]+).*?", data) == []:
                                continue
                            else:
                                info['弹幕'][str(num)] = re.findall(".*?([\u4E00-\u9FA5]+).*?", data)[0]
        return info

def get_url_files():
    url_file_names = []
    current_path = os.path.dirname(os.path.abspath(__file__))
    urls_path = current_path + '/Urls'
    for root,dirs,files in os.walk(current_path):  # 遍历file_path下所有的子目录及文件
        for file in files:  #遍历当前路径下所有非目录子文件
            if file.startswith('video_url_'):
                url_file_names.append(urls_path + '/' + file)
    ## 待修改
    return url_file_names

def get_uid_from_url(url:str):
    uid = url.split('/')[-2]
    return uid
    
if __name__ == "__main__":

    ## 先获取文件夹下的全部记录了url的json文件
    urls_by_up_list = get_url_files()
    urls_list = []
    for file in urls_by_up_list:
        up_name_start_index = file.index('video_url_')
        up_name_end_index = file.index('.json')
        up_name = str(file[(up_name_start_index + 10):up_name_end_index])
        with open(file,'r',encoding='utf-8') as f_single_up_urls:
            data = json.load(f_single_up_urls)
            for item in data:
                urls_list.append(item['url'])
        print("UP:{} urls all found.".format(up_name))
        
    for url in urls_list[:1]:
        uid = get_uid_from_url(url)
        fetcher = VideoInfoFetcher()
        video_info = fetcher.fetch_video_info(url)
        target_file_name = str(uid) + "_video_detail" + '.json'
        target_file_path = current_path + '/Vedio_data/' + target_file_name
        with open(target_file_path, mode='w', encoding='utf-8') as f:
            json.dump(video_info,f,ensure_ascii=False,indent=4)
