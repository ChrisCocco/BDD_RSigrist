# -*- coding: utf-8 -*-

import pandas as pd
import re


dfs = pd.read_html('DATA/BaseA1.htm', header = 0)

dataA1 = dfs[0]    


# print(dataA1.loc[:,"Numéro"])
# print(dataA1["Numéro"]) #is equivalent to the line above

# #print(dataA1["Numéro"] == 1) # => TRUE or FALSE
# dataA1.loc[lambda df: df.Numéro == 1, :]

printout = str()

printout = "INSERT INTO Savants (id_savant, type_savant, nom, prenom, " +\
	"naissance_date, naissance_date_certitude, naissance_date_comment," +\
	"mort_date, mort_date_certitude, mort_date_comment, naissance_lieu,"+\
	"mort_lieu) VALUES\n"

for index, row in dataA1.iterrows():
	name = str(row['Nom'])
	if name == "nan":
		continue
	name = name.replace("'", "\\\'")

	firstname = str(row['Prénom'])
	firstname = firstname.replace("'", "\\\'")

	born_date = str(row['Né'])
	if re.match('^[0-9]{4}$', born_date):
		born_date_cert = str(1)
		born_comment   = str()
	else:
		born_date_cert = str(0)
		born_comment   = born_date[5:]
		born_date      = born_date[0:4]

	death_date = str(row['Mort'])
	if re.match('^[0-9]{4}$', death_date):
		death_date_cert = str(1)
		death_comment   = str()
	else:
		death_date_cert = str(0)
		death_comment   = death_date[5:]
		death_date      = death_date[0:4]

	born_place  = str(row['Lieu naiss.'])
	born_place  = born_place.replace("'", "\\\'")
	death_place = str(row['Lieu mort'])
	death_place = death_place.replace("'", "\\\'")
		
	printout += '(\'' + str(row['Numéro']) + '\', \'A\',\'' + name + '\', \'' +\
				 firstname + '\',' + born_date + ',' + born_date_cert + ',\''+\
				 born_comment + '\',' + death_date + ',' + death_date_cert +\
				 ',\'' + death_comment + '\', \'' + born_place + '\', \'' +\
				 death_place + '\'),\n'



# COULD BE A SOLUTION FOR SPECIAL CHARACTER such as ' \' '
# for row in dataA1.itertuples():
# 	print(row)

# print(printout)
with open("data_for_sql/savants.sql", mode = "w", encoding = "utf8") as f: #mode "a" for the followings
	f.write(printout[:-2]) #-2 to remove the last ",\n"






