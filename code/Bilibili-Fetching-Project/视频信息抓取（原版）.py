import json
import re
import time
from datetime import datetime

import requests
from lxml import etree
import hashlib


def get_picture_hash_key(tt):
    rt = [46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49, 33, 9, 42, 19, 29, 28, 14, 39, 12,
          38, 41, 13, 37, 48, 7, 16, 24, 55, 40, 61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62,
          11, 36, 20, 34, 44, 52]
    Vt = []

    for Zt in rt:
        if Zt < len(tt):
            Vt.append(tt[Zt])

    return ''.join(Vt)[:32]


def get_inner_title(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'title':
                return value
            else:
                result = get_inner_title(value)
                if result is not None:
                    return result


def return_date_str(start_date_str, end_date_str):
    ll = []
    from datetime import datetime
    # 定义开始日期和结束日期

    # 将开始日期和结束日期转换为日期对象
    start_date = datetime.strptime(start_date_str, '%Y-%m')
    end_date = datetime.strptime(end_date_str, '%Y-%m')

    # 循环遍历并打印包括 2 月份的月份
    current_date = start_date
    while current_date <= end_date:
        ll.append(current_date.strftime('%Y-%m'))
        if current_date.month == 12:
            current_date = current_date.replace(year=current_date.year + 1, month=1)
        else:
            current_date = current_date.replace(month=current_date.month + 1)
    return ll

url=input('请输入视频地址：')
session = requests.session()
session.headers = {
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
    "Cookie": "buvid3=2F1DB4B6-DB4F-DD14-79DD-05F649DF87A233631infoc; b_nut=1707839765; buvid4=7A33C3CF-6098-0080-011E-34BA24C4E5BE33631-024021315-XAHy0MDYOfn27bBbT2spoQ%3D%3D; _uuid=8D58A5FB-1056A-D44F-984F-AB4C6B2AA6E782410infoc; buvid_fp=28410fa1fa1a8c073464df33ed7e2ffa; enable_web_push=DISABLE; header_theme_version=CLOSE; home_feed_column=5; DedeUserID=150045326; DedeUserID__ckMd5=b41838d91b16a13c; hit-dyn-v2=1; bmg_af_switch=1; bmg_src_def_domain=i0.hdslb.com; LIVE_BUVID=AUTO3517079087974665; rpdid=|(k|k)~kR~uJ0J'u~|)|mukll; browser_resolution=1865-969; SESSDATA=1404bc97%2C1723717527%2C94c71%2A21CjCDz3lcLFbP3L4pMvAds4KvH0VqYSwv-LPwAH_xJBJulgF59HZrjM-_euvWi11oD5sSVjJLUHphLXFlSm5DSm11M0tOdVNFbXRTWDJXVkxnenVhRkV5aTdIajJRR1ZFZGplRUwxeXU3REJjMHNUVURCcEUzdUctdnhoOXdxNzJBNVQzQjRESzN3IIEC; bili_jct=a56e3d102d3e8069367c9bb672ecf976; CURRENT_BLACKGAP=0; CURRENT_FNVAL=4048; CURRENT_QUALITY=112; sid=6w7tr9n9; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDg1MTcyMjksImlhdCI6MTcwODI1Nzk2OSwicGx0IjotMX0.kx2vcGasvYfHbW-hEAJSjkNQ07xpPy9oBFl0atISNq0; bili_ticket_expires=1708517169; bp_video_offset_150045326=899480827413397589; b_lsid=F358109DD_18DBCCC4B12; PVID=3"
}
response = session.get(url)
time.sleep(2)
html = etree.HTML(response.text)
videodata = re.findall('window.__playinfo__=.*?</script>', response.text)[0].replace('window.__playinfo__=',
                                                                                     '').replace('</script>', '')
infodata = re.findall('window.__INITIAL_STATE__=.*?};', response.text)[0].replace('window.__INITIAL_STATE__=',
                                                                                  '').replace(';', '')
videodata = json.loads(videodata)
infodata = json.loads(infodata)
uid=infodata["videoData"]["owner"]["mid"]
audio=videodata["data"]["dash"]["audio"][0]["base_url"]
with open(f"{infodata['videoData']['title']}-audio.m4s", mode='wb') as f:
    downloadaudio=session.get(audio)
    f.write(downloadaudio.content)
# 将日期格式转换为字符串
newvideo = datetime.fromtimestamp(infodata['videoData']['pubdate']).strftime('%Y-%m-%d %H:%M:%S')
downloadvideo = session.get(videodata["data"]["dash"]["video"][3]["base_url"])
time.sleep(2)
bqvideo=infodata["rcmdTabNames"]
with open(f"{infodata['videoData']['title']}.m4s", mode='wb') as f:
    f.write(downloadvideo.content)
oid = infodata['videoData']['stat']['aid']
aid = infodata['videoData']['cid']
Vt = '7cd084941338484aae1ad9425b84077c'
Zt = '4932caff0ff746eab6f01bf08b70ac45'
Wt = get_picture_hash_key(Vt + Zt)
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
# 将日期格式转换为字符串
date_str = date_obj.strftime('%Y-%m')
date_str1 = date_obj1.strftime('%Y-%m')
start_end_date = return_date_str(date_str, date_str1)
info = {
    'mid':uid,
    '视频发布时间':newvideo,
    '视频标签':bqvideo,
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
response = session.get(
    f'https://api.bilibili.com/x/v2/reply/main?mode=3&oid={oid}&pagination_str=%7B%22offset%22:%22%22%7D&plat=1&seek_rpid=&type=1')
time.sleep(2)
title_value = get_inner_title(response.json()["data"]["top_replies"][0]["content"])
info['带货商品名称'] = title_value
shipl = response.json()['data']['replies']
num = 0
info["评论"]={}
info["弹幕"]={}
for pl in shipl:
    num += 1
    info["评论"][str(num)] = pl['content']['message']
    # info[str(num)] = pl['content']['message']
num = 0
for date in start_end_date:
    for j in session.get(f'https://api.bilibili.com/x/v2/dm/history/index?month={date}&type=1&oid={aid}').json()['data']:
        time.sleep(2)
        pldata = session.get(f'https://api.bilibili.com/x/v2/dm/web/history/seg.so?type=1&oid={aid}&date={j}')
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
print(info)
with open(f'{info["up主名称"]}.json',mode='a',encoding='utf-8')as f:
    f.write(json.dumps(info))
