'''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2017/6/6
# @Author  : foodish
# @File    : xq_pagerank.py
'''
import sqlite3
import pandas as pd
import networkx as nx


def pagerank_hits():
    conn = sqlite3.connect("xqfriends_0504.db")
    cur = conn.cursor()

    cur.execute('SELECT from_id, to_id FROM Follows WHERE from_id IN (SELECT id FROM People WHERE fo_num > 5000 AND '
                'fo_num < 1000000) AND to_id IN '
                '(SELECT id FROM People WHERE fo_num > 5000 AND fo_num < 1000000)')

    g = nx.DiGraph(name='net5k')

    for i in cur.fetchall():
        g.add_edge(*i)

    # PageRank
    pr = nx.pagerank(g)
    prsorted = sorted(pr.items(), key=lambda item: item[1], reverse=True)
    # prsorted = sorted(list(pr.items()), key=lambda x: x[1], reverse=True)

    print('\npagerank top 100:\n')
    for i in range(100):
        id, fans_num = prsorted[i]
        cur.execute('SELECT name, fo_num FROM People WHERE id = ?', (id,))
        name, fo_num = cur.fetchone()
        print(name, fo_num, fans_num)

    # HITS
    hub, auth = nx.hits(g)
    hub_sorted = sorted(hub.items(), key=lambda item: item[1], reverse=True)
    auth_sorted = sorted(auth.items(), key=lambda item: item[1], reverse=True)

    print('\nhub top 100:\n')
    for i in range(100):
        id, fans_num = hub_sorted[i]
        cur.execute('SELECT name, fo_num FROM People WHERE id = ?', (id,))
        name, fo_num = cur.fetchone()
        print(name, fo_num, fans_num)

    print('\nauth top 100:\n')
    for i in range(100):
        id, fans_num = auth_sorted[i]
        cur.execute('SELECT name, fo_num FROM People WHERE id = ?', (id,))
        name, fo_num = cur.fetchone()
        print(name, fo_num, fans_num)

    conn.close()


if __name__ == '__main__':
    pagerank_hits()
