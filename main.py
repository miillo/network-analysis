import networkx as nx
from random import choice
import operator
import itertools
import collections
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import powerlaw


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

# #######################T O D O################################
# find no. of k-cores with highest possible k
# print('First shot')
# print_k_cores(largest_cc_graph)
#
# # unfreeze graph
# newOne = nx.Graph(largest_cc_graph)
#
# print('\nSecond shot')
# to_del1 = [node for node, degree in dict(newOne.degree()).items() if degree > 155]
# newOne.remove_nodes_from(to_del1)
# print_k_cores(newOne)

# print('\nThird shot')
# to_del2 = [node for node, degree in dict(largest_cc_graph.degree()).items() if degree > 155]
# ts = ss.remove_nodes_from(to_del2)
# print_k_cores(ts)

# first analysis showed that k = 155 is highest
#cutDegrees = cut_degree(largest_cc_graph, 156)
#print_k_cores(cutDegrees)

# DEBUG
# print(dict(largest_cc_graph.degree()).items())
# for node, degree in dict(largest_cc_graph.degree()).items():
#     if degree > 2000:
#         print('NODE: ' + node + ' | DEGREE: ' + str(degree))

########################################################

# Distribution of nodes degrees
# degree_sequence = sorted([d for n, d in largest_cc_graph.degree()], reverse=True)
# degreeCount = collections.Counter(degree_sequence)
# deg, cnt = zip(*degreeCount.items())
#
# plt.bar(deg, cnt, width=0.10, color='b')
#
# plt.title("Degree Histogram")
# plt.ylabel("Count")
# plt.xlabel("Degree")
# axes = plt.gca()
# axes.set_xlim([0,60])
# axes.set_ylim([0,14000])
# plt.show()

########################################################
# wyznacz wykładnik rozkładu potęgowego metodą regresji dla dopełnienia dystrybuanty rozkładu stopni, dla przedziałów
# rozlokowanych logarytmicznie

# wyznaczenie kubelkow
res = np.logspace(1, 3, 7, dtype = int)
# zapis stopni w. w liście
degrees = [val for (node, val) in largest_cc_graph.degree()]

# zliczenie w. o podanych st. w kubełkach
degreeBasket = []
for i in res:
    ww = sum(1 for x in degrees if x > i)
    degreeBasket.append(ww)

# pobranie częstości st. w
frequencyOfDegrees = nx.degree_histogram(largest_cc_graph)
frequencyBaskets = []
for i in res:
    ww = frequencyOfDegrees[i]
    frequencyBaskets.append(ww)

# regresja
# x = np.array(degreeBasket).reshape((-1,1))
# y = np.array(frequencyBaskets)
#
# model = LinearRegression().fit(x,y)
# r_sq = model.score(x,y)
# pred = model.predict(x)
#
# print(str(degreeBasket))
# print(str(frequencyBaskets))
#
# plt.plot(res, frequencyBaskets, 'b.')
# plt.plot(res, pred, 'r-', label = 'linear regression')
# plt.xlabel('Node degree')
# plt.ylabel('Node frequency')
# plt.legend()
# plt.show()


# diagram hilla - pakiet lawpace

# working sample # # #
# d=[6, 4, 0, 0, 0, 0, 0, 1, 3, 1, 0, 3, 3, 0, 0, 0, 0, 1, 1, 0, 0, 0, 3,2,  3, 3, 2, 5, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 2, 1, 0, 1, 0, 0, 0, 0, 1,0, 1, 2, 0, 0, 0, 2, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1,3, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 2, 2, 3, 2, 1, 0, 0, 0, 1, 2]
# fit = powerlaw.Fit(np.array(d)+1,xmin=1,discrete=True)
# fit.power_law.plot_pdf( color= 'b',linestyle='--',label='fit ccdf')
# fit.plot_pdf( color= 'b')
# plt.show()
# print('alpha= ',fit.power_law.alpha,'  sigma= ',fit.power_law.sigma)

print(frequencyOfDegrees)

fit = powerlaw.Fit(np.array(frequencyOfDegrees) + 1, xmin= 1, discrete= True)
fit.power_law.plot_pdf(color='b', linestyle='--',label='Fit ccdf')
fit.plot_pdf( color= 'b')
plt.show()
print('alpha= ',fit.power_law.alpha,'  sigma= ',fit.power_law.sigma)

# fit = powerlaw.Fit(frequencyOfDegrees)
# powerlaw.plot_pdf(frequencyOfDegrees)
# plt.show()
# fig2 = fit.plot_pdf(color = 'b', linewidth = 2)
# fit.power_law.plot_pdf(color = 'b')
# print(fit.power_law.alpha)
# fig2 = fit.plot_pdf(color = ‘b’, linewidth = 2)
# print(fit.xmin)
# print(fit.alpha)
# powerlaw.plot_pdf()



# print('Largest connected component parameters')
# print('No. of nodes: ' + str(largest_cc_graph.number_of_nodes()))
# print('No. of edges: ' + str(largest_cc_graph.number_of_edges()))


print('\nEnd of processing')

# ! ! ! Tutorial sample degree plot
# all_deg = list(dict(nx.degree(largest_cc_graph)).values())
# unique_deg = list(set(all_deg))
# count_of_deg = []
# for i in unique_deg:
#     x = all_deg.count(i)
#     count_of_deg.append(x)
#
# axes = plt.gca()
# axes.set_xlim([0,60])
#
# plt.bar(unique_deg, count_of_deg)
# plt.show()
