import networkx as nx
from random import choice

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

approxPathLength = 0
noOfNodes = largest_cc_graph.number_of_nodes()
nodes = largest_cc_graph.nodes()

print('@@@@ ' + str(noOfNodes))

for i in range(0, 10000):
    print('# ' + str(i))
    node1 = choice(list(nodes))
    node2 = choice(list(nodes))
    shortest_path_length = nx.dijkstra_path_length(largest_cc_graph, node1, node2)
    approxPathLength += shortest_path_length

print(approxPathLength / (noOfNodes * (noOfNodes - 1)))

#print(nx.average_shortest_path_length(largest_cc_graph))
print('\nEnd of processing')
