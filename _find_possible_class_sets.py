

def find_possible_class_sets(pairs):
	## 2-class sets
	two_classes_set = []

	for i in range(len(pairs)):
		two_classes_set.append([pairs[i][0], pairs[i][1]])
	
	## 3-class sets
	three_classes_set = []

	for i in range(len(pairs)):
		for j in range(i+1, len(pairs)):
			elements = [pairs[i][0], pairs[i][1], pairs[j][0], pairs[j][1]]
			elements_set = set(elements)
			if len(elements_set) == 3:
				elements_arr = list(elements_set)
				three_classes_set.append(elements_arr)
	
	## 4-class sets
	four_classes_set = []

	for i in range(len(three_classes_set)):
		for j in range(len(pairs)):
			elements = three_classes_set[i] + [pairs[j][0], pairs[j][1]]
			elements_set = set(elements)
			if len(elements_set) == 4:
				elements_arr = list(elements_set)
				four_classes_set.append(elements_arr)
	


	return two_classes_set + three_classes_set + four_classes_set


def construct_specs(classes_sets, nontriviality_arr):

	specs_arr = []

	for classes_set in classes_sets:
		for class_ in classes_set:
			spec = {
				"class_number": len(classes_set),
				"nontriviality": nontriviality_arr[class_],
				"classes": classes_set,
				"target": class_
			}
			for point_number in [100, 150, 200]:
				spec["point_number"] = point_number

				for distortion_amount in ["low_distortion", "high_mn", "high_fn"]:
					spec["distortion_amount"] = distortion_amount
					spec["key"] = f"point_{point_number}_class_{len(classes_set)}_nontriviality_{nontriviality_arr[class_]}_distortion_{distortion_amount}"

					specs_arr.append(spec.copy())
	
	

	return specs_arr
