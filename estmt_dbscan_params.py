from sklearn.neighbors import NearestNeighbors
from matplotlib import pyplot as plt
import numpy as np


time = 0

dataset = np.load('/Users/teo/Downloads/default_embs_terza_prova_{t}-2.npz'.format(t=time), allow_pickle=True)['data']

neighbors = NearestNeighbors(n_neighbors=16)
neighbors_fit = neighbors.fit(dataset)
distances, indices = neighbors_fit.kneighbors(dataset)

distances = np.sort(distances, axis=0)
distances = distances[:, 1]
plt.plot(distances)
plt.show()
