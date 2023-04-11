# -*- coding: utf-8 -*-

import requests
import urllib.parse
import re

# 51job的COOKIE 抓包获取 ck只需要"51job=xxx;"这一段
# 没有增加对cookie失效的判断 如果返回值存在'error_code': '010002' 则表示cookie失效 请重新抓取
job_cookie = ''

# 51job的UA 建议自己抓包获取 如果不懂请勿修改
job_ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) ' \
         'Mobile/15E148 statusBarHeight:47.0 navBarHeight:91.0 width:390.0'

# 是否跳过无用任务 建议运行一次后改为True 再根据无法完成的任务ID手动添加到job_skip_taskid中
job_skip = True
# 跳过的任务ID 仅在job_skip为True时有效
# 28：购买简历服务 42：投递3个岗位 按需开启
job_skip_taskid = ['28', '42']

# 是否运行隐藏任务 默认为True
job_hide = True
# 隐藏任务ID
job_hide_taskid = ['800']

# 做任务开关 默认开启 请勿关闭 仅在调试时使用
is_task = True
# 领金币开关 默认开启 请勿关闭 仅在调试时使用
is_gold = True
# 每日签到开关 默认开启
is_sign = True
# 浏览五个岗位任务 默认开启
is_get_job = True
# 是否进行评论(讨论)任务
is_topic = True


def getTask():
    url = 'https://mtask.51job.com/ajax/getTask.ajax.php'
    headers = {
        'Host': 'mtask.51job.com',
        'Origin': 'https://mtask.51job.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cookie': job_cookie,
        'Content-Length': '0',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'User-Agent': job_ua,
        'Referer': 'https://mtask.51job.com/?fullscreen=1',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'X-Requested-With': 'XMLHttpRequest'
    }
    response = requests.post(url, headers=headers)
    return response.json()


def finishTask(task_id):
    url = f"https://mtask.51job.com/ajax/finishTask.ajax.php?id=0&property=%7B%22frompageUrl%22%3A%22%22%2C%22pageUrl" \
          f"%22%3A%22https%3A%2F%2Fmtask.51job.com%2F%22%7D&distinct_id={cuid}&from_domain=51job_app_iphone"
    headers = {
        "Host": "mtask.51job.com",
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://mtask.51job.com",
        "User-Agent": job_ua,
        "Connection": "keep-alive",
        "Referer": "https://mtask.51job.com/?fullscreen=1",
        "Cookie": job_cookie
    }
    data = {
        "task": task_id
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()


def getUserBubble():
    url = 'https://mtask.51job.com/ajax/getUserBubble.ajax.php'
    headers = {
        "Host": "mtask.51job.com",
        "Origin": "https://mtask.51job.com",
        "Accept-Encoding": "gzip, deflate, br",
        "Cookie": job_cookie,
        "Content-Length": "0",
        "Connection": "keep-alive",
        "Accept": "/",
        "User-Agent": job_ua,
        "Referer": "https://mtask.51job.com/?fullscreen=1",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "X-Requested-With": "XMLHttpRequest"
    }
    response = requests.post(url, headers=headers)
    return response.json()


def getgold(gold_list):
    url = 'https://mtask.51job.com/ajax/getgold.ajax.php'
    headers = {
        "Host": "mtask.51job.com",
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://mtask.51job.com",
        "User-Agent": job_ua,
        "Connection": "keep-alive",
        "Referer": "https://mtask.51job.com/?fullscreen=1",
        "Content-Length": "80",
        "Cookie": job_cookie
    }
    for j in gold_list:
        print(j)
        data = {'typeid': j['type'],
                'nums': j['nums'],
                'initime': j['initime'],
                'mks': j['mks'],
                'anniversary': j['anniversary'],
                'expiration': j['expiration']
                }
        response = requests.post(url, headers=headers, data=data)
        print(f"领取{j['nums']}金币返回：{response.text}")


def getjob():
    url = f"https://mtask.51job.com/ajax/finishTask.ajax.php?property=%7B%22frompageUrl%22%3A%22https%3A%2F%2Fmtask.51job.com%2F%22%2C%22pageUrl%22%3A%22https%3A%2F%2Fmtask.51job.com%2F%22%7D&distinct_id={cuid}&from_domain=51job_app_iphone "
    headers = {
        "Host": "mtask.51job.com",
        "Origin": "https://mtask.51job.com",
        "Accept-Encoding": "gzip, deflate, br",
        "Cookie": job_cookie,
        "Content-Length": "6",
        "Connection": "keep-alive",
        "Accept": "/",
        "User-Agent": job_ua,
        "Referer": "https://mtask.51job.com/?fullscreen=1",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "X-Requested-With": "XMLHttpRequest"
    }
    data = {
        "task": "1"
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()


def topic(topicid):
    url = "https://mtask.51job.com/ajax/topic.ajax.php"
    headers = {
        "Host": "mtask.51job.com",
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://mtask.51job.com",
        "User-Agent": job_ua,
        "Connection": "keep-alive",
        "Referer": "https://mtask.51job.com/?fullscreen=1",
        "Cookie": job_cookie
    }
    data = {
        "type": "addcomment",
        "param%5Btopicid%5D": topicid,
        "param%5Bcomment%5D": "%E9%9A%94%E8%A1%8C%E5%A6%82%E9%9A%94%E5%B1%B1",
        "param%5Bstatus%5D": "0"
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()


if __name__ == '__main__':
    # 获取cuid
    match = re.search(r'cuid%3D(\d+)', job_cookie)
    if match:
        result = match.group(1)
        cuid = result
    else:
        print('cookie中未找到cuid，请检查cookie是否正确')
        exit()

    # 判断cookie是否过期
    res = finishTask("666")
    if 'error_code' in res:
        if res['error_code'] == '010002':
            print("cookie已过期，请重新获取")
            exit()

    # 判断签到开关
    if is_sign:
        # 执行签到任务
        print("开始执行签到任务")
        res = finishTask("999")
        print(f"签到任务返回： {res}")

    # 判断是否浏览五个职位
    if is_get_job:
        print("\n开始执行浏览5个职位任务")
        for j in range(5):
            res = (getjob())
            print(f"第{j + 1}次浏览职位任务返回：{res}")

    # 判断是否运行隐藏任务
    if job_hide:
        for i in job_hide_taskid:
            print(f"\n开始执行隐藏任务：{i}")
            res = finishTask(i)
            print(f"隐藏任务{i}返回：{res}")

    # 判断任务开关
    if is_task:
        # 获取任务列表
        print("\n开始获取任务列表")
        task_list = getTask()
        print(f"今日共有{len(task_list)}个任务，尝试完成每个任务......")
        for i in task_list:
            # 任务ID
            task_id = str(i['type'])
            # 任务名称
            name = urllib.parse.unquote(i['name'])
            # 判断任务是否跳过
            if job_skip and task_id in job_skip_taskid:
                print(f"跳过任务ID：{task_id}，任务名称：{name}")
                continue
            print(f"进行任务ID：{task_id}，任务名称：{name}")
            if "topicid" in i and is_topic:
                topic_res = topic(i['topicid'])
                print(f"评论任务topicid：{i['topicid']}，任务返回：{topic_res}")
                continue
            # 执行任务
            res = finishTask(task_id)
            print(f"任务{task_id} 返回：{res}")

    # 判断金币开关
    if is_gold:
        # 获取金币气泡
        print("\n开始执行领取金币任务")
        gold_list = res_gold = getUserBubble()
        print(f"获取到{len(res_gold)}个金币气泡，尝试领取......")
        # 领取金币
        getgold(gold_list)
