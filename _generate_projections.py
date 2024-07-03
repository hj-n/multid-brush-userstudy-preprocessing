
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.random_projection import GaussianRandomProjection

from zadu import zadu
from bayes_opt import BayesianOptimization

from tqdm import tqdm

import numpy as np


def generate_projections(trial_infos, data, label):
	projections = []

	## generate a list of big random numbers without repetition
	np.random.seed(0)
	random_numbers = np.random.choice(1000, len(trial_infos) * len(trial_infos["P1"]), replace=False)
	identifier_idx = 0
	for participant in trial_infos:
		print("participant: ", participant)
		for trial in tqdm(trial_infos[participant]):
			classes = trial["classes"]
			distortion_amount = trial["distortion_amount"]
			point_number = trial["point_number"]

			data_selected = data[np.isin(label, classes)]
			label_selected = label[np.isin(label, classes)]

			## make each class to have number of "point_number" (randomly selected)
			data_sampled = []
			label_sampled = []

			for class_ in classes:
				data_class = data_selected[label_selected == class_]
				label_class = label_selected[label_selected == class_]

				idx = np.random.choice(data_class.shape[0], point_number, replace=False)

				data_sampled += data_class[idx].tolist()
				label_sampled += label_class[idx].tolist()
			
			data_sampled = np.array(data_sampled)
			label_sampled = np.array(label_sampled)
			if distortion_amount == "pca":
				pca = PCA(n_components=2)
				projection = pca.fit_transform(data_sampled)
			if distortion_amount == "low_distortion":
				projection = generate_low_distortion_projection(data_sampled)
			if distortion_amount == "high_mn":
				projection = generate_high_mn_projection(data_sampled)
			if distortion_amount == "high_fn":
				projection = generate_high_fn_projection(data_sampled)

			identifier = int(random_numbers[identifier_idx])
			projections.append({
				"projection": projection.tolist(),
				"identifier":	identifier
			})

			trial["identifier"] = identifier

			identifier_idx += 1
	
	
	return projections



			
	
def generate_low_distortion_projection(data):

	pbounds = {
		"perplexity": (2, np.min([500, data.shape[0] - 1]))
	}

	spec = [{
    "id"    : "tnc",
    "params": { "k": 5 },
	}]

	def projector(perplexity):
		projection = TSNE(n_components=2, perplexity=perplexity).fit_transform(data)
		scores = zadu.ZADU(spec, data).measure(projection)
		trust = scores[0]["trustworthiness"]
		conti = scores[0]["continuity"]
		f1_score_tnc = (2 * trust * conti) / (trust + conti)

		return f1_score_tnc
	
	optimizer = BayesianOptimization(
		f=projector,
		pbounds=pbounds,
		random_state=1,
		verbose=0
	)

	optimizer.maximize(
		init_points=10,
		n_iter=40
	)

	perplexity = optimizer.max["params"]["perplexity"]

	projection = TSNE(n_components=2, perplexity=perplexity).fit_transform(data)

	return projection





def generate_high_mn_projection(data):
	projection = TSNE(n_components=2, perplexity=1).fit_transform(data)

	return projection

def generate_high_fn_projection(data):
	projection = GaussianRandomProjection(n_components=2).fit_transform(data)

	return projection


