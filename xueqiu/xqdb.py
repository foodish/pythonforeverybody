from urllib.request import Request, urlopen
from urllib import error, parse
import json
import sqlite3


conn = sqlite3.connect('xqfriends.sqlite')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Xueqiu 
            (uid INTEGER, retrieved INTEGER, friends_num INTEGER)''')
            
headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
		'Cookie': 'xq_a_token=720138cf03fb8f84ecc90aab8d619a00dda68f65'
	}
	
while True:
    userid = input('Enter Xueqiu Account id or q:')
    if userid == 'q': break
    elif len(userid) < 1:
        cur.execute('SELECT uid FROM Xueqiu WHERE retrieved = 0 LIMIT 1')
        try:
            userid = cur.fetchone()[0]
            print(userid)
        except:
            print('No unretrieved Xueqiu accounts found')
            continue
                
    url = 'https://xueqiu.com/friendships/groups/members.json?page=1&uid=%s&gid=0' % (userid)
    print('Retrieving', url)
    request = Request(url, headers=headers)
    r = urlopen(request)
    data = r.read().decode('utf-8')

    js = json.loads(data)
    # print(json.dumps(js, indent=2))

    # header = dict(r.getheaders())
    cur.execute('UPDATE Xueqiu SET retrieved=1 WHERE uid = ?', (userid, ))
    
    countnew = 0
    countold = 0
    
    for u in js['users']:
        friend_id = u['id']
        
        print(u['id'], u['screen_name'])
        
        cur.execute('SELECT friends_num FROM Xueqiu WHERE uid = ? LIMIT 1',
                    (friend_id, ))
        try:
            count = cur.fetchone()[0]
            cur.execute('UPDATE Xueqiu SET friends_num = ? WHERE uid = ? LIMIT 1',
                    (count+1, friend_id))
            countold = countold + 1
        except:
            cur.execute('''INSERT INTO Xueqiu (uid, retrieved, friends_num)
                        VALUES (?, 0, 1)''', (friend_id, ))
            countnew = countnew + 1
    print('New accounts=', countnew, ' revisited=', countold)
    conn.commit()
cur.close()
#5962548939
