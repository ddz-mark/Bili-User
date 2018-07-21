# _*_coding:utf-8_*_
# user  : dudaizhong
# time  : 2018/7/19 20:43
# info  :

import requests
import json
from sqlconnect import MysqlConnect
import threadpool
from time import ctime, sleep

conn_ = MysqlConnect()
urls = []
base_url = 'https://api.bilibili.com/x/web-interface/card?mid='
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}

for m in range(5216, 5230):
    for i in range(m * 100, (m + 10) * 100):
        url = base_url + str(i)
        urls.append(url)


def getsource(url):
    try:
        jscontent = requests.get(url, headers=headers).text
        parser(jscontent)
    except requests.HTTPError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)


def parser(jscontent):
    global conn_

    jsdict = json.loads(jscontent)
    jscard = jsdict['data']['card']
    mid = jscard['mid']
    name = jscard['name']
    sex = jscard['sex']
    current_level = jscard['level_info']['current_level']
    description = jscard['description']
    fans = jscard['fans']
    friend = jscard['friend']
    data = [mid, name, sex, current_level, description, fans, friend]
    print(data)
    conn_.insertdb(data)


if __name__ == "__main__":
    pool = threadpool.ThreadPool(1)  # 线程池数量
    reqs = threadpool.makeRequests(getsource, urls)  # 使用线程池
    for req in reqs:
        pool.putRequest(req)
        # sleep(0.1)
    pool.wait()
