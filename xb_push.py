# -*- coding: utf-8 -*-
"""
cron: */15 * * * * *
定时默认15秒 不建议低于10秒 会被封IP
如需晚上不推送 可以设置为 */15 * 8-23 * * *

注：黑名单优先级大于白名单 即同时满足黑名单和白名单的情况下 会被判定为黑名单

Bark仅支持IOS设备 / wxPusher_Push是微信公众号推送 支持安卓/IOS
Bark_Key需下载Bark后获取并填入 如未填写则不推送Bark

WxPusher需自行注册并配置：https://wxpusher.zjiecode.com/admin/
扫码登录-新建应用-复制appToken-需要接收推送的微信扫码关注-复制UID-填入脚本
new Env('线报推送');
"""

import os
import requests

# 推送关键词 可自行修改
key = ["023", "重庆", "电费", "0.01", "漏洞", "BUG", "bug", "神价", "话费", "赶紧", "云缴费", "1分", "洞", "饿了么",
       "云闪付", "立减", "速度", "打车", "高德", "滴滴", "美团", "外卖", "国网", "大水", "有水", "0撸", "0薅", "大毛"]
# 黑名单关键词 可自行修改
# black_key = ["怎么", "求", "了吗", "了没", "是不是", "有没", "能不能", "如何", "哪些", "哪里", "什么"]
black_key = []

# Bark推送Key
Bark_Key = ""
# Bark推送声音
Bark_sound = "choo"

# WxPusher_appToken
WxPusher_appToken = ""
# WxPusher_uids
WxPusher_uids = ""


def read_log():
    log_file = "./xb_push.log"
    # 判断日志文件是否存在
    if os.path.exists(log_file):
        pass
    else:
        # 不存在就创建
        os.system("touch ./xb_push.log")

    # 读取日志文件
    with open(log_file, "r") as f:
        log = f.read()
    # 获取最新的一条推送
    return log


def get_new_xb():
    # url = 'https://v1.xianbao.fun/plus/json/push.txt'
    url = 'http://new.xianbao.fun/plus/json/push.txt'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/103.0.0.0 Safari/537.36'
    }
    data = requests.get(url=url, headers=headers).json()
    cache_ID = data[0]['url']  # 获取最新的一条推送的ID 待推送完毕后写入日志
    a = 0
    # 遍历线报列表
    for i in data:
        title = i['title']  # 获取线报标题
        title = title.replace("/", "\\")  # 替换标题中的斜杠 防止Bark推送失败
        content = i['content']  # 获取线报内容
        content = content.replace("/", "\\")  # 替换内容中的斜杠 防止Bark推送失败
        xb_url = "http://new.xianbao.fun" + i['url']  # 获取线报URL
        ID = i['url']  # 获取线报ID

        a += 1
        # 通过线报ID判断是否推送过
        if ID in read_log():
            print("第" + str(a) + "条线报：" + ID + "已推送过")
            print("检测到已推送过的线报，结束本次检测")
            break

        # 判断是否包含黑名单关键词
        for k in black_key:
            if k in title or k in content:
                title = "黑名单关键词[" + k + "]"
                break

        b = 0
        # 判断线报标题和内容是否包含关键字
        for j in key:
            if "黑名单关键词[" in title:
                print("第" + str(a) + "条线报：" + "标题或内容包含" + title)
                b = 1
                break
            if j in title:
                print("第" + str(a) + "条线报：" + "标题包含关键字：" + j)
                title = "[标题][" + j + "]" + title
                push(title, content, xb_url)
                b = 1
                break
            elif j in content:
                print("第" + str(a) + "条线报：" + "内容包含关键字：" + j)
                title = "[内容][" + j + "]" + title
                push(title, content, xb_url)
                b = 1
                break
        if b == 0:
            print("第" + str(a) + "条线报：" + "未匹配到关键字")
    # 写入缓存ID
    with open("./xb_push.log", "w") as f:
        f.write(cache_ID)


def wxPusher_Push(appToken, content, title, uids, urls):
    url = "https://wxpusher.zjiecode.com/api/send/message"
    data = {
        "appToken": appToken,
        "content": content,
        "summary": title,
        "contentType": 1,
        "uids": [
            uids
        ],
        "url": urls
    }
    req = requests.post(url, json=data).json()
    if req['code'] == 1001:
        print(req['msg'])
    elif req['code'] == 1000:
        print(req['data'][0]['status'])


def bark(title, content, push_url):
    if Bark_Key == "":
        print("Bark推送Key为空，跳过推送")
        return
    url = "https://api.day.app/" + Bark_Key + "/" + title + "/" + content
    params = {
        "sound": Bark_sound,
        "url": push_url
    }
    if len(url) > 300:
        url = "https://api.day.app/" + Bark_Key + "/" + title + "/线报内容过长，请进入查看。"
    data = requests.post(url=url, params=params).json()
    if data['code'] == 200:
        print("Bark推送成功")
    elif data['code'] == 400:
        print("Bark推送失败")
    else:
        print("Bark未知错误,状态码：" + str(data['code']))


def push(title, content, push_url):
    if Bark_Key != "":
        bark(title, content, push_url)
    if WxPusher_appToken != "" and WxPusher_uids != "":
        wxPusher_Push(WxPusher_appToken, content, title, WxPusher_uids, push_url)


if __name__ == '__main__':
    get_new_xb()
