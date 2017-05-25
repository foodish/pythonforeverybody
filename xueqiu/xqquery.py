# coding:utf-8
# 数据库查询
import sqlite3

conn = sqlite3.connect('xqfriends_0504.db')
cur = conn.cursor()


def f1():
    cur.execute('SELECT * FROM People')
    count = 0
    for row in cur:
        count = count + 1
    print('People Table has', count, 'rows.')


def f2():
    cur.execute('SELECT * FROM Follows')
    count = 0
    for row in cur:
        # if count < 25: print(row)
        count = count + 1
    print('Follows Table has', count, 'rows.')


def f3():
    cur.execute('''SELECT * FROM Follows JOIN People
            ON Follows.to_id = People.id
            WHERE Follows.from_id = 2''')
    count = 0
    print('Connections for id=2:')
    for row in cur:
        if count < 25:
            print(row)
        count = count + 1
    print(count, 'rows.')


def f4():
    # cur.execute("SELECT * FROM People WHERE uid = '7379293559'")
    cur.execute("SELECT * FROM People WHERE name = '不明真相的群众'")
    # cur.execute("SELECT * FROM People WHERE id = '1'")
    # cur.execute("SELECT * FROM People WHERE fr_num = '0'")
    # cur.execute("SELECT * FROM People WHERE fo_num > '10000'")
    # cur.execute("SELECT * FROM People WHERE fo_num > '10000' AND gender ='f'")
    # cur.execute("SELECT * FROM People WHERE fo_num > '10000' AND gender ='f' ORDER BY fo_num DESC")
    # cur.execute("SELECT * FROM People WHERE fo_num > '10000' AND gender ='f'
    # ORDER BY fr_num ASC ")
    print(cur.fetchall())


def f5():
    # cur.execute("SELECT count(*) FROM People WHERE fo_num > '10000' AND gender ='f'")
    # print(cur.fetchone())
    cur.execute("SELECT count(*) FROM People")
    print(cur.lastrowid)
    print(cur.rowcount)


if __name__ == '__main__':
    # f1()
    # f2()
    f4()
    # f5()
    cur.close()
    # me:7379293559
    # 方丈：1955602780
