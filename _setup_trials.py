import pandas as pd


def setup_trials(ind_variables, conf_variables):
	trials_df = pd.read_csv("./trials/trials_exp1.csv")
	techniques_df = pd.read_csv("./trials/techniques.csv")


	trials_per_participants = {}

	participants = trials_df.columns.values[1:] 
	## filter "Unnamed: " columns
	participants = [participant for participant in participants if "Unnamed" not in participant]

	for i, participant in enumerate(participants):
		trial_ind = trials_df[participant].values
		trial_conf = trials_df[f'Unnamed: {(i+1)*2}'].values
		technique = techniques_df[participant].values

		trial_key = [f"{ind}_{conf}_{tech}" for ind, conf, tech in zip(trial_ind, trial_conf, technique)]

		trials_per_participants[participant] = trial_key
	

	trial_infos_per_participants = {}

	for participant in participants:

		trial_infos = []

		for i, trial_key in enumerate(trials_per_participants[participant]):

			ind, conf, tech = trial_key.split("_")

			if i == 0 or i == 9 or i == 18 or i == 27:
				trial_info = {
					"stage": "training",
					"technique": tech
				}
				trial_infos.append(trial_info)
			
			ind = ind_variables[ind]
			conf = conf_variables[conf]

			trial_info = {
				"stage": "experiment",
				"technique": tech,
			}
			for ind_key, ind_value in ind.items():
				trial_info[ind_key] = ind_value
			
			for conf_key, conf_value in conf.items():
				trial_info[conf_key] = conf_value
			
			trial_infos.append(trial_info)
		
		trial_infos_per_participants[participant] = trial_infos
		
	
	return trial_infos_per_participants


	## training은 무조건 같은 세팅 같은 임베딩 쓰자

	

