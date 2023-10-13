import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np


# Import the data
X = np.load('/Users/teo/Desktop/Tesi Magistrale/FASE 1/DySAT_new/logs/DySAT_default/output/default_embs_birth_death_0.npz')['data']

# Create an empty list to store the sum of squared distances
wcss = []

# Determine the range of k (number of clusters) you want to test
k_range = range(15, 35)

# Calculate the sum of squared distances for different values of k
for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=0)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)

# Plot the elbow method graph
plt.figure(figsize=(8, 6))
plt.plot(k_range, wcss, marker='o', linestyle='-')
plt.title('Elbow Method for Optimal k')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Within-Cluster Sum of Squares (WCSS)')
plt.grid()
plt.show()
