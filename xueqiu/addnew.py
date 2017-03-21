from urllib.request import Request, urlopen
from urllib import error, parse
import json
import sqlite3
import time


conn = sqlite3.connect('xqfriends.db')
cur = conn.cursor()
         
cur.execute('''CREATE TABLE IF NOT EXISTS People
            (id INTEGER PRIMARY KEY, uid INTEGER UNIQUE, name TEXT,gender TEXT, province TEXT, fr_num INTEGER, fo_num INTEGER, retrieved INTEGER)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Follows
            (from_id INTEGER, to_id INTEGER, UNIQUE(from_id, to_id))''')
            
headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
		'Cookie': 'xq_a_token=720138cf03fb8f84ecc90aab8d619a00dda68f65'
	}
	
def get_page(uid, page):
    url = 'https://xueqiu.com/friendships/groups/members.json?page=%d&uid=%s&gid=0' % (page, uid)
    print('Retrieving', url)
    request = Request(url, headers=headers)
    data = urlopen(request).read().decode('utf-8')
    js = json.loads(data)
    return js

def parse_page(js):
    for u in js['users']:
        user_id = u['id']
        user_name = u['screen_name']
        print(u['id'], u['screen_name'])        
        cur.execute('SELECT id FROM People WHERE uid = ? LIMIT 1', (user_id, ))
        
        try:
            friend_id = cur.fetchone()[0]
        except:
            cur.execute('INSERT OR IGNORE INTO People (uid, name, gender, province, fr_num, fo_num, retrieved) VALUES (?, ?, ?, ?, ?, ?, 0)', (u['id'], u['screen_name'], u['gender'], u['province'], u['friends_count'], u['followers_count']))
            conn.commit()
            if cur.rowcount != 1:
                print('Error inserting account:', user_id)
                continue
            friend_id = cur.lastrowid
        print(friend_id)
        cur.execute('INSERT OR IGNORE INTO Follows (from_id, to_id) VALUES (?, ?)', (id, friend_id))
 
seedid = 2818960454
max_num = 5
num = max_num       
       
while num:
    if num == max_num:
        id = 1
        userid = seedid
    else:
        cur.execute('SELECT id, uid FROM People WHERE retrieved = 0 LIMIT 1')
        try:
            (id, userid) = cur.fetchone()
            print(userid)
        except:
            print('No unretrieved Xueqiu accounts found')
            continue
            
    js_1 = get_page(userid, 1)
    cur.execute('UPDATE People SET retrieved = 1 WHERE uid = ?', (userid, ))
        
    max_Page = js_1['maxPage']
    
    parse_page(js_1)
  
    for i in range(2, int(max_Page)+1):
        js_i = get_page(userid, i)
        parse_page(js_i)

    conn.commit()
    num = num - 1
    print(num)
    time.sleep(1)
    
cur.close()
