import _find_percentile as fp
import _examine_mnist as em
import _nontriviality as nt
import _find_possible_class_sets as fpcs

## turn off warnings
import warnings
warnings.filterwarnings('ignore')


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