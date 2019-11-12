import networkx as nx

# read graph
G = nx.read_adjlist('C:\\Users\\Milosz\\Desktop\\TASS_Project_I\\3.net')

# print original parameters
# print(G.number_of_nodes())
# print(G.number_of_edges())

print()

# remove selfloops
G.remove_edges_from(nx.selfloop_edges(G))
# Graph is loaded as Graph class instance - it means it can't have duplicated edges
# print(type(G))

# print modified graph parameters
# print(G.number_of_nodes())
# print(G.number_of_edges())

# generate largest connected component
# largest_cc = max(nx.connected_components(G), key=len) # -> returns SET
subGraph = [G.subgraph(c).copy() for c in nx.connected_components(G)]
# print(type(largest_cc))
print(max(subGraph))
# print(subGraph.number_of_edges())

# nx.write_pajek(G, "C:\\Users\\Milosz\\Desktop\\TASS_Project_I\\test11.net")
# nx.draw(G)
