#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2017/6/8
# @Author  : foodish
# @File    : test_sql_insert_many.py
import requests
import sqlite3

# 连接数据库，创建User，Follow表
conn = sqlite3.connect('xqfriends_0608.db')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS User(id INT PRIMARY KEY, screen_name TEXT, gender TEXT, province TEXT, 
city TEXT, verified INT, verified_type INT, cube_count INT, stocks_count INT, friends_count INT, followers_count INT, status_count INT,
  last_status_id INT, is_visited INT DEFAULT 0)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Follow
            (from_id INTEGER, to_id INTEGER, UNIQUE(from_id, to_id))''')


# 好友列表地址
urls = [
    'https://xueqiu.com/friendships/groups/members.json?page=' + str(i) + '&uid=7379293559&gid=0' for i in range(1, 4)
]


def get_maxpage(uid):
    url = 'https://xueqiu.com/friendships/groups/members.json?page=1&gid=0&uid=%s' % (uid)
    return get_page(url)['maxPage']


def get_page_list(uid):
    url = 'https://xueqiu.com/friendships/groups/members.json?page=1&gid=0&uid=%s' % (uid)
    max_page = int(get_page(url)['maxPage']) + 1
    page_list = ['https://xueqiu.com/friendships/groups/members.json?page=%d&uid=%s&gid=0' % (i, uid) for i in range(1,
                                                                                                                     max_page)]
    return page_list


# 获取每页数据，为json格式
def get_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Cookie'    : 'xq_a_token=876f2519b10cea9dc131b87db2e5318e5d4ea64f'
    }
    r = requests.get(url, headers=headers).json()
    return r


uid = 7379293559
user_list = []
friendship_list = []
func_user = user_list.append
func_friendship = friendship_list.append


# 获取好友列表各页数据
results = map(get_page, urls)
# close the pool and wait for the work to finish
for page_data in results:
    users = page_data['users']
    for user in users:
        id = user['id']
        screen_name = user['screen_name']
        gender = user['gender']
        province = user['province']
        city = user['city']
        verified = user['verified']
        verified_type = user['verified_type']
        cube_count = user['cube_count']
        stocks_count = user['stocks_count']
        friends_count = user['friends_count']
        followers_count = user['followers_count']
        status_count = user['status_count']
        last_status_id = user['last_status_id']
        user = (id, screen_name, gender, province, city, verified, verified_type, cube_count,
                stocks_count, friends_count, followers_count, status_count, last_status_id)
        friendship = (uid, id)
        func_user(user)
        func_friendship(friendship)

cur.executemany(
    "INSERT INTO User (id, screen_name, gender, province, city, verified, verified_type, cube_count, stocks_count, friends_count, followers_count, status_count,last_status_id) VALUES (?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?)",
    user_list)
cur.executemany("INSERT INTO Follow (from_id, to_id) VALUES (?, ?)", friendship_list)
conn.commit()
cur.close()
conn.close()
