import networkx as nx
from random import choice
import operator
import itertools
import collections
import matplotlib.pyplot as plt


def cut_degree(graph, degree):
    gg = nx.Graph()
    for n, d in graph.degree_iter():
        if d > degree:
            gg.add_node(n)
    for n in gg.nodes_iter():
        for nbr, eattr in graph[n].items():
            if nbr in gg:
                gg.add_edge(n, nbr)
    return gg


def print_k_cores(graph):
    core_numbers = nx.core_number(graph)

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


# read graph
G = nx.read_adjlist('C:\\Users\\Milosz\\Desktop\\TASS_Project_I\\Ex2_data\\3.txt')

# print('Original graph parameters')
# print('No. of nodes: ' + str(G.number_of_nodes()))
# print('No. of edges: ' + str(G.number_of_edges()))

# print()

# remove self-loops
G.remove_edges_from(nx.selfloop_edges(G))
# Graph is loaded as 'networkx.classes.graph.Graph' class instance - it means it can't have duplicated edges

# print('Graph without loops / double edges parameters')
# print('No. of nodes: ' + str(G.number_of_nodes()))
# print('No. of edges: ' + str(G.number_of_edges()))

# print()

# test number of components -> nx.number_connected_components(G)

# generate largest connected component
largest_cc = max(nx.connected_components(G), key=len)
largest_cc_graph = G.subgraph(largest_cc)

# print('Largest connected component parameters')
# print('No. of nodes: ' + str(largest_cc_graph.number_of_nodes()))
# print('No. of edges: ' + str(largest_cc_graph.number_of_edges()))

# approximation of average path length with three random samples: 100 / 1k / 10k
# approxPathLength = 0
# noOfNodes = largest_cc_graph.number_of_nodes()
# nodes = largest_cc_graph.nodes()

# print('@@@@ ' + str(noOfNodes))

# for i in range(0, 10000):
#    print('# ' + str(i))
#    node1 = choice(list(nodes))
#    node2 = choice(list(nodes))
#    shortest_path_length = nx.dijkstra_path_length(largest_cc_graph, node1, node2)
#    approxPathLength += shortest_path_length

# print(approxPathLength / (noOfNodes * (noOfNodes - 1)))

print()

# move after k-cores !!!!!!!
# degree_sequence = sorted([d for n, d in largest_cc_graph.degree()], reverse=True)
# print(max(degree_sequence))
#
# degreeCount = collections.Counter(degree_sequence)
# deg, cnt = zip(*degreeCount.items())
#
# fig, ax = plt.subplots()
# plt.bar(deg, cnt, width=0.10, color='b')
#
# plt.title("Degree Histogram")
# plt.ylabel("Count")
# plt.xlabel("Degree")
# ax.set_xticks([d + 0.4 for d in deg])
# ax.set_xticklabels(deg)
#
# plt.show()

all_deg = list(dict(nx.degree(largest_cc_graph)).values())
unique_deg = list(set(all_deg))
count_of_deg = []
for i in unique_deg:
    x = all_deg.count(i)
    count_of_deg.append(x)

axes = plt.gca()
axes.set_xlim([0,60])

plt.bar(unique_deg, count_of_deg)
plt.show()

# plt.hist(list(dict(nx.degree(largest_cc_graph)).values()))
# plt.show()


# find no. of k-cores with highest possible k
print_k_cores(largest_cc_graph)

print()

# first analysis showed that k = 155 is highest
#cutDegrees = cut_degree(largest_cc_graph, 156)
#print_k_cores(cutDegrees)


print('\nEnd of processing')
