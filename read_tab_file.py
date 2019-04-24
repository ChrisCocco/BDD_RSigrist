# -*- coding: utf-8 -*-

import pandas as pd
import re


dfsA1  = pd.read_html('DATA/BaseA1.htm', header = 0)
dfsA2  = pd.read_html('DATA/BaseA2.htm', header = 0)

dataA1 = dfsA1[0]
dataA2 = dfsA2[0]

dataA  = pd.concat([dataA1, dataA2], sort = False)
# Two columns do not have the same name in both databases: 
# "Corrections" for A1 and "Corr. BMS" for A2 (no prob, not used)

#dataA = dataA1


# print(dataA1.loc[:,"Numéro"])
# print(dataA1["Numéro"]) #is equivalent to the line above

# #print(dataA1["Numéro"] == 1) # => TRUE or FALSE
# dataA1.loc[lambda df: df.Numéro == 1, :]

printout   = str()

printout = "INSERT INTO Savants (id_savant, type_savant, nom, prenom, " +\
	"naissance_date, naissance_date_certitude, naissance_date_comment," +\
	"mort_date, mort_date_certitude, mort_date_comment, naissance_lieu,"+\
	"mort_lieu, discipl_1, nbre_acad, gasc, id_type_eminence) VALUES\n"

for index, row in dataA.iterrows():

	id_savant = str(row['Numéro']).zfill(4)

	name = str(row['Nom'])
	if name == "nan" or name == "vide":
		continue
	name = name.replace("'", "\\\'")

	firstname = str(row['Prénom'])
	firstname = firstname.replace("'", "\\\'")

	born_date = str(row['Né'])
	if re.match('^[0-9]{4}$', born_date):
		born_date_cert = str(1)
		born_comment   = 'NULL'
	else:
		born_date_cert = str(0)
		born_comment   = born_date[5:]
		born_date      = born_date[0:4]

	death_date = str(row['Mort'])
	if re.match('^[0-9]{4}$', death_date):
		death_date_cert = str(1)
		death_comment   = 'NULL'
	else:
		death_date_cert = str(0)
		death_comment   = death_date[5:]
		death_date      = death_date[0:4]

	born_place  = str(row['Lieu naiss.'])
	if born_place == "nan":
		born_place = 'NULL'
	else:
		born_place  = born_place.replace("'", "\\\'")
	
	death_place = str(row['Lieu mort'])
	if death_place == "nan":
		death_place = 'NULL'
	else:
		death_place = death_place.replace("'", "\\\'")

	discipl_1   = str(row['Discipl. 1'])
	discipl_1   = discipl_1.replace("'", "\\\'")
	# discipl_2, etc.

	try:
		nbre_acad   = str(int(row['Nbre acad.']))
	except:
		print("Prob about nbre_acad with ", id_savant, row['Nbre acad.'], "NULL introduced")
		nbre_acad   = 'NULL'

	if str(row['Gasc.']) == "oui":
		gasc_bin = 1
	elif str(row['Gasc.']) == "non" or pd.isna(row['Gasc.']):
		gasc_bin = 0
	else:
		print("Prob about Gasc. with ", id_savant)

	if str(row['AA et AAA']) == "oui/oui":
		type_eminence = 1
	elif str(row['AA et AAA']) == "oui/non" or "oui//non":
		type_eminence = 2
	elif str(row['AA et AAA']) == "non/non" or "non / non":
		type_eminence = 3
	else:
		print("Prob about eminence type with ", id_savant, str(row['AA et AAA']))

		
	printrow  = '(\'' + id_savant + '\', \'A\',\'' + name + '\', \'' +\
				 firstname + '\',' + born_date + ',' + born_date_cert + ',\''+\
				 born_comment + '\',' + death_date + ',' + death_date_cert +\
				 ',\'' + death_comment + '\', \'' + born_place + '\', \'' +\
				 death_place + '\', \'' + discipl_1 + '\',' +\
				 nbre_acad + ',' + str(gasc_bin) + ',' + str(type_eminence) +\
				 '),\n'

	printrow  = printrow.replace("'NULL'", "NULL")

	printout += printrow



# COULD BE A SOLUTION FOR SPECIAL CHARACTER such as ' \' '
# for row in dataA1.itertuples():
# 	print(row)

# print(printout)
with open("data_for_sql/savants.sql", mode = "w", encoding = "utf8") as f: #mode "a" for the followings
	f.write(printout[:-2]) #-2 to remove the last ",\n"






