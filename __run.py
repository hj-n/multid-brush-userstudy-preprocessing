import _find_percentile as fp
import _examine_mnist as em
import _nontriviality as nt
import _find_possible_class_sets as fpcs
import _setup_trials as st
import _assign_trial_infos_to_specs as atis
import _generate_projections as gp

import _variables_exp1 as ve1

import json

## turn off warnings
import warnings
warnings.filterwarnings('ignore')


ve = ve1


print("Finding 90th percentile...")
percentile = fp.find_90_percentile()
print("Finished!!")


print("downlowding mnist data...")
data, label = em.import_mnist()
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
projections = gp.generate_projections(trial_infos, data, label)

## save results
print("saving results...")
with open("./trial_infos/trial_infos_exp1.json", "w") as f:
	json.dump(trial_infos, f)

for i, projection_info in enumerate(projections):
	projection_list = projection_info["projection"]
	identifier = projection_info["identifier"]

	with open(f"./trial_projections/exp1/{identifier}.json", "w") as f:
		json.dump(projection_list, f)