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
    # 连接People和Follows表，选择id为2的用户所关注的用户
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
    # cur.execute("SELECT * FROM People WHERE name = '跟我走吧14'")
    # cur.execute("SELECT * FROM People WHERE id = '1'")
    # cur.execute("SELECT * FROM People WHERE fr_num = '0'")
    cur.execute(
        "SELECT name, fo_num FROM People WHERE fo_num > '39000' ORDER BY fo_num DESC")
    # cur.execute("SELECT * FROM People WHERE fo_num > '10000' AND gender ='f'")
    # cur.execute("SELECT * FROM People WHERE fo_num > '10000' AND gender ='f' ORDER BY fo_num DESC")
    # cur.execute("SELECT * FROM People WHERE fo_num > '10000' AND gender ='f'
    # ORDER BY fr_num ASC ")
    count = 1
    for i in cur.fetchall():
        print(count, i[0], i[1])
        count += 1


if __name__ == '__main__':
    # f1()
    # f2()
    # f3()
    f4()
    cur.close()
    # me:(21849, 7379293559, '红色番茄酱', 'n', '省/直辖市', 48, 286, 0)
    # 方丈：1955602780
    # (13847, 8255849716, '跟我走吧14', 'm', '江苏', 140, 339029, 1)
