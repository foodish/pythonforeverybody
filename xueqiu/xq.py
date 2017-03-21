from urllib.request import Request, urlopen
from urllib import error, parse
import json
import sqlite3


conn = sqlite3.connect('xqfriends.sqlite')
cur = conn.cursor()
         
cur.execute('''CREATE TABLE IF NOT EXISTS People
            (id INTEGER PRIMARY KEY, uid INTEGER UNIQUE, name TEXT, retrieved INTEGER)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Follows
            (from_id INTEGER, to_id INTEGER, UNIQUE(from_id, to_id))''')
            
headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
		'Cookie': 'xq_a_token=720138cf03fb8f84ecc90aab8d619a00dda68f65'
	}
	
while True:
    userid = input('Enter Xueqiu Account id or q:')
    
    if userid == 'q': break
    elif len(userid) < 1:
        cur.execute('SELECT id, uid FROM People WHERE retrieved = 0 LIMIT 1')
        try:
            (id, userid) = cur.fetchone()
            print(userid)
        except:
            print('No unretrieved Xueqiu accounts found')
            continue
    else:
        cur.execute('SELECT id FROM People WHERE uid = ? LIMIT 1', (userid, ))
        try:
            id = cur.fetchone()[0]
        except:
            cur.execute('''INSERT OR IGNORE INTO People (uid, retrieved) VALUES (?, 0)''', (userid, ))
            conn.commit()
            if cur.rowcount != 1:
                print('___________')
                print('Error inserting account:', userid)
                continue
            id = cur.lastrowid
    print('>>>>>>>>')
    print(id)           
    url = 'https://xueqiu.com/friendships/groups/members.json?page=1&uid=%s&gid=0' % (userid)
    print('Retrieving', url)
    request = Request(url, headers=headers)
    r = urlopen(request)
    data = r.read().decode('utf-8')
    js = json.loads(data)
    #print(hs)
    # print(json.dumps(js, indent=2))

    cur.execute('UPDATE People SET retrieved=1 WHERE uid = ?', (userid, ))
    
    countnew = 0
    countold = 0
    
    max_Page = js['maxPage']
    
    for u in js['users']:
        user_id = u['id']
        user_name = u['screen_name']
        print(u['id'], u['screen_name'])        
        cur.execute('SELECT id FROM People WHERE uid = ? LIMIT 1', (user_id, ))
        
        try:
            friend_id = cur.fetchone()[0]
            print('*********')
            print(friend_id)
            countold = countold + 1
        except:
            cur.execute('INSERT OR IGNORE INTO People (uid, name, retrieved) VALUES (?, ?, 0)', (user_id,user_name))
            conn.commit()
            if cur.rowcount != 1:
                print('***********')
                print('Error inserting account:', user_id)
                continue
            friend_id = cur.lastrowid
            print('------')
            print(friend_id)
            countnew = countnew + 1
        cur.execute('INSERT OR IGNORE INTO Follows (from_id, to_id) VALUES (?, ?)', (id, friend_id))
    print('New accounts=', countnew, ' revisited=', countold)
    conn.commit()
    
cur.close()

