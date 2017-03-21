import sqlite3

conn = sqlite3.connect('xqfriends.sqlite')
cur = conn.cursor()

cur.execute('SELECT * FROM Xueqiu')
count = 0
print('People:')
for row in cur:
    print(row)
    count = count + 1
print(count, 'rows.')

cur.close()
