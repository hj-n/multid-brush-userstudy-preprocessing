import numpy as np

def assign_trial_infos_to_specs(trial_infos, specs_arr):

	for participants in trial_infos.keys():
		trial_info = trial_infos[participants]

		for trial in trial_info:
			if trial["stage"] == "experiment":
				key = f"point_{trial['point_number']}_class_{trial['cluster_number']}_nontriviality_{trial['nontriviality']}_distortion_{trial['distortion_amount']}"
				matching_spec = []
				# print(key)
				for spec in specs_arr:
					if spec['key'] == key:
						matching_spec.append(spec)
				## random pick
				connected_spec = np.random.choice(matching_spec)
				trial["classes"] = connected_spec["classes"]
				trial["target"] = connected_spec["target"]
			elif trial["stage"] == "training":
				trial["classes"] = [2, 3, 6, 7]
				trial["target"] = 7
				trial["distortion_amount"] = "pca"
				trial["point_number"] = 300
		
