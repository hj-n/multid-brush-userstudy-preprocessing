import numpy as np

from sklearn.mixture import GaussianMixture

def check_nontriviality_digits(data, labels):

	log_likelihoods = []
	for label in np.unique(labels):
		X = data[labels == label]
		gmm = GaussianMixture(n_components=1, covariance_type='spherical')
		gmm.fit(X)

		log_likelihoods.append(gmm.score(X))
	
	nontriviality_arr = []
	## top three log-likihood: low, bottom three log-likelihood: high, middle four: medium

	low_percentile = np.percentile(log_likelihoods, 30)
	high_percentile = np.percentile(log_likelihoods, 70)

	for log_likelihood in log_likelihoods:
		if log_likelihood < low_percentile:
			nontriviality_arr.append("low")
		elif log_likelihood > high_percentile:
			nontriviality_arr.append("high")
		else:
			nontriviality_arr.append("medium")


	return nontriviality_arr
	