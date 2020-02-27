import networkx as nx
from random import choice
import collections
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import powerlaw


# returns sorted k-cores with number of vertices
def no_of_nodes_for_k_cores(graph):
    core_numbers = nx.core_number(graph)

    # count number of vertices for each core
    inv_map = {}
    for k, v in core_numbers.items():
        inv_map[v] = inv_map.get(v, [])
        inv_map[v].append(k)

    mapped = {k: len(v) for k, v in inv_map.items()}
    sorted_core_numbers = collections.OrderedDict(sorted(mapped.items(), key=lambda kv: kv[0]))
    return sorted_core_numbers


G = nx.read_adjlist('resources\\3.txt')

print('No. of nodes: ' + str(G.number_of_nodes()))
print('No. of edges: ' + str(G.number_of_edges()))
print()

# # delete loops
G.remove_edges_from(nx.selfloop_edges(G))
# # network is read as 'networkx.classes.graph.Graph' instance, so there is no duplicated edges
print('No. of nodes / edges after deleting loops / edge duplicates')
print('No. of nodes: ' + str(G.number_of_nodes()))
print('No. of edges: ' + str(G.number_of_edges()))
print()

# # # # point largest connected component and find it's no. of nodes / edges

print('No. of components: ' + str(nx.number_connected_components(G)))

# # getting largest connected component
largest_cc = max(nx.connected_components(G), key=len)
largest_cc_graph = G.subgraph(largest_cc)

print('No. of nodes / edges for largest connected component')
print('No. of nodes: ' + str(largest_cc_graph.number_of_nodes()))
print('No. of edges: ' + str(largest_cc_graph.number_of_edges()))

# # # # compute approximation of average length path using 100, 1k, 10k random samples of vertices

sumOfShortestPaths = 0
noOfNodes = largest_cc_graph.number_of_nodes()
nodes = largest_cc_graph.nodes()

for i in range(0, 10):
    node1 = choice(list(nodes))
    node2 = choice(list(nodes))
    shortest_path_length = nx.dijkstra_path_length(largest_cc_graph, node1, node2)
    sumOfShortestPaths += shortest_path_length
    print('Iteration: ' + str(i) + ' | Sum: ' + str(sumOfShortestPaths))

print(sumOfShortestPaths / (noOfNodes * (noOfNodes - 1)))

print()

# # # # compute no. of cores with largest possible no. of edges, second largest possible no. of edges and third largest
# # # # possible no. of edges - print those numbers

unfrezeed = nx.Graph(largest_cc_graph)

print('First check of core no.: ' + str(no_of_nodes_for_k_cores(unfrezeed)))  # max 155

# point vertices for deletion based on last reading
to_del1 = [node for node, degree in dict(unfrezeed.degree()).items() if degree >= 155]
unfrezeed.remove_nodes_from(to_del1)

print('Second check of core no.: ' + str(no_of_nodes_for_k_cores(unfrezeed)))  # max 67

# point vertices for deletion based on last reading
to_del2 = [node for node, degree in dict(unfrezeed.degree()).items() if degree >= 67]
unfrezeed.remove_nodes_from(to_del2)

print('Third check of core no.:  ' + str(no_of_nodes_for_k_cores(unfrezeed)))  # max 53

# # # # print vertex degree distribution

degree_sequence = sorted([d for n, d in largest_cc_graph.degree()], reverse=True)
degreeCount = collections.Counter(degree_sequence)
deg, cnt = zip(*degreeCount.items())

plt.bar(deg, cnt, width=0.10, color='b')
plt.title("Vertex degree distribution")
plt.ylabel("No. of vertices")
plt.xlabel("Degree")
axes = plt.gca()
axes.set_xlim([0, 60])
axes.set_ylim([0, 40000])
plt.show()

# # # # compute index of power distribution using linear regression for completion of cumulative distribution of vertex
# # # # degree distribution for logarithmic bins

# get logarithmic bins
logIntervals = np.logspace(2.2, 3, 7, dtype=int)
degrees = [val for (node, val) in largest_cc_graph.degree()]

# count vertices in bins
degreeBaskets = []
for i in logIntervals:
    intervalSum = sum(1 for x in degrees if x > i)
    degreeBaskets.append(intervalSum)

# count frequency of degrees in bins
frequencyOfDegrees = nx.degree_histogram(largest_cc_graph)
frequencyBaskets = []
for i in logIntervals:
    frequencyInterval = frequencyOfDegrees[i]
    frequencyBaskets.append(frequencyInterval)

# linear regression
x = np.array(degreeBaskets).reshape((-1, 1))
y = np.array(frequencyBaskets)

model = LinearRegression().fit(x, y)
pred = model.predict(x)

plt.plot(logIntervals, frequencyBaskets, 'b.')
plt.plot(logIntervals, pred, 'r-', label='linear regression')
plt.xlabel('Degree of vertex')
plt.ylabel('Frequency')
plt.legend()
plt.show()

# # print Hill's distribution

fit = powerlaw.Fit(np.array(degree_sequence) + 1, xmin=1, discrete=True)
fit.power_law.plot_pdf(color='b', linestyle='--', label='PDF - sample')
fit.plot_pdf(color='g', label='PDF - data[HILL]')
plt.legend()
plt.show()
