import sqlite3
import networkx as nx


conn = sqlite3.connect('xqfriends_0504.db')
cur = conn.cursor()


def shortest():
    cur.execute('select * from Follows limit 1000000')  # 选取太多pythonista会崩溃
    g = nx.DiGraph(name='xq_social')

    for i in cur.fetchall():
        g.add_edge(*i)

    p = nx.shortest_path(g, 1, 21849)  # 第二种写法pythonista崩溃
    # p = nx.shortest_path(g)
    # p[1][21849]
    print(p)

    p_all = nx.all_shortest_paths(g, 1, 21849)
    for i in p_all:
        print(i)


def centrality():
    # cur.execute('select from_id, to_id from Follows where from_id in (select id from People where fo_num > 50000) and to_id in (select id from People where fo_num > 50000)')
    cur.execute(
        'select from_id, to_id from Follows where from_id in (select id from People where fo_num > 100000)')

    g = nx.DiGraph(name='net100k')

    for i in cur.fetchall():
        g.add_edge(*i)

    print(nx.info(g))

    closeness = nx.closeness_centrality(g)
    sorted_closeness = sorted(
        closeness.items(), key=lambda item: item[1], reverse=True)

    print('\ntop 10 closeness_centrality of graph:\n')
    for i in range(10):
        id, fans_num = sorted_closeness[i]
        cur.execute('select name, fo_num from People where id = ?', (id,))
        name, fo_num = cur.fetchone()
        print(name, fo_num, fans_num)

    betweenness = nx.betweenness_centrality(g)
    sorted_betweeness = sorted(
        betweenness.items(), key=lambda item: item[1], reverse=True)

    print('\ntop 10 betweenness_centrality of graph:\n')
    for i in range(10):
        id, fans_num = sorted_betweeness[i]
        cur.execute('select name, fo_num from People where id = ?', (id,))
        name, fo_num = cur.fetchone()
        print(name, fo_num, fans_num)

    eigenvector = nx.eigenvector_centrality(g)
    sorted_eigenvector = sorted(
        eigenvector.items(), key=lambda item: item[1], reverse=True)

    print('\ntop 10 eigenvector_centrality of graph:\n')
    for i in range(10):
        id, fans_num = sorted_eigenvector[i]
        cur.execute('select name, fo_num from People where id = ?', (id,))
        name, fo_num = cur.fetchone()
        print(name, fo_num, fans_num)

    # PageRank
    pr = nx.pagerank(g)
    prsorted = sorted(pr.items(), key=lambda item: item[1], reverse=True)
    # prsorted = sorted(list(pr.items()), key=lambda x: x[1], reverse=True)

    print('\npagerank top 10:\n')
    for i in range(10):
        id, fans_num = prsorted[i]
        cur.execute('select name, fo_num from People where id = ?', (id,))
        name, fo_num = cur.fetchone()
        print(name, fo_num, fans_num)

    # HITS
    hub, auth = nx.hits(g)
    hub_sorted = sorted(hub.items(), key=lambda item: item[1], reverse=True)
    auth_sorted = sorted(auth.items(), key=lambda item: item[1], reverse=True)

    print('\nhub top 10:\n')
    for i in range(10):
        id, fans_num = hub_sorted[i]
        cur.execute('select name, fo_num from People where id = ?', (id,))
        name, fo_num = cur.fetchone()
        print(name, fo_num, fans_num)

    print('\nauth top 10:\n')
    for i in range(10):
        id, fans_num = auth_sorted[i]
        cur.execute('select name, fo_num from People where id = ?', (id,))
        name, fo_num = cur.fetchone()
        print(name, fo_num, fans_num)


def strongly_connected_components():
    cur.execute('select from_id, to_id from Follows where from_id in (select id from People where fo_num > 5000) and to_id in (select id from People where fo_num > 5000)')
    g = nx.DiGraph(name='net5k')

    for i in cur.fetchall():
        g.add_edge(*i)

    # print((len(list(cur.fetchall()))))
    # print(nx.info(g))

    scompgraphs = nx.strongly_connected_component_subgraphs(g)
    scomponents = sorted(
        nx.strongly_connected_components(g), key=len, reverse=True)
    print(('components nodes distribution:', [len(c) for c in scomponents]))

    # plot graph of component, calculate saverage_shortest_path_length of
    # components who has over 1 nodes
    index = 0
    print('average_shortest_path_length of components who has over 1 nodes:')
    for tempg in scompgraphs:
        index += 1
        if len(tempg.nodes()) != 1:
            print((nx.average_shortest_path_length(tempg)))
            print('diameter', nx.diameter(tempg))
            print('radius', nx.radius(tempg))


if __name__ == '__main__':
    print('---------starting----------')
    # shortest()
    # strongly_connected_components()
    centrality()
    print('---------ending---------')
    '''
    Name: net5k
Type: DiGraph
Number of nodes: 4404
Number of edges: 433028
Average in degree:  98.3261
Average out degree:  98.3261
'''
'''
('components nodes distribution:', [3134, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
average_shortest_path_length of components who has over 1 nodes:
2.2302910675028023
diameter 5
radius 3
'''
