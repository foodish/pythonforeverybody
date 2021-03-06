# coding: utf-8
import pandas as pd
import sqlite3
import networkx as nx


def pagerank():
    conn = sqlite3.connect('xqfriends_0504.db')

    following_data = pd.read_sql(
        'select from_id, to_id from Follows where from_id in (select id from People where fo_num > 10000) and to_id '
        'in (select id from People where fo_num > 10000)', conn)
    conn.close()

    print(following_data.describe())

    G = nx.DiGraph()
    for d in following_data.iterrows():
        G.add_edge(d[1][0], d[1][1])

    # PageRank
    pr = nx.pagerank(G)
    pr_sorted = sorted(pr.items(), key=lambda x: x[1], reverse=True)
    print('pagerank top 100:\n')
    for p in pr_sorted[:100]:
        print(p[0], p[1])


if __name__ == '__main__':
    pagerank()
