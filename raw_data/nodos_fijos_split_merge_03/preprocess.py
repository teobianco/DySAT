import os

import networkx as nx
import numpy as np
from scipy import sparse


found_num_attr = False
max_node = 0

for i in range(0, 10):
    with open('t{num}.graph'.format(num=i), 'r') as file:
        next(file)
        for line in file:
            if '#' in line:
                break
            else:
                el = line.split(';')
                if int(el[0]) > max_node:
                    max_node = int(el[0])
            if not found_num_attr:
                num_attr = line.count(';') - 1
                found_num_attr = True

print("max_node: ", max_node)

feature_list = []
graph_list = []
labels_list = []

for i in range(0, 10):

    print("Processing graph: ", i)

    found_edges = False
    skipped_line = False
    feature_matrix = np.zeros((max_node+1, num_attr))
    labels = np.full((max_node+1,), -1)
    edges = []

    with open('t{num}.graph'.format(num=i), 'r') as file:
        next(file)
        for line in file:
            if found_edges and skipped_line:
                pos = line.find(';')
                first_node = int(line[0:pos])
                second_node = int(line[pos + 1:-1])
                # print(type(line)) #what is line dtype?
                # first_node = line.
                edges.append((first_node, second_node))
            if found_edges:
                skipped_line = True
            if '#' in line:
                found_edges = True
                continue
            elif not found_edges:
                el = line.split(';')
                if num_attr > 1:
                    feature_matrix[int(el[0])] = np.array([float(el[i]) for i in range(1, num_attr + 1)])
                else:
                    feature_matrix[int(el[0])] = float(el[1])
                labels[int(el[0])] = int(el[num_attr + 1])

    G = nx.Graph()
    for n in range(0, max_node+1):
        G.add_node(n)
    G.add_edges_from(edges)
    adj = nx.to_numpy_matrix(G)  # Prova salvare matrice adiacenza
    sadj = sparse.csr_matrix(adj)
    graph_list.append(sadj)
    print("Graph: ", i, " has ", G.number_of_nodes(), " nodes and ", G.number_of_edges(), " edges.")

    s_feature_matrix = sparse.csr_matrix(feature_matrix)
    feature_list.append(s_feature_matrix)

    s_labels = sparse.csr_matrix(labels)
    labels_list.append(s_labels)

#print(graph_list[0].number_of_edges())

os.mkdir("/Users/teo/Desktop/Tesi Magistrale/FASE 1/DySAT_new/data/nodos_fijos_split_merge_03")

# Save the graph list
np.savez('/Users/teo/Desktop/Tesi Magistrale/FASE 1/DySAT_new/data/nodos_fijos_split_merge_03/graphs.npz', graph=graph_list)
# Save the attribute list
np.savez('/Users/teo/Desktop/Tesi Magistrale/FASE 1/DySAT_new/data/nodos_fijos_split_merge_03/features.npz', features=feature_list)
# Save the labels list
np.savez('/Users/teo/Desktop/Tesi Magistrale/FASE 1/DySAT_new/data/nodos_fijos_split_merge_03/labels.npz', labels=labels_list)