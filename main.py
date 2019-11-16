import networkx as nx
from random import choice
import operator
import itertools
import collections

# read graph
G = nx.read_adjlist('C:\\Users\\Milosz\\Desktop\\TASS_Project_I\\Ex2_data\\3.txt')

#print('Original graph parameters')
#print('No. of nodes: ' + str(G.number_of_nodes()))
#print('No. of edges: ' + str(G.number_of_edges()))

#print()

# remove self-loops
G.remove_edges_from(nx.selfloop_edges(G))
# Graph is loaded as 'networkx.classes.graph.Graph' class instance - it means it can't have duplicated edges

#print('Graph without loops / double edges parameters')
#print('No. of nodes: ' + str(G.number_of_nodes()))
#print('No. of edges: ' + str(G.number_of_edges()))

#print()

# test number of components -> nx.number_connected_components(G)

# generate largest connected component
largest_cc = max(nx.connected_components(G), key=len)
largest_cc_graph = G.subgraph(largest_cc)

#print('Largest connected component parameters')
#print('No. of nodes: ' + str(largest_cc_graph.number_of_nodes()))
#print('No. of edges: ' + str(largest_cc_graph.number_of_edges()))

# approximation of average path length with three random samples: 100 / 1k / 10k
#approxPathLength = 0
#noOfNodes = largest_cc_graph.number_of_nodes()
#nodes = largest_cc_graph.nodes()

#print('@@@@ ' + str(noOfNodes))

#for i in range(0, 10000):
#    print('# ' + str(i))
#    node1 = choice(list(nodes))
#    node2 = choice(list(nodes))
#    shortest_path_length = nx.dijkstra_path_length(largest_cc_graph, node1, node2)
#    approxPathLength += shortest_path_length

#print(approxPathLength / (noOfNodes * (noOfNodes - 1)))

print()

# find no. of k-cores with highest possible k
core_numbers = nx.core_number(largest_cc_graph)

# count number of nodes for each k-core
inv_map = {}
for k, v in core_numbers.items():
    inv_map[v] = inv_map.get(v, [])
    inv_map[v].append(k)

# aggregate nodes to list length
mapped = {k: len(v) for k, v in inv_map.items()}
# sort by k and print
sorted_core_numbers = collections.OrderedDict(sorted(mapped.items(), key=lambda kv: kv[0]))
print(sorted_core_numbers)



print('\nEnd of processing')
