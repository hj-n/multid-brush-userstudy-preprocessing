

INDEPENDENT_VARIABLES = {
	"A": {
		"nontriviality": "low",
		"distortion_inspection": "no",
	},
	"B": {
		"nontriviality": "low",
		"distortion_inspection": "global",
	},
	"C": {
		"nontriviality": "low",
		"distortion_inspection": "global_local",
	},
	"D": {
		"nontriviality": "medium",
		"distortion_inspection": "no",
	},
	"E": {
		"nontriviality": "medium",
		"distortion_inspection": "global",
	},
	"F": {
		"nontriviality": "medium",
		"distortion_inspection": "global_local",
	},
	"G": {
		"nontriviality": "high",
		"distortion_inspection": "no",
	},
	"H": {
		"nontriviality": "high",
		"distortion_inspection": "global",
	},
	"I": {
		"nontriviality": "high",
		"distortion_inspection": "global_local",
	}
}


CONFOUNDING_VARIABLES = {
	"a": {
		"cluster_number": 2,
		"point_number": 100,
		"distortion_amount": "low_distortion"
	},
	"b": {
		"cluster_number": 3,
		"point_number": 100,
		"distortion_amount": "high_mn"
	},
	"c": {
		"cluster_number": 4,
		"point_number": 100,
		"distortion_amount": "high_fn"
	},
	"d": {
		"cluster_number": 2,
		"point_number": 150,
		"distortion_amount": "high_mn"
	},
	"e": {
		"cluster_number": 3,
		"point_number": 150,
		"distortion_amount": "high_fn"
	},
	"f": {
		"cluster_number": 4,
		"point_number": 150,
		"distortion_amount": "low_distortion"
	},
	"g": {
		"cluster_number": 2,
		"point_number": 200,
		"distortion_amount": "high_fn"
	},
	"h": {
		"cluster_number": 3,
		"point_number": 200,
		"distortion_amount": "low_distortion"
	},
	"i": {
		"cluster_number": 4,
		"point_number": 200,
		"distortion_amount": "low_distortion"
	}
}