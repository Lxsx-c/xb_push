# -*- coding: utf-8 -*-
"""
cron: */15 * * * * *
定时默认15秒 不建议低于10秒 会被封IP
如需晚上不推送 可以设置为 */15 * 8-23 * * *
new Env('线报推送');
"""

import os, requests

# 关键词类别 可自行修改
key = ["电费", "抗原", "清瘟", "9.9-8.9", "0.01", "N95", "白菜", "漏洞", "BUG", "bug", "福利", "神价", "好价", "话费", "赶紧", "返现", "高反", "洞", "建行生活", "外卖", "云闪付", "立减", "速度"]
# Bark推送Key
Bark_Key = ""
# Bark推送声音
Bark_sound = "choo"


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
    url = 'https://v1.xianbao.fun/plus/json/push.txt'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
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
        xb_url = "https://v1.xianbao.fun" + i['url']  # 获取线报URL
        ID = i['url']  # 获取线报ID

        a += 1
        # 通过线报ID判断是否推送过
        if ID in read_log():
            print("第" + str(a) + "条线报：" + ID + "已推送过")
            print("检测到已推送过的线报，结束本次检测")
            break
        # 判断线报标题是否包含关键字
        for j in key:
            if j in title:
                print("第" + str(a) + "条线报：" + "标题包含关键字：" + j)
                title = "[标题][" + j + "]" + title
                bark(title, content, xb_url)
                break
            elif j in content:
                print("第" + str(a) + "条线报：" + "内容包含关键字：" + j)
                title = "[内容][" + j + "]" + title
                bark(title, content, xb_url)
                break
        print("第" + str(a) + "条线报：" + "未匹配到关键字")
    # 写入缓存ID
    with open("./xb_push.log", "w") as f:
        f.write(cache_ID)


def bark(title, content, push_url):
    url = "https://api.day.app/" + Bark_Key + "/" + title + "/" + content
    params = {
        "sound": Bark_sound,
        "url": push_url
    }

    data = requests.post(url=url, params=params).json()

    if data['code'] == 200:
        print("推送成功")
    elif data['code'] == 400:
        print("推送失败")
    else:
        print("未知错误")


if __name__ == '__main__':
    get_new_xb()
