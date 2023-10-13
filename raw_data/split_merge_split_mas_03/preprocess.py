import os

import networkx as nx
import numpy as np
from scipy import sparse

os.mkdir("/Users/teo/Desktop/Tesi Magistrale/FASE 1/DySAT_new/data/split_merge_split_mas_03")

graph_list = []
attr_list = []

found_num_attr = False
num_node_graph = []

for i in range(0, 10):
    ctr = 0
    with open('t{num}.graph'.format(num=i), 'r') as file:
        next(file)
        for line in file:
            if not found_num_attr:
                num_attr = line.count(';') - 1
                found_num_attr = True
            if not '#' in line:
                ctr += 1
            elif '#' in line:
                break

    num_node_graph.append(ctr)


max_node = 0
node_in_graph = []
edge_in_graph = []
label_in_graph = []

for i in range(0, 10):

    nodes = []
    edges = []
    labels = []
    node_attr = np.zeros((num_node_graph[i], num_attr))
    ctr = 0

    # Define the filename of your text file
    file_name = 't{num}.graph'.format(num=i)

    part_node = True
    with open(file_name, 'r') as file:
        next(file)
        for line in file:
            if part_node:
                if '#' in line:
                    node_in_graph.append(nodes)
                    part_node = False
                else:
                    el = line.split(';')
                    attr = el[1:num_attr + 1]
                    numeric_attr = [float(attr[i]) for i in range(0, num_attr)]
                    node_attr[ctr] = numeric_attr
                    labels.append(int(el[num_attr+1]))
                    nodes.append(int(el[0]))
                    ctr += 1
                    if int(el[0]) > max_node:
                        max_node = int(el[0])
            elif not part_node:
                if '# Edges' in line:
                    continue
                else:
                    pos = line.find(';')
                    first_node = int(line[0:pos])
                    second_node = int(line[pos + 1:-1])
                    # print(type(line)) #what is line dtype?
                    # first_node = line.
                    edges.append((first_node, second_node))

    edge_in_graph.append(edges)
    label_in_graph.append(labels)
    snode_attr = sparse.csr_matrix(node_attr)
    attr_list.append(snode_attr)

print(max_node)


for i in range(0, 10):
    node_idx = {}
    ctr = 0
    for node in node_in_graph[i]:
        if node not in node_idx:
            node_idx[node] = ctr
            #idx_node.append(node)
            ctr += 1

    G = nx.Graph()
    for node in node_in_graph[i]:
        G.add_node(node_idx[node])
    for edge in edge_in_graph[i]:
        G.add_edge(node_idx[edge[0]], node_idx[edge[1]])

    graph_list.append(G)
    #print(G.edges())
    #raw_input("Press Enter to continue...")








# for i in range(0, 10):
#     #print iteration
#     print(i)
#
#     # Define the filename of your text file
#     file_name = 't{num}.graph'.format(num=i)
#
#     # Initialize a flag to indicate whether we have found '# Edges'
#     found_edges = False
#
#     # Initialize a flag to indicate whether we have found the number of attributes
#     found_num_attr = False
#
#     # Create a list to store the lines before '# Edges'
#     lines_before_edges = []
#
#     # Create a list to store the lines after '# Edges'
#     lines_after_edges = []
#
#     # Open the file for reading
#     with open(file_name, 'r') as file:
#         # Skip the first line
#         next(file)
#         # Read the file line by line
#         for line in file:
#             # Check if the line contains '# Edges'
#             if '# Edges' in line:
#                 found_edges = True
#                 continue  # Skip the line that contains '# Edges' itself
#             elif '#' in line:
#                 continue
#             else:
#                 lines_before_edges.append(line)
#                 if not found_num_attr:
#                     num_attr = line.count(';') - 1
#                     found_num_attr = True
#             # If we have found '# Edges' and not encountered another line with it, add the line to the list
#             if found_edges:
#                 lines_after_edges.append(line)
#
#     #Create scipy sparse matrix to store node attributes
#     node_attr = np.zeros((len(lines_before_edges), num_attr))
#     label = np.zeros(len(lines_before_edges))
#     for line in lines_before_edges:
#         element = line.split(';')
#         #for el in element:
#             #print(el)
#         node = int(element[0])
#         attr = element[1:num_attr+1]
#         numeric_attr = [float(attr[i]) for i in range(0, num_attr)]
#         node_attr[node] = numeric_attr
#         label[node] = element[num_attr]
#
#     snode_attr = sparse.csr_matrix(node_attr)
#     attr_list.append(snode_attr)
#
#     # Create list of tuples to store the edges
#     edge_list = []
#     for line in lines_after_edges:
#         pos = line.find(';')
#         first_node = int(line[0:pos])
#         second_node = int(line[pos+1:-1])
#         #print(type(line)) #what is line dtype?
#         #first_node = line.
#         edge_list.append((first_node, second_node))

    # #print(edge_list)
    # G = nx.Graph(edge_list)
    # #print(G.edges())
    # #raw_input("Press Enter to continue...")
    # graph_list.append(G)
    # #graph_data_list = [nx.node_link_data(G) for G in graph_list]

# Save the graph list
#np.savez('/Users/teo/Desktop/Tesi Magistrale/FASE 1/DySAT/data/split_merge_split_mas_03/graphs.npz', graph=graph_data_list)
np.savez('/Users/teo/Desktop/Tesi Magistrale/FASE 1/DySAT_new/data/split_merge_split_mas_03/graphs.npz', graph=graph_list)
# Save the attribute list
np.savez('/Users/teo/Desktop/Tesi Magistrale/FASE 1/DySAT_new/data/split_merge_split_mas_03/features.npz', features=attr_list)