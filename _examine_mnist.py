from sklearn.datasets import fetch_openml
import helpers.calinski_harabasz as ch

import numpy as np 
from tqdm import tqdm

from sklearn.preprocessing import StandardScaler

from sklearn.decomposition import PCA

import os

## import mnist


def import_mnist():

	if not os.path.exists("./mnist/data.npy"):
			
		mnist = fetch_openml('mnist_784', version=1)
		data = mnist.data
		label = mnist.target

		data = data[::10]
		label = label[::10]

		np.save("./mnist/data.npy", data)
		np.save("./mnist/label.npy", label)

	else:
		data = np.load("./mnist/data.npy", allow_pickle=True)
		label = np.load("./mnist/label.npy", allow_pickle=True)


	data_reduced = PCA(n_components=10).fit_transform(data)
	data_reduced = StandardScaler().fit_transform(data_reduced)
	label = label.astype(np.int32)

	return data, data_reduced, label


def check_pairwise_sep(percentile_thrd, data, label):



	separable_pairs = []


	for label_i in range(10):
		for label_j in range(label_i + 1, 10):

			X_pair = data[((label == label_i) | (label == label_j))]
			label_pair = label[((label == label_i) | (label == label_j))]

			unique_labels = np.unique(label_pair)
			label_map = {old_label: new_label for new_label, old_label in enumerate(unique_labels)}
			label_pair = np.array([label_map[old_label] for old_label in label_pair], dtype=np.int32)

			score = ch.calinski_harabasz_adjusted(X_pair, label_pair)

			if score > percentile_thrd:
				separable_pairs.append((label_i, label_j))

	
	return separable_pairs	