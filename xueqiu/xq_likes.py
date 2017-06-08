# coding: utf-8
import sqlite3
import networkx as nx
import cProfile


conn = sqlite3.connect('xqfriends_0504.db')
cur = conn.cursor()


def save_graph_nets(fans_level):
    # cur.execute('select from_id, to_id from Follows where from_id in (select id from People where fo_num > ?) and to_id in (select id from People where fo_num > ?)', (fans_level, fans_level))
    cur.execute(
        'select from_id, to_id from Follows where from_id in (select id from People where fo_num > ?)', (fans_level,))

    name = 'net' + str(int(fans_level / 1000)) + 'k'
    g = nx.DiGraph(name=name)

    for i in cur.fetchall():
        g.add_edge(*i)

    nx.write_pajek(g, name + '.net')


def ego_graph(user_name):
    cur.execute(
        'select from_id, to_id from Follows where from_id in (select to_id from Follows where from_id in (select id from People where name = ?))', (user_name,))
    g = nx.DiGraph(name='ego_graph')

    for i in cur.fetchall():
        g.add_edge(*i)

    in_degree = g.in_degree()
    sorted_in_degree = sorted(
        in_degree.items(), key=lambda item: item[1], reverse=True)

    print('\ntop 50 likes of ego_graph:\n')
    # for i in range(100):
    for i in range(len(sorted_in_degree)):
        id, likes_num = sorted_in_degree[i]
        cur.execute('select name, fo_num from People where id = ?', (id,))
        name, fo_num = cur.fetchone()
        print(i + 1, name, fo_num, likes_num)


def likes_top_50(fans_level):
    name = 'net' + str(int(fans_level / 1000)) + 'k'
    g = nx.read_pajek(name + '.net')

    print(nx.info(g))

    in_degree = g.in_degree()
    sorted_in_degree = sorted(
        in_degree.items(), key=lambda item: item[1], reverse=True)

    print('\ntop 50', 'likes of', name, 'graph:\n')
    for i in range(200):
        id, likes_num = sorted_in_degree[i]
        cur.execute('select name, fo_num from People where id = ?', (id,))
        name, fo_num = cur.fetchone()
        print(i + 1, name, fo_num, likes_num)

    # with open(name + 'like_top50.txt', 'a', encoding='utf-8') as f:
        # f.write(nx.info(g))
        # f.write('\ntop 50 in_degree of graph:\n')
        # for i in range(50):
        # id, likes_num = sorted_in_degree[i]
        # cur.execute('select name, fo_num from People where id = ?', (id,))
        # name, fo_num = cur.fetchone()
        # f.write(str(i+1) + name + str(fo_num) + str(likes_num))


if __name__ == '__main__':
    print('---------starting----------')
    net_list = [100000, 50000, 10000, 5000]

    # for i in net_list:
    #     save_graph_nets(i)
    #     likes_top_50(i)
    # save_graph_nets(1000)
    cProfile.run('likes_top_50(50000)')
    # ego_graph('不明真相的群众')
    print('---------ending---------')
