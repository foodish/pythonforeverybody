import sqlite3
import networkx as nx
import pylab


conn = sqlite3.connect('xqfriends_0504.db')
cur = conn.cursor()

def shortest():
    cur.execute('select * from Follows limit 1000000') #选取太多pythonista会崩溃
    g = nx.DiGraph(name='xq_social')
    
    for i in cur.fetchall():
        g.add_edge(*i)
        
    p = nx.shortest_path(g, 1, 21849) #第二种写法pythonista崩溃
    #p = nx.shortest_path(g)
    #p[1][21849]
    print(p)
    
    p_all = nx.all_shortest_paths(g, 1, 21849)
    for i in p_all:
        print(i)

def net5k():
    cur.execute('select from_id, to_id from Follows where from_id in (select id from People where fo_num > 5000) and to_id in (select id from People where fo_num > 5000)')
    g = nx.DiGraph(name='net5k')
    
    for i in cur.fetchall():
        g.add_edge(*i)
        
    print((nx.info(g)))
        ##print nx.average_shortest_path_length(G), '\n'
    print(('density of graph:', nx.density(g)))
       
def density_centrality():
    cur.execute('select from_id, to_id from Follows where from_id in (select id from People where fo_num > 100000) and to_id in (select id from People where fo_num > 100000)')
    g = nx.DiGraph(name='net5k')
    
    for i in cur.fetchall():
        g.add_edge(*i)
        
    in_degree = g.in_degree()    
    sorted_in_degree = sorted(in_degree.items(), key=lambda item:item[1], reverse=True)
    print('top 10 in_degree of graph:\n',sorted_in_degree[0:10])
    
    closeness = nx.closeness_centrality(g)        
    sorted_closeness = sorted(closeness.items(), key=lambda item:item[1], reverse=True)
    print('top 10 closeness_centrality of graph:\n',sorted_closeness[0:10])
    
    betweenness = nx.betweenness_centrality(g)
    sorted_betweeness = sorted(closeness.items(), key=lambda item:item[1], reverse=True)
    print('top 10 betweenness_centrality of graph:\n',sorted_betweeness[0:10])
    
    eigenvector = nx.eigenvector_centrality(g)
    sorted_eigenvector = sorted(eigenvector.items(), key=lambda item:item[1], reverse=True)
    print('top 10 eigenvector_centrality of graph:\n',sorted_betweeness[0:10])
    
    ##print nx.average_shortest_path_length(G), '\n'
    #print('density of graph:', nx.density(g))
    ##user_betweenness_list = sorted(list(betweenness.items()), lambda x, y: cmp(x[1], y[1]), reverse=True) #result like [(2, 0.0), (3, 0.0), (1, 1.0)]
    ##betweenness_list = zip(*user_betweenness_list)[1]# result like: [(2, 3, 1), (0.0, 0.0, 1.0)][1]; zip(*) is like un zip()

    #betweenness_count_pairs = collections.Counter(list(betweenness_list)).most_common() # list of element like: (0.0006937913420042883, 1)
    #b_value = zip(*betweenness_count_pairs)[0] #unzip to get 0.0006937913420042883
    #b_count = zip(*betweenness_count_pairs)[1]    


    ##user_closeness_list = sorted(list(closeness.items()), lambda x, y: cmp(x[1], y[1]), reverse=True) #Dict.items(): {1: 1.0, 2: 0.0, 3: 0.0} -> [(1, 1.0), (2, 0.0), (3, 0.0)]
    ##closeness_list = zip(*user_closeness_list)[1]   

    #closeness_count_pairs = collections.Counter(list(closeness_list)).most_common()
    #c_value = zip(*closeness_count_pairs)[0]
    #c_count = zip(*closeness_count_pairs)[0]

    
def pagerank_hits():
    cur.execute('select from_id, to_id from Follows where from_id in (select id from People where fo_num > 5000) and to_id in (select id from People where fo_num > 5000)')
    g = nx.DiGraph(name='net5k')
    
    for i in cur.fetchall():
        g.add_edge(*i)

    # PageRank
    pr = nx.pagerank(g)
    prsorted = sorted(list(pr.items()), key=lambda x: x[1], reverse=True)
    print('pagerank top 100:\n')
    for p in prsorted[:100]:
        print(p[0], p[1])
    
    # HITS
    hub, auth = nx.hits(g)
    print('hub top 100:\n')
    for h in sorted(list(hub.items()), key=lambda x: x[1], reverse=True)[:100]:
        print(h[0], h[1])
    print('\nauth top 100:\n')    
    for a in sorted(list(auth.items()), key=lambda x: x[1], reverse=True)[:100]:     
        print(a[0], a[1])

def strongly_connected_components():
    cur.execute('select from_id, to_id from Follows where from_id in (select id from People where fo_num > 5000) and to_id in (select id from People where fo_num > 5000)')
    g = nx.DiGraph(name='net5k')
    
    for i in cur.fetchall():
        g.add_edge(*i)
        
    #print((len(list(cur.fetchall()))))  
    #print(nx.info(g))

    scompgraphs = nx.strongly_connected_component_subgraphs(g)
    scomponents = sorted(nx.strongly_connected_components(g), key=len, reverse=True)
    print(('components nodes distribution:', [len(c) for c in scomponents]))
    
    #plot graph of component, calculate saverage_shortest_path_length of components who has over 1 nodes
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
    #shortest()
    #net5k()
    #strongly_connected_components()
    #pagerank_hits()
    density_centrality()
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

