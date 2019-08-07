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

accents = (u'\x92', u"'"), ('é', 'e'), ('è', 'e'), ('â', 'a'), ('ö', 'o'), \
		('ü', 'u'), ("(",""), (")",""), (".","")

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

def retrieve_field(field_name, dict_field_list):
	if not field_name.startswith("("):
		interpret = 0
	else:
		interpret = 1

	field_name = functools.reduce(
		lambda a, kv: a.replace(*kv), accents, field_name)

	if field_name in dict_field_list:
		id_field = dict_field_list[field_name]
	# to check if "x @ y" instead of "y @ x"
	elif "@" in field_name and \
		field_name.split(" @ ")[1] + " @ " + field_name.split(" @ ")[0] \
		in dict_field_list:
		id_field = dict_field_list[field_name.split(" @ ")[1] +\
			" @ " + field_name.split(" @ ")[0]]
	elif field_name == "physique exper" or field_name == "physique exp":
		id_field = dict_field_list["physique experimentale"]
	elif field_name == "biologie":
		id_field = dict_field_list["biomed"]
	elif field_name == "physique th" or field_name == "physique theor":
		id_field = dict_field_list["physique theorique"]
	elif field_name == "philo" or field_name == "hist-philo-pedago" or \
		field_name == "hist - philo - pedago":
		id_field = dict_field_list["philosophie"]
	else:
		dict_leven = dict()
		for field_saved, id_field in dict_field_list.items():
			leven_dist = levenshtein(field_name, field_saved)
			dict_leven[id_field] = leven_dist
			# if leven_dist < 2:
			# 	id_field = dict_field[field_saved]				
		dist_min = min(dict_leven.values())
		id_found = [
			id_field for id_field, dist in dict_leven.items() 
			if dist == dist_min
			]
		if len(id_found) == 1 and dist_min <= 2:
			id_field = id_found[0]
		else:
			print("Not in the list: ", field_name)
	return(interpret, id_field)

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
	'physique math.', 
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

		interpretation, id_field = retrieve_field(field, dict_field)

		printrow = '(\'' + id_savant + '\', \'A\',' + str(id_field) + ',' +\
				 	str(interpretation) + ',' + str(principal_field) + '),\n'

		printout_rel_field += printrow

	if pd.notna(row['champ2']):

		field = str(row['champ2'])

		principal_field = 0

		interpretation, id_field = retrieve_field(field, dict_field)

		printrow = '(\'' + id_savant + '\', \'A\',' + str(id_field) + ',' +\
				 	str(interpretation) + ',' + str(principal_field) + '),\n'

		printout_rel_field += printrow

	if pd.notna(row['champ3']):

		field = str(row['champ3'])

		principal_field = 0

		interpretation, id_field = retrieve_field(field, dict_field)

		printrow = '(\'' + id_savant + '\', \'A\',' + str(id_field) + ',' +\
				 	str(interpretation) + ',' + str(principal_field) + '),\n'

		printout_rel_field += printrow

	if pd.notna(row['champ4']):

		text = str(row['champ4'])

		if '@' not in text:

			field = text

			principal_field = 0

			interpretation, id_field = retrieve_field(field, dict_field)

			printrow = '(\'' + id_savant + '\', \'A\',' + str(id_field) + ',' +\
				 		str(interpretation) + ',' + str(principal_field) + '),\n'

			printout_rel_field += printrow

		else:

			fields_list = text.split(" @ ")

			for field in fields_list:

				principal_field = 0

				interpretation, id_field = retrieve_field(field, dict_field)

				printrow = '(\'' + id_savant + '\', \'A\',' + str(id_field) + ',' +\
				 			str(interpretation) + ',' + str(principal_field) + '),\n'

				printout_rel_field += printrow

print("A done")


#################
#### B bases ####
#################

for index, row in dataB.iterrows():

	id_savant = str(row['Numéro'])[0:4] # Take numbers, not "-B"

	if pd.notna(row['Champ 1']):

		field_1 = str(row['Champ 1'])

		principal_field = 1

		interpretation, id_field = retrieve_field(field_1, dict_field)

		printrow = '(\'' + id_savant + '\', \'B\',' + str(id_field) + ',' +\
				 	str(interpretation) + ',' + str(principal_field) + '),\n'

		printout_rel_field += printrow

	if pd.notna(row['Champ 2']):

		field_2 = str(row['Champ 2'])

		if field_2 != field_1:

			principal_field = 0

			interpretation, id_field = retrieve_field(field_2, dict_field)

			printrow = '(\'' + id_savant + '\', \'B\',' + str(id_field) + ',' +\
					 	str(interpretation) + ',' + str(principal_field) + '),\n'

			printout_rel_field += printrow

	if pd.notna(row['Champ 3']):

		text = str(row['Champ 3'])

		if '@' not in text:

			field = text

			principal_field = 0

			interpretation, id_field = retrieve_field(field, dict_field)

			printrow = '(\'' + id_savant + '\', \'B\',' + str(id_field) + ',' +\
				 		str(interpretation) + ',' + str(principal_field) + '),\n'

			printout_rel_field += printrow

		else:

			fields_list = text.split(" @ ")

			for field in fields_list:

				principal_field = 0

				interpretation, id_field = retrieve_field(field, dict_field)

				printrow = '(\'' + id_savant + '\', \'B\',' + str(id_field) + ',' +\
				 			str(interpretation) + ',' + str(principal_field) + '),\n'

				printout_rel_field += printrow




for field, id_field in dict_field.items():
		printout_field += '(' + str(id_field) + ', \'' + field + '\'),\n'

# print(printout)
with open("data_for_sql/champs_savants.sql", mode = "w", encoding = "utf8") as f:
	f.write(printout_field[:-2]) #-2 to remove the last ",\n"
	f.write(';\n\n')
	f.write(printout_rel_field[:-2]) #-2 to remove the last ",\n"


