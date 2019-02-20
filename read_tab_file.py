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
	"naissance_date, naissance_date_certitude) VALUES\n"

for index, row in dataA1.iterrows():
	name = str(row['Nom'])
	name = name.replace("'", "\\\'")
	firstname = str(row['Prénom'])
	firstname = firstname.replace("'", "\\\'")
	born_date = str(row['Né'])
	if re.match('^[0-9]{4}$', born_date):
		born_date_cert = str(1)
	else:
		born_date_cert = str(0)
		born_date = born_date[0:4]
		born_comment = born_date[4:]
		
	printout += '(\'' + str(row['Numéro']) + '\', \'A\',\'' + name + '\', \'' +\
				 firstname + '\',' + born_date + ',' + born_date_cert +\
				 '),\n'
    # !!!!!!!
    # need to check empty rows (no name and firstname, birthdate, and so on) !!!!!!!!!!!!!!
    # !!!!!!!


# COULD BE A SOLUTION FOR SPECIAL CHARACTER such as ' \' '
# for row in dataA1.itertuples():
# 	print(row)

# print(printout)
with open("data_for_sql/savants.sql", mode = "w", encoding = "utf8") as f: #mode "a" for the followings
	f.write(printout[:-2]) #-2 to remove the last ",\n"






