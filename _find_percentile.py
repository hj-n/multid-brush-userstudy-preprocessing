import helpers.calinski_harabasz as ch
import os

from tqdm import tqdm

import numpy as np 

from sklearn.preprocessing import StandardScaler


def find_90_percentile():
	labeled_datasets = os.listdir('./labeled-dataset/npy/')


	scores = []

	for dataset in tqdm(labeled_datasets):
		data = np.load('./labeled-dataset/npy/' + dataset + '/data.npy')
		label = np.load('./labeled-dataset/npy/' + dataset + '/label.npy')

		## scale data

		scaler = StandardScaler()
		data = scaler.fit_transform(data)


		unique_labels = np.unique(label)

		## change all labels to number 0~n
		label_map = {old_label: new_label for new_label, old_label in enumerate(unique_labels)}
		label = np.array([label_map[old_label] for old_label in label], dtype=np.int32)

		unique_labels = np.unique(label)

		scores.append(ch.calinski_harabasz_adjusted(data, label))


	return np.percentile(scores, 90)


