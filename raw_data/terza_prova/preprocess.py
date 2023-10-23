import os

import networkx as nx
import numpy as np
from scipy import sparse


found_num_attr = False

with open('t0.graph', 'r') as file:
    next(file)
    for line in file:
        if not found_num_attr:
            num_attr = line.count('|') + 1
            found_num_attr = True

feature_mat_list = []
graph_list = []
labels_list = []

for i in range(0, 100):
    print("Processing graph: ", i)
    found_edges = False
    skipped_line = False
    feature_list = []
    labels = []
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
                eliminate_node = line.split(';')
                el = eliminate_node[1].split('|')
                if num_attr > 1:
                    feature_list.append(np.array([float(el[j]) for j in range(0, num_attr)]))
                else:
                    feature_list.append(float(el[0]))
                labels.append(int(eliminate_node[2]))

    G = nx.Graph()
    G.add_edges_from(edges)
    adj = nx.to_numpy_matrix(G)  # Prova salvare matrice adiacenza
    sadj = sparse.csr_matrix(adj)
    graph_list.append(sadj)
    print("Graph: ", i, " has ", G.number_of_nodes(), " nodes and ", G.number_of_edges(), " edges.")

    feature_matrix = np.array(feature_list)
    s_feature_matrix = sparse.csr_matrix(feature_matrix)
    feature_mat_list.append(s_feature_matrix)

    label_arr = np.array(labels)
    s_labels = sparse.csr_matrix(label_arr)
    labels_list.append(s_labels)

#print(graph_list[0].number_of_edges())

os.mkdir("/Users/teo/Desktop/Tesi Magistrale/DySAT/data/terza_prova")

# Save the graph list
np.savez('/Users/teo/Desktop/Tesi Magistrale/DySAT/data/terza_prova/graphs.npz', graph=graph_list)
# Save the attribute list
np.savez('/Users/teo/Desktop/Tesi Magistrale/DySAT/data/terza_prova/features.npz', features=feature_mat_list)
# Save the labels list
np.savez('/Users/teo/Desktop/Tesi Magistrale/DySAT/data/terza_prova/labels.npz', labels=labels_list)