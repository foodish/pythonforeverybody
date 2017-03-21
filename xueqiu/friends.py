from urllib.request import Request, urlopen
from urllib import error, parse
import json


#xq_url = 'https://xueqiu.com/friendships/groups/members.json?page=%d&uid=%s&gid=0' % (i, userid)
headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
		'Cookie': 'xq_a_token=720138cf03fb8f84ecc90aab8d619a00dda68f65'
	}

while True:
    print('')
    id = input('Enter Xueqiu Account id:')
    if (len(id) < 1): break
    url = 'https://xueqiu.com/friendships/groups/members.json?page=1&uid=%s&gid=0' % (id)
    print('Retrieving', url)
    request = Request(url, headers=headers)
    r = urlopen(request)
    data = r.read().decode('utf-8')

    js = json.loads(data)
    # print(json.dumps(js, indent=2))

    # header = dict(r.getheaders())

    for u in js['users']:
        print(u['id'], u['screen_name'], u['description'])
        #seedid = 1955602780 #不明真相的群众，关注较多
        #2018766569
