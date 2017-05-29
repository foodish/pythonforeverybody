#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-05-28 22:31:02
# @Author  : foodish
# @Email   : xbj1900@gmail.com
# @Link    : https://foodish.github.io
import pandas as pd
import sqlite3
import networkx as nx
import time


# 计算路径距离
def get_path_length(graph, p):
    length = 0.0
    for i in range(len(p) - 1):
        length += graph[p[i]][p[i + 1]]['weight']  # 带权重值计算路径
    return length


if __name__ == '__main__':
    start_time = time.time()
    print('starting...')
    conn = sqlite3.connect("xqfriends_0504.db")
    following_data = pd.read_sql(
        "select from_id, to_id from Follows where from_id in (select id from People where fo_num > 100000) and to_id in (select id from People where fo_num > 100000)", conn)

    # following_data = pd.read_sql(
    #     "select from_id, to_id from Follows where from_id in (select id from People) and to_id in (select id from People)", conn)

    conn.close()

    print('data has been written into pd')

    G = nx.DiGraph()
    for d in following_data.iterrows():
        G.add_edge(d[1][0], d[1][1])
        # print(d[1][0], d[1][1])

    print('nx has stored following data')

    # 计算两点之间所有路径
    path_iter = nx.all_simple_paths(G, 1, 13847)

    # 查看具体路径
    # pathes = [p for p in path_iter]
    pathes = []
    for p in path_iter:
        pathes.append(p)
        # print(p, len(p))
    print(pathes)

    print('ending...')
    end_time = time.time()
    print('the total time is', end_time - start_time)
