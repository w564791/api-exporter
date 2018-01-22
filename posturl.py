#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
author: how_bjl@live.cn
file: posturl
time: 17-12-25 上午9:27
"""

from urllib import  request,parse
import json
import requests
import time
'''
url=r'http://192.168.31.233:8309/v1/nbr/listTopicCategory'
data = {
    "categoryType": "ALL"
}

# data=json.dumps(data)
# print(type(data))
header = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "User-Agent": r"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)"
}
data = parse.urlencode(data).encode('UTF-8')
body_value = request.Request(url=url,data=data,headers=header,method='POST')
resbonse = request.urlopen(body_value)
print(dir(resbonse))
print(resbonse.status)
print(resbonse.read().decode())
'''




# url=r'http://192.168.31.233:8309/v1/nbr/listTopicCategory'
url = r'http://192.168.31.233:8307/v1/manage/userManage/usersStatusInfoList?usersIdList=1'
# data = {
#     "categoryType": "ALL"
# }
header = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "User-Agent": r"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)"
}
# resbonse=requests.post(url=url,data=json.dumps(data),headers=header)
resbonse=requests.get(url=url,headers=header,timeout=2)

print(dir(resbonse))
# print(type(resbonse))
# print(resbonse.headers)

print(resbonse.json()['code'])
print(resbonse.status_code)