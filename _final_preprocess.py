import numpy as np
import os, json
from _snnknn import KnnSnn as ks 
from scipy.spatial.distance import cdist
from scipy.sparse import csr_matrix




def knn(data, param):
	"""
	Compute distance matrix based on k-nearest neighbor (KNN)
	"""
	DEFAULT_K = 10

	k = param["k"] if "k" in param.keys() else DEFAULT_K

	kSnn = ks(k)
	knn_results = kSnn.knn(data)

	return knn_results


def snn(knn_results, param):
	"""
	Compute distance matrix based on shared nearest neighbor (SNN)
	"""
	DEFAULT_K = 10

	k = param["k"] if "k" in param.keys() else DEFAULT_K
	kSnn = ks(k)
	snn_results = kSnn.snn(knn_results)

	## normalize snn
	snn_results /= np.max(snn_results)

	return snn_results

def compute_distance(data, distance):
	"""
	Parse distance dictionary and 
	Computer distance matrix from the hd data
	"""
	metric = distance["metric"]
	param = distance["params"] if "params" in distance.keys() else None

	if metric == "euclidean" or metric == "cosine":
		dist_matrix = cdist(data, data, metric=metric)
	elif metric == "snn":
		knn_results = knn(data, param=param)
		dist_matrix = snn(knn_results, param=param)

	return dist_matrix

def convert_to_csr(dist_matrix):
	"""
	Convert distance matrix to csr matrix
	"""
	snn_csr = csr_matrix(dist_matrix)

	csr_data = snn_csr.data.tolist()
	csr_indptr = snn_csr.indptr.tolist()
	csr_indices = snn_csr.indices.tolist()


	return csr_data, csr_indptr, csr_indices

def preprocess(original_data, hd, ld, labels, max_neighbors):
	"""
	Preprocess the data and construct preprocessed info
	"""


	preprocessed = {}

	
	### Compute distance matrix of hd data and convert it to csr matrix
	distance = {
		"metric": "snn",
		"params": {
			"k": 10
		}
	}
	dist_matrix = compute_distance(hd, distance)
	csr_data, csr_indptr, csr_indices = convert_to_csr(dist_matrix)
	csr = {
		"data": csr_data,
		"indptr": csr_indptr,
		"indices": csr_indices
	}
	preprocessed["csr"] = csr

	### Compute knn graph regarding max_neighbors
	knn_max_neighbors = knn(hd, param={"k": max_neighbors})
	preprocessed["knn"] = knn_max_neighbors.tolist()



	### ADD HD, LD, and Labels (if exists)

	hd = hd.astype(np.float16)
	ld = ld.astype(np.float16)
	labels = labels.astype(np.int8) if labels is not None else None

	preprocessed["hd"] = original_data.tolist()
	preprocessed["original_data"] = hd.tolist()
	preprocessed["ld"] = ld.tolist()
	if labels is not None:
		preprocessed["labels"] = labels.tolist()



	return preprocessed