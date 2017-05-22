
# coding: utf-8

# In[8]:

import pandas as pd
import sqlite3
import numpy as np
import networkx as nx

def mean_medium():
    conn = sqlite3.connect("xqfriends_0504.db")
    # user_data = pd.read_sql(
    #     'select fr_num, fo_num from People where fo_num > 50000', conn)
    user_data = pd.read_sql(
        'select fr_num, fo_num from People', conn)
    conn.close()
    print(user_data.describe())
    print(user_data.count())
    print('mean number of fr_num, fo_num:', user_data.mean())
    print('medium number of fr_num, fo_num:', user_data.median())


def density_centrality():
    #密度中心性
    conn = sqlite3.connect("xqfriends_0504.db")
    following_data = pd.read_sql(
        'select from_id, to_id from Follows where from_id in (select id from People where fo_num > 50000) and to_id '
        'in (select id from People where fo_num > 50000)', conn)

    # print(following_data)
    # following_data = pd.read_sql(
    #     'select from_id, to_id from Follows where from_id in (select id from People where fo_num > 5000) and to_id '
    #     'in (select id from People where fo_num > 5000)', conn)
    conn.close()

    G = nx.DiGraph()
    for d in following_data.iterrows():
        G.add_edge(d[1][0], d[1][1])


    print('number of nodes:', G.number_of_nodes())
    print('number of edges:', G.number_of_edges())

    ##print nx.average_shortest_path_length(G), '\n'
    print('density of graph:', nx.density(G))

    # user_betweenness_list = sorted(nx.betweenness_centrality(G).items(), lambda x, y: cmp(x[1], y[1]), reverse=True) #result like [(2, 0.0), (3, 0.0), (1, 1.0)]
    # betweenness_list = zip(*user_betweenness_list)[1]# result like: [(2, 3, 1), (0.0, 0.0, 1.0)][1]; zip(*) is like un zip()

    #betweenness_count_pairs = collections.Counter(list(betweenness_list)).most_common() # list of element like: (0.0006937913420042883, 1)
    #b_value = zip(*betweenness_count_pairs)[0] #unzip to get 0.0006937913420042883
    #b_count = zip(*betweenness_count_pairs)[1]
    #pylab.figure('Betweenness Distribution')
    #pylab.title('Betweenness Distribution')
    #pylab.xlabel('Betweenness')
    #pylab.ylabel('Count')
    #pylab.scatter(b_value, b_count)


    # user_closeness_list = sorted(nx.closeness_centrality(G).items(), lambda x, y: cmp(x[1], y[1]), reverse=True) #Dict.items(): {1: 1.0, 2: 0.0, 3: 0.0} -> [(1, 1.0), (2, 0.0), (3, 0.0)]
    # closeness_list = zip(*user_closeness_list)[1]

    #closeness_count_pairs = collections.Counter(list(closeness_list)).most_common()
    #c_value = zip(*closeness_count_pairs)[0]
    #c_count = zip(*closeness_count_pairs)[0]
    #pylab.figure('Closeness Distribution')
    #pylab.title('Closeness Distribution')
    #pylab.xlabel('Closeness')
    #pylab.ylabel('Count')
    #pylab.scatter(c_value, c_count)


def pagerank():
    conn = sqlite3.connect('xqfriends_0504.db')
    # following_data = pd.read_sql('select from_id, to_id from Follows where from_id in (select id from People where fo_num > 5000) and to_id in (select id from People where fo_num > 5000)', conn)
    # following_data = pd.read_sql(
    #     'select from_id, to_id from Follows where from_id in (select id from People where fo_num > 10000) and to_id '
    #     'in (select id from People where fo_num > 10000)', conn)
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
    
    #PageRank
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



