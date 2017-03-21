from urllib.request import Request, urlopen
from urllib import error, parse
import json
import sqlite3
import time
import multiprocessing

# seedid = 2818960454
max_num = 5
num = max_num
pool_num = multiprocessing.cpu_count() * 2

conn = sqlite3.connect('xqfriends.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS People
            (id INTEGER PRIMARY KEY, uid INTEGER UNIQUE, name TEXT, gender TEXT, province TEXT, fr_num INTEGER, fo_num INTEGER, retrieved INTEGER)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Follows
            (from_id INTEGER, to_id INTEGER, UNIQUE(from_id, to_id))''')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Cookie': 'xq_a_token=720138cf03fb8f84ecc90aab8d619a00dda68f65'
}


def get_pagedata(url):
    print('Retrieving', url)
    request = Request(url, headers=headers)
    data = urlopen(request).read().decode('utf-8')
    js = json.loads(data)
    return js


def get_maxpage(uid):
    url = 'https://xueqiu.com/friendships/groups/members.json?page=1&uid=%s&gid=0' % (uid)
    return get_pagedata(url)['maxPage']


def get_pageurl(uid):
    pageurl = []
    for i in range(1, int(get_maxpage(uid=uid))+1):
        url = 'https://xueqiu.com/friendships/groups/members.json?page=%d&uid=%s&gid=0' % (i, uid)
        pageurl.append(url)
    return pageurl


def parse_page(url):
    global id
    js = get_pagedata(url)
    for u in js['users']:
        user_id = u['id']
        # print(u['id'], u['screen_name'])
        cur.execute('SELECT id FROM People WHERE uid = ? LIMIT 1', (user_id, ))
        
        try:
            friend_id = cur.fetchone()[0]
            print(friend_id)
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
        cur.execute('SELECT id, uid FROM People WHERE retrieved = 0 LIMIT 1')
        try:
            (id, userid) = cur.fetchone()
            print(id, userid)
        except:
            print('No unretrieved Xueqiu accounts found')
            break
            # continue

        cur.execute('UPDATE People SET retrieved = 1 WHERE uid = ?', (userid, ))

        urls = get_pageurl(userid)
        for url in urls:
            parse_page(url)
        conn.commit()
        num = num - 1
        print(num)
        time.sleep(1)

    cur.close()


if __name__ == '__main__':
    start()