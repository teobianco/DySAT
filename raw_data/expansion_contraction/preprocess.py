import os
import networkx as nx
import numpy as np
from scipy import sparse


count = 0
dir_path = '/Users/teo/Desktop/Tesi Magistrale/FASE 1/DySAT_new/raw_data/expansion_contraction/expansion_contraction_data'  #path to the directory containing the graphs
for path in os.listdir(dir_path):
    # check if current path is a file
    if os.path.isfile(os.path.join(dir_path, path)):
        count += 1
print('File count:', count)

length = count
graph_list = []
for i in range(length):
    # Step 1: Read adjacency data from a file
    file_path = dir_path + '/{i}'.format(i=i+1)
    label_path = '/Users/teo/Desktop/Tesi Magistrale/FASE 1/DySAT_new/raw_data/expansion_contraction/expansion_contraction_groundtruth' + '/expand.t0{n}.comm'.format(n=i+1)

    # Initialize an empty graph
    G = nx.MultiGraph()

    # Step 2: Add nodes (if not already known)
    # You can add nodes explicitly or based on the adjacency data
    for j in range(1000):
        G.add_node(j+1)

    # Step 3: Read and add edges based on the adjacency data
    with open(file_path, "r") as file:
        for line in file:
            nodes = line.strip().split()  # Assuming the file has space-separated nodes
            if len(nodes) == 2:
                node1, node2 = nodes
                G.add_edge(int(node1), int(node2))
                G.add_edge(int(node2), int(node1))

    # Step 4: Add the graph to the list of graphs
    adj = nx.to_numpy_matrix(G)  # Prova salvare matrice adiacenza
    sadj = sparse.csr_matrix(adj)
    graph_list.append(sadj)

    labels = np.zeros(1000)
    # Step 5: Add the labels to the list of labels
    i = 1
    with open(label_path, "r") as l_file:
        for line in l_file:
            nodes = line.split()
            for node in nodes:
                labels[int(node)-1] = i
            i += 1

# Create directory to store the graphs
os.mkdir("/Users/teo/Desktop/Tesi Magistrale/FASE 1/DySAT_new/data/expansion_contraction")

# Save the graph list
np.savez('/Users/teo/Desktop/Tesi Magistrale/FASE 1/DySAT_new/data/expansion_contraction/graphs.npz', graph=graph_list)
# Save the labels
np.savez('/Users/teo/Desktop/Tesi Magistrale/FASE 1/DySAT_new/data/expansion_contraction/labels.npz', labels=labels)