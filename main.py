import networkx as nx
from random import choice
import operator
import itertools
import collections
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import powerlaw


# Wypisuje posortowane k-rdzenie oraz liczbę wierzchołków do nich należącą
def no_of_nodes_for_k_cores(graph):
    # liczba rdzeni dla każdego wierzchołka
    core_numbers = nx.core_number(graph)

    # zliczenie liczby wierzchołków dla każdego rdzenia
    inv_map = {}
    for k, v in core_numbers.items():
        inv_map[v] = inv_map.get(v, [])
        inv_map[v].append(k)

    mapped = {k: len(v) for k, v in inv_map.items()}
    sorted_core_numbers = collections.OrderedDict(sorted(mapped.items(), key=lambda kv: kv[0]))
    return sorted_core_numbers


# wczytanie grafu
G = nx.read_adjlist('C:\\Users\\Milosz\\Desktop\\TASS_Project_I\\Ex2_data\\3.txt')

# # # # # zbadaj jaki jest rząd i rozmiar całej sieci: pierwotnej oraz po usunięciu pętli i duplikatów krawędzi # # # #

# print('Rząd i rozmiar sieci pierwotnej')
# print('Liczba wierzchołków(rząd): ' + str(G.number_of_nodes()))
# print('Liczba krawędzi(rozmiar): ' + str(G.number_of_edges()))
#
# print()

# usunięcie pętli
G.remove_edges_from(nx.selfloop_edges(G))
# graf jest wczytany jako obiekt typu: 'networkx.classes.graph.Graph' - tzn. nie ma zduplikowanych krawędzi

# print('Rząd i rozmiar sieci po usunięciu pętli / duplikató krawędzi')
# print('Liczba wierzchołków(rząd): ' + str(G.number_of_nodes()))
# print('Liczba krawędzi(rozmiar): ' + str(G.number_of_edges()))
#
# print()

# # # # # wyodrębnij największą składową spójną, zbadaj jej rząd i rozmiar # # # #

# sprawdzenie liczby komponentów
# print('Liczba komponentów: ' + str(nx.number_connected_components(G)))

# generate largest connected component
largest_cc = max(nx.connected_components(G), key=len)
largest_cc_graph = G.subgraph(largest_cc)

# print('Rząd i rozmiar największej składowej spójnej')
# print('Liczba wierzchołków(rząd): ' + str(largest_cc_graph.number_of_nodes()))
# print('Liczba krawędzi(rozmiar): ' + str(largest_cc_graph.number_of_edges()))

# # # # # wyznacz aproksymacje średniej długości ścieżki,
# # # # # operując na próbie losowej 100, 1000 i 10 tys. par wierzchołków

# TODO dla trzech prob

sumOfShortestPaths = 0
noOfNodes = largest_cc_graph.number_of_nodes()
nodes = largest_cc_graph.nodes()

for i in range(0, 10):
    node1 = choice(list(nodes))
    node2 = choice(list(nodes))
    shortest_path_length = nx.dijkstra_path_length(largest_cc_graph, node1, node2)
    sumOfShortestPaths += shortest_path_length
    print('Iteration: ' + str(i) + ' | Current sum: ' + str(sumOfShortestPaths))

print(sumOfShortestPaths / (noOfNodes * (noOfNodes - 1)))

# print()

# # # # # wyznacz liczbę rdzeni o największym możliwym rzędzie, o drugim możliwie największym rzędzie
# # # # # o trzecim możliwie największym rzędzie; jakie to są rzędy? # # # #

# 'odmrożenie' grafu w celu umożliwienia wykonania na nim operacji
# unfrezeed = nx.Graph(largest_cc_graph)
#
# print('Pierwsze sprawdzenie liczby rdzeni: ' + str(no_of_nodes_for_k_cores(unfrezeed)))  # max 155
#
# # wyznaczenie wierzchołków do usunięcia na podstawie ostatniego odczytu
# to_del1 = [node for node, degree in dict(unfrezeed.degree()).items() if degree >= 155]
# unfrezeed.remove_nodes_from(to_del1)
#
# print('Drugie sprawdzenie liczby rdzenii: ' + str(no_of_nodes_for_k_cores(unfrezeed))) # max 67
#
# # wyznaczenie wierzchołków do usunięcia na podstawie ostatniego odczytu
# to_del2 = [node for node, degree in dict(unfrezeed.degree()).items() if degree >= 67]
# unfrezeed.remove_nodes_from(to_del2)
#
# print('Trzecie sprawdzenie liczby rdzenii: ' + str(no_of_nodes_for_k_cores(unfrezeed))) # max 53

# # # # wykreśl rozkład stopni wierzchołków

# degree_sequence = sorted([d for n, d in largest_cc_graph.degree()], reverse=True)
# degreeCount = collections.Counter(degree_sequence)
# deg, cnt = zip(*degreeCount.items())
#
# plt.bar(deg, cnt, width=0.10, color='b')
# plt.title("Rozkład stopni wierzchołków")
# plt.ylabel("Liczba wierzchołków")
# plt.xlabel("Stopień")
# axes = plt.gca()
# axes.set_xlim([0,60])
# axes.set_ylim([0,40000])
# plt.show()

# # # # wyznacz wykładnik rozkładu potęgowego metodą regresji dla dopełnienia dystrybuanty rozkładu stopni,
# # # # dla przedziałów rozlokowanych logarytmicznie


# TODO ffff
# # wyznaczenie przedziałów logarytmicznych
# logIntervals = np.logspace(1, 3, 7, dtype = int)
# # zapis stopni wierzchołków w liście
# degrees = [val for (node, val) in largest_cc_graph.degree()]
#
# # zliczenie wierzchołków w przedziałach
# degreeBaskets = []
# for i in logIntervals:
#     intervalSum = sum(1 for x in degrees if x > i)
#     degreeBaskets.append(intervalSum)
#
# # zliczenie częstotliwości stopni wierzchołków
# frequencyOfDegrees = nx.degree_histogram(largest_cc_graph)
# print(frequencyOfDegrees)
#
# frequencyBaskets = []
# for i in logIntervals:
#     frequencyInterval = frequencyOfDegrees[i]
#     frequencyBaskets.append(frequencyInterval)
#
# print(frequencyBaskets)
#
# # regresja
# x = np.array(degreeBaskets).reshape((-1, 1))
# y = np.array(frequencyBaskets)
#
# model = LinearRegression().fit(x, y)
# r_sq = model.score(x, y)
# pred = model.predict(x)
#
# plt.plot(logIntervals, frequencyBaskets, 'b.')
# plt.plot(logIntervals, pred, 'r-', label='linear regression')
# plt.xlabel('Stopień wierzchołka')
# plt.ylabel('Częstotliwość')
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

# print(frequencyOfDegrees)
#
# fit = powerlaw.Fit(np.array(frequencyOfDegrees) + 1, xmin= 1, discrete= True)
# fit.power_law.plot_pdf(color='b', linestyle='--',label='Fit ccdf')
# fit.plot_pdf( color= 'b')
# plt.show()
# print('alpha= ',fit.power_law.alpha,'  sigma= ',fit.power_law.sigma)

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
