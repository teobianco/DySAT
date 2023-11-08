import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, DBSCAN
from sklearn.mixture import GaussianMixture
import numpy as np
from sklearn.manifold import TSNE
import scipy as sp
from sklearn.metrics import normalized_mutual_info_score as nmi
from sklearn.metrics import silhouette_score as sil
from sklearn.metrics import adjusted_rand_score as ari


time = 0

# Import the data
#X = np.load('/Users/teo/Desktop/Tesi Magistrale/FASE 1/DySAT_new/logs/DySAT_default/output/default_embs_birth_death_0.npz')['data']
X = np.load('/Users/teo/Downloads/default_embs_terza_prova_{t}-2.npz'.format(t=time), allow_pickle=True)['data']
labels = np.load('/Users/teo/Desktop/Tesi_Magistrale/DySAT/data/terza_prova/labels.npz', allow_pickle=True)['labels']
labels_0 = labels[time].todense()
#labels_0 = np.flatten(labels_0)
#labels_0.flatten()
#labels_0 = np.reshape(labels_0, (labels_0.shape[1], ))
labels_0 = np.ravel(labels_0)
cluster = DBSCAN(eps=0.16, min_samples=16).fit(X)
#cluster = GaussianMixture(n_components=10, random_state=0).fit(X)
#cluster_labels = cluster.predict(X)

# Plot the data

# Perform t-SNE projection
tsne = TSNE(n_components=2, perplexity=80, random_state=42)
Y = tsne.fit_transform(X)

# Create a scatter plot and color points by their labels
plt.figure(figsize=(8, 6))
scatter = plt.scatter(Y[:, 0], Y[:, 1], c=cluster.labels_, cmap='nipy_spectral')
plt.title('t-SNE Projection with Labels')
plt.xlabel('t-SNE Dimension 1')
plt.ylabel('t-SNE Dimension 2')
plt.colorbar(scatter, label='Labels')

#
plt.show()


print('NMI: ', nmi(cluster.labels_, labels_0))
print('Silhouette score: ', sil(X, labels_0))
print('ARI: ', ari(cluster.labels_, labels_0))
# # Create an empty list to store the sum of squared distances
# wcss = []
#
# # Determine the range of k (number of clusters) you want to test
# k_range = range(15, 35)
#
# # Calculate the sum of squared distances for different values of k
# for k in k_range:
#     kmeans = KMeans(n_clusters=k, random_state=0)
#     kmeans.fit(X)
#     wcss.append(kmeans.inertia_)
#
# # Plot the elbow method graph
# plt.figure(figsize=(8, 6))
# plt.plot(k_range, wcss, marker='o', linestyle='-')
# plt.title('Elbow Method for Optimal k')
# plt.xlabel('Number of Clusters (k)')
# plt.ylabel('Within-Cluster Sum of Squares (WCSS)')
# plt.grid()
# plt.show()
