# coding : utf-8
# 从数据库中随机挑选一个未访问过的用户作为种子用户，遍历其关注者；如果所有用户均被访问过，则结束
import requests
import sqlite3
import time

conn = sqlite3.connect('xqfriends_0608.db')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS User(
          id INT PRIMARY KEY, 
          screen_name TEXT, 
          gender TEXT, 
          province TEXT, 
          city TEXT, 
          verified INT, 
          verified_type INT, 
          cube_count INT, 
          stocks_count INT, 
          friends_count INT, 
          followers_count INT, 
          status_count INT,
          last_status_id INT, 
          is_visited INT DEFAULT 0)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Follows
            (from_id INTEGER, to_id INTEGER, UNIQUE(from_id, to_id))''')
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Cookie'    : 'xq_a_token=876f2519b10cea9dc131b87db2e5318e5d4ea64f'
}


def get_page(url):
    r = requests.get(url, headers=headers).json()
    return r


def get_maxpage(uid):
    url = 'https://xueqiu.com/friendships/groups/members.json?page=1&gid=0&uid=%s' % (uid)
    return get_page(url)['maxPage']


def get_page_list(uid):
    max_page = int(get_maxpage(uid)) + 1
    page_list = ['https://xueqiu.com/friendships/groups/members.json?page=%d&uid=%s&gid=0' % (i, uid) for i in range(1,
                                                                                                                     max_page)]
    return page_list


def get_data(url):
    global id
    print('==================================')
    print('Getting friends list for page %s' % (url))
    print('==================================')
    data = get_page(url)
    for u in data['users']:
        user_id = u['id']
        cur.execute('SELECT id FROM User WHERE id = ? LIMIT 1', (user_id,))
        try:
            friend_id = cur.fetchone()[0]
        except:
            cur.execute('INSERT OR IGNORE INTO User (id, screen_name, gender, province, city, verified, verified_type, '
                        'cube_count, stocks_count, friends_count, followers_count, status_count,last_status_id, is_visited) VALUES (?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, 0)', ' \
                    (u['id'], u['screen_name'], u['gender'], u['province'], u['city'], u['verified'], u['verified_type'],u['cube_count'], u['stocks_count'], u['friends_count'], u['followers_count'], u['status_count'], u['last_status_id']))
            conn.commit()
            friend_id = cur.lastrowid
            # cursor.executemany("insert into userinfo(name, email) values(?, ?)", users)
        cur.execute('INSERT OR IGNORE INTO Follows (from_id, to_id) VALUES (?, ?)', (id, friend_id))


def main():
    seed_id = 1955602780
    try:
        cur.execute('SELECT id FROM User WHERE is_visited = 0 LIMIT 1')
        id = cur.fetchone()
    except:
        id = seed_id


    urls = get_page_list(id)
    for url in urls:
        get_data(url)
        time.sleep(1)
    cur.execute('UPDATE User SET is_visited = 1 WHERE id = ?', (id,))
    conn.commit()
    time.sleep(1)
    cur.close()

if __name__ == '__main__':
    main()
    # seedid = 1955602780 #不明真相的群众，关注较多
    # 2018766569
