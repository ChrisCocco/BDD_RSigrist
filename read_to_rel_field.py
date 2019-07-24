# -*- coding: utf-8 -*-

import pandas as pd
import re
import functools # to use "reduce"

dfsA1  = pd.read_html('DATA/BaseA1.htm', header = 0)
dfsA2  = pd.read_html('DATA/BaseA2.htm', header = 0)

dfsB1  = pd.read_html('DATA/BaseB1.htm', header = 0)
dfsB2  = pd.read_html('DATA/BaseB2.htm', header = 0)

dataA1 = dfsA1[0]
dataA2 = dfsA2[0]

dataB1 = dfsB1[0]
dataB2 = dfsB2[0]

dataA  = pd.concat([dataA1, dataA2], sort = False, ignore_index = True)
# Two columns do not have the same name in both databases: 
# "Corrections" for A1 and "Corr. BMS" for A2 (no prob, not used)


dataB2.rename(columns = {"Pays":"Pays 1"}, inplace = True)
# Eleven columns still not have the same name (Pays corrected), maybe to 
# correct later depending on the useful columns
dataB  = pd.concat([dataB1, dataB2], sort = False, ignore_index = True)

print("data loaded")

printout_field     = str()

printout_rel_field = str()

printout_field = "INSERT INTO Champs (id_champ, champ) VALUES\n"

printout_rel_field = "INSERT INTO Rel_champs_savants (id_savant, type_savant,"+\
	"id_champ, champ_interpret, champ_principal) VALUES\n"

dict_field  = dict()


# all_fields = set(
# 	list(dataA.champ1.unique())+
# 	list(dataA.champ2.unique())+
# 	list(dataA.champ3.unique())+
# 	[item for sublist in 
# 		[item.split(" @ ") for item in dataA.champ4.unique() if not pd.isna(item)] 
# 		for item in sublist
# 	] +
# 	list(dataB['Champ 1'].unique())+
# 	list(dataB['Champ 2'].unique())+
# 	[item for sublist in 
# 		[item.split(" @ ") for item in dataB['Champ 3'].unique() if not pd.isna(item)] 
# 		for item in sublist
# 	]
# 	)

accents = (u'\x92', u"'"), ('é', 'e'), ('è', 'e'), ('â', 'a'), ('ö', 'o'), \
		('ü', 'u'), ("(",""), (")",""), (".","")


# all_fields = [functools.reduce(
# 				lambda a, kv: a.replace(*kv), accents, field
# 				) 
# 				for field in all_fields if not pd.isna(field)]

# all_fields = [field.lower() for field in all_fields]

# all_fields = list(set(all_fields))

# https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
def levenshtein(s1, s2):
	if len(s1) < len(s2):
		return levenshtein(s2, s1)
	# len(s1) >= len(s2)
	if len(s2) == 0:
		return len(s1)
	previous_row = range(len(s2) + 1)
	for i, c1 in enumerate(s1):
		current_row = [i + 1]
		for j, c2 in enumerate(s2):
			insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
			deletions = current_row[j] + 1       # than s2
			substitutions = previous_row[j] + (c1 != c2)
			current_row.append(min(insertions, deletions, substitutions))
		previous_row = current_row
	return previous_row[-1]

# double_set = set()

# for i in range(len(all_fields)):
# 	for j in range(i+1, len(all_fields)):
# 		leven_dist = levenshtein(all_fields[i], all_fields[j])
# 		if leven_dist < 2:
# 			print(all_fields[i], all_fields[j])
# 			double_set.add(all_fields[j])


# print(double_set)

# all_fields = [field for field in all_fields if field not in double_set]

# print(all_fields)

# ['physique th.', 'physique maths', 'science de la terre', 'biomed', 'tehcniques', 'sciences de la terr', 'astronomie @ biomed', 'physique math. et exper.', 'pluridisciplinaire', 'physique exp.', 'sciencesen general', 'physique theorique', 'histoire naturelle @ biomed', 'sciences en genreal', 'maths', 'physique exper.', 'histoie naturelle', 'physique @ astronomie', 'physique experimentale', 'hist-philo-pedago', 'physique theor.', 'scoemces en general', 'physique generale', 'hist - philo - pedago', 'terre', 'biomed @ histoire naturelle', 'theologie', 'sciences sociales', 'geologie', 'biologie', 'philosophie', 'lettres', 'chimie', 'techniques', 'physique', 'astronomie', 'philo', 'agronomie']

# manual_list_fields = [
# 	'agronomie',
# 	'astronomie',
# 	'astronomie @ biomed',
# 	'biologie', # à regrouper avec biomed
# 	'biomed',
# 	'chimie', 
# 	'géologie',
# 	'hist-philo-pedago', # à regrouper avec philo selon proposition René? Mais philosphie avec philo aussi? Aussi pour hist - philo - pedago
# 	'histoire naturelle', 
# 	'histoire naturelle @ biomed',
# 	'lettres',
# 	'maths', 
# 	'philo', 
# 	'philosophie', 
# 	'physique', 
# 	'physique @ astronomie', 
# 	'physique expérimentale', # regrouper avec physique exp et physique exper
# 	'physique générale', 
# 	'physique math. et exper.', 
# 	'physique maths', 
# 	'physique théorique', # regrouper avec phyisique th, physique theor
# 	'pluridisciplinaire', 
# 	'sciences de la terre', 
# 	'sciences en général', 
# 	'sciences sociales', 
# 	'techniques', # regrouper avec technique	
# 	'terre', 
# 	'théologie',
# 	]

manual_list_fields = [
	'agronomie',
	'astronomie',
	'astronomie @ biomed',
	'biomed', # regrouper avec biologie
	'chimie', 
	'géologie',
	'histoire naturelle', 
	'histoire naturelle @ biomed',
	'lettres',
	'maths', 
	'philosophie', # regrouper avec hist-philo-pedago, hist - philo - pedago, philo
	'physique', 
	'physique @ astronomie', 
	'physique expérimentale', # regrouper avec physique exp et physique exper
	'physique générale', 
	'physique math. et exper.', 
	'physique maths', 
	'physique théorique', # regrouper avec phyisique th, physique theor
	'pluridisciplinaire', 
	'sciences de la terre', 
	'sciences en général', 
	'sciences sociales', 
	'techniques', # regrouper avec technique	
	'terre', 
	'théologie',
	]

for id_field, field in enumerate(manual_list_fields):
	field = functools.reduce(lambda a, kv: a.replace(*kv), accents, field)
	dict_field[field] = id_field + 1

id_field_max = len(manual_list_fields)


#################
#### A bases ####
#################

for index, row in dataA.iterrows():

	id_savant = str(row['Numéro']).zfill(4)

	if pd.notna(row['champ1']):
		field = str(row['champ1'])

		principal_field = 1

		if "(" not in field:
			interpret = 0
		else:
			interpret = 1

		field = functools.reduce(lambda a, kv: a.replace(*kv), accents, field)

		if field in dict_field:
			id_field = dict_field[field]
		# to check if "x @ y" instead of "y @ x"
		elif "@" in field and \
			field.split(" @ ")[1] + " @ " + field.split(" @ ")[0] in dict_field:

			id_field = dict_field[field.split(" @ ")[1] +\
				" @ " + field.split(" @ ")[0]]
		elif field == "physique exper" or field == "physique exp":
			id_field = dict_field["physique experimentale"]
		elif field == "biologie":
			id_field = dict_field["biomed"]
		else:
			print("Not in the list: ", field)


