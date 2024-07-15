import _find_percentile as fp
import _examine_mnist as em
import _nontriviality as nt
import _find_possible_class_sets as fpcs
import _setup_trials as st
import _assign_trial_infos_to_specs as atis
import _generate_projections as gp
from tqdm import tqdm
import numpy as np

import _final_preprocess as fpre

import _variables_exp1 as ve1
import _variables_exp2 as ve2

import os

import json

## turn off warnings
import warnings
warnings.filterwarnings('ignore')

SETTING = "exp2"


if SETTING == "exp1":
	ve = ve1
elif SETTING == "exp2":
	ve = ve2


print("Finding 90th percentile...")
percentile = fp.find_90_percentile()
print("Finished!!")



print("downlowding mnist data...")
original_data, data, label = em.import_mnist()
print("Finding mnist pairs exceeding 90th percentile...")
pairs = em.check_pairwise_sep(percentile, data, label)
print("Finished!!")


print("Checking the non-triviality of the pairs...")
nontriviality_arr = nt.check_nontriviality_digits(data, label)


print("finding possible class sets...")
classes_sets = fpcs.find_possible_class_sets(pairs)

print("construct specs array...")
specs_arr = fpcs.construct_specs(classes_sets, nontriviality_arr)

print("constrct trials infos...")
trial_infos = st.setup_trials(ve.INDEPENDENT_VARIABLES, ve.CONFOUNDING_VARIABLES)

print("assigning trial infos to specs...")
atis.assign_trial_infos_to_specs(trial_infos, specs_arr)

print("generating projections...")
projections = gp.generate_projections(trial_infos, original_data, data, label)

## save results
print("saving results...")
with open(f"./trial_infos/trial_infos_{SETTING}.json", "w") as f:
	json.dump(trial_infos, f)

for i, projection_info in enumerate(projections):
	projection_list = projection_info["projection"]
	original_data_list = projection_info["original_data"]
	data_list = projection_info["data"]
	label_list = projection_info["label"]
	identifier = projection_info["identifier"]

	with open(f"./trial_data/{SETTING}/original_data/{identifier}.json", "w") as f:
		json.dump(original_data_list, f)

	with open(f"./trial_data/{SETTING}/projections/{identifier}.json", "w") as f:
		json.dump(projection_list, f)
	
	with open(f"./trial_data/{SETTING}/data/{identifier}.json", "w") as f:
		json.dump(data_list, f)
	
	with open(f"./trial_data/{SETTING}/labels/{identifier}.json", "w") as f:
		json.dump(label_list, f)




for file_name in tqdm(os.listdir(f"./trial_data/{SETTING}/original_data/")):

	with open(f"./trial_data/{SETTING}/original_data/{file_name}", "r") as f:
		original_data = json.load(f)
	
	with open(f"./trial_data/{SETTING}/projections/{file_name}", "r") as f:
		projection = json.load(f)
	
	with open(f"./trial_data/{SETTING}/data/{file_name}", "r") as f:
		hd = json.load(f)
	
	with open(f"./trial_data/{SETTING}/labels/{file_name}", "r") as f:
		labels = json.load(f)


	preprocessed = fpre.preprocess(np.array(original_data), np.array(hd), np.array(projection), np.array(labels), 50)

	with open(f"./trial_data/{SETTING}/preprocessed/{file_name}", "w") as f:
		json.dump(preprocessed, f)