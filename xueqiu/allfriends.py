from urllib.request import Request, urlopen
from urllib import error, parse
import json


#xq_url = 'https://xueqiu.com/friendships/groups/members.json?page=%d&uid=%s&gid=0' % (i, userid)
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
        print(u['id'], u['screen_name'], u['gender'], u['province'], u['friends_count'], u['followers_count'])

while True:
    id = input('Enter Xueqiu Account id:')
    if (len(id) < 1): break  
    js_1 = get_page(id, 1)
    print(js_1)

    max_Page = js_1['maxPage']  
    parse_page(js_1)
   
    for i in range(2, int(max_Page)+1):
        js_i = get_page(id, i)
        parse_page(js_i)

        #seedid = 1955602780 #不明真相的群众，关注较多
        #2018766569
