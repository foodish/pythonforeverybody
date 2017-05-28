#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-05-28 22:31:02
# @Author  : foodish
# @Email   : xbj1900@gmail.com
# @Link    : https://foodish.github.io
import pandas as pd
import sqlite3
import networkx as nx


# 计算路径距离
def get_path_length(graph, p):
    length = 0.0
    for i in range(len(p) - 1):
        length += graph[p[i]][p[i + 1]]['weight']
    return length


if __name__ == '__main__':
    conn = sqlite3.connect("xqfriends_0504.db")
    # following_data = pd.read_sql(
    #     "select from_id, to_id from Follows where from_id in (select id from People where fo_num > 50000) and to_id in (select id from People where fo_num > 50000)", conn)

    following_data = pd.read_sql(
        "select from_id, to_id from Follows where from_id in (select id from People) and to_id in (select id from People)", conn)

    conn.close()

    G = nx.DiGraph()
    for d in following_data.iterrows():
        G.add_edge(d[1][0], d[1][1])

    # 计算两点之间所有路径
    path_iter = nx.all_simple_paths(G, 1, 21849)

    # 查看具体路径
    # pathes = [p for p in path_iter]
    pathes = []
    for p in path_iter:
        pathes.append(p)
    print(pathes)

    for p in pathes:
        print(get_path_length(G, p), '\t', p)
