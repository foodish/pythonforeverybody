
# coding: utf-8


import pandas as pd
import sqlite3
# import numpy as np
import networkx as nx


def mean_medium():
    conn = sqlite3.connect("xqfriends_0504.db")
    # user_data = pd.read_sql(
    #     'select fr_num, fo_num from People where fo_num > 50000', conn)
    user_data = pd.read_sql(
        'select fr_num, fo_num from People', conn)
    user_data = pd.read_sql(
        'select fr_num, fo_num from People where fo_num > 1000', conn)
    conn.close()
    print(user_data.describe())
    print(user_data.count())
    print('mean number of fr_num, fo_num:', user_data.mean())
    print('medium number of fr_num, fo_num:', user_data.median())


def density_centrality():
    # 密度中心性
    conn = sqlite3.connect("xqfriends_0504.db")

    # sql_50000 = 'select id from People where fo_num > 50000'

    following_data = pd.read_sql(
        "select from_id, to_id from Follows where from_id in (select id from People where fo_num > 50000) and to_id in (select id from People where fo_num > 50000)", conn)

    # print(following_data)
    conn.close()

    G = nx.DiGraph()
    for d in following_data.iterrows():
        G.add_edge(d[1][0], d[1][1])

    print('number of nodes:', G.number_of_nodes())
    print('number of edges:', G.number_of_edges())

    # print nx.average_shortest_path_length(G), '\n'
    print('density of graph:', nx.density(G))


def pagerank():
    conn = sqlite3.connect('xqfriends_0504.db')

    following_data = pd.read_sql(
        'select from_id, to_id from Follows where from_id in (select id from People where fo_num > 10000) and to_id '
        'in (select id from People where fo_num > 10000)', conn)
    conn.close()

    G = nx.DiGraph()
    cnt = 0
    for d in following_data.iterrows():
        G.add_edge(d[1][0], d[1][1])
        cnt += 1
    print('link numbers:', cnt)

    # PageRank
    pr = nx.pagerank(G)
    pr_sorted = sorted(pr.items(), key=lambda x: x[1], reverse=True)
    print('pagerank top 100:\n')
    for p in pr_sorted[:100]:

        print(p[0], p[1])


if __name__ == '__main__':
    # pagerank()
    # density_centrality()
    mean_medium()
# In[ ]:
