# coding : utf-8
# 从数据库中随机挑选一个未访问过的用户作为种子用户，遍历其关注者；如果所有用户均被访问过，则结束
import requests
import json
import sqlite3
import time
import multiprocessing

# seedid = 2818960454
num = 1
pool_num = multiprocessing.cpu_count() * 2

conn = sqlite3.connect('xqfriends_0504.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS People
            (id INTEGER PRIMARY KEY, uid INTEGER UNIQUE, name TEXT, gender TEXT, province TEXT, fr_num INTEGER, fo_num INTEGER, retrieved INTEGER)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Follows
            (from_id INTEGER, to_id INTEGER, UNIQUE(from_id, to_id))''')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Cookie': 'xq_a_token=afe4be3cb5bef00f249343e7c6ad8ac7dc0e17fb'
}

def get_page(url):
    r = requests.get(url, headers=headers)
    data = json.loads(r.text)
    return data

def get_maxpage(uid):
    url = 'https://xueqiu.com/friendships/groups/members.json?page=1&uid=%s&gid=0' % (uid)
    return get_page(url)['maxPage']


def get_pageurl(uid):
    pageurl = []
    for i in range(1, int(get_maxpage(uid=uid))+1):
        url = 'https://xueqiu.com/friendships/groups/members.json?page=%d&uid=%s&gid=0' % (i, uid)
        pageurl.append(url)
    return pageurl


def parse_page(url):
    global id
    #print('当前解析的url为', url)
    js = get_page(url)
    for u in js['users']:
        user_id = u['id']
        # print(u['id'], u['screen_name'])
        cur.execute('SELECT id FROM People WHERE uid = ? LIMIT 1', (user_id, ))
        
        try:
            friend_id = cur.fetchone()[0]
            # print(friend_id)
        except:
            cur.execute('INSERT OR IGNORE INTO People (uid, name, gender, province, fr_num, fo_num, retrieved) VALUES (?, ?, ?, ?, ?, ?, 0)', (u['id'], u['screen_name'], u['gender'], u['province'], u['friends_count'], u['followers_count']))
            conn.commit()
            if cur.rowcount != 1:
                print('Error inserting account:', user_id)
                continue
            friend_id = cur.lastrowid
        # print(id, friend_id)
        cur.execute('INSERT OR IGNORE INTO Follows (from_id, to_id) VALUES (?, ?)', (id, friend_id))


def start():
    global num
    global id
    while (True):
        print(num)
        cur.execute('SELECT id, uid FROM People WHERE retrieved = 0 LIMIT 1')
        try:
            (id, userid) = cur.fetchone()
            # print(id, userid)
        except:
            print('No unretrieved Xueqiu accounts found')
            break


        urls = get_pageurl(userid)
        for url in urls:
            parse_page(url)
            time.sleep(1)
        
        cur.execute('UPDATE People SET retrieved = 1 WHERE uid = ?', (userid, ))
        
        conn.commit()
        num = num + 1
        time.sleep(1)

    cur.close()


if __name__ == '__main__':
    start()
    #seedid = 1955602780 #不明真相的群众，关注较多
    #2018766569



