# -*- coding: utf-8 -*-

import pandas as pd
import re

dfsA1_base = pd.read_html('DATA/LiensA1.htm', header = 0)

dataA1_base = dfsA1_base[0]




printout   = str()

printout = "INSERT INTO Liens (id_savant, type_savant, id_savant_1, type_savant_1, id_type_lien, lien_intensite)\n"


#################
#### A bases ####
#################

for index, row in dataA1_base.iterrows():

	id_savant = str(row['Numéro']).zfill(4)

	#need loop on columns...!!! columns_M = ['Maître 1']
	if pd.notna(row['Maître 1']):
		savant_1 = str(row['Maître 1'])
		elements = re.findall('\(.*?\)', savant_1)
		if elements:
			# only master with an intensity
			if len(elements) == 1:
				id_elements = re.search('no (\d{4})(\-B)?', savant_1)

				if re.match('\(\dX\)',elements[0]):
					
					if id_elements:
						id_savant_1 = id_elements.group(1)
						relation_type = str(1)
						lien_intensite = re.search('\d', elements[0]).group(0)
						# if there is "-B" in the name
						if id_elements.group(2):
							type_savant_1 = "B"
						else:
							type_savant_1 = "A" 
					else:
						print(savant_1)

				elif not re.match('\(\+.*\)',elements[0]):

					if id_elements:
						id_savant_1 = id_elements.group(1)

						if elements[0] == "(patron)":
							relation_type = str(3)
						elif elements[0] == "(influence)":
							relation_type = str(5)
						else:
							print(savant_1)
						lien_intensite = str(1)
						# if there is "-B" in the name
						if id_elements.group(2):
							type_savant_1 = "B"
						else:
							type_savant_1 = "A" 
					else:
						print(savant_1)

				else:

					if id_elements:
						id_savant_1 = id_elements.group(1)
						relation_type_a = str(1)
						if elements[0] == "(+patron)":
							relation_type_b = str(3)
						elif elements[0] == "(+influence)":
							relation_type_b = str(5)
						else:
							print(savant_1)
						lien_intensite = str(1)
						# if there is "-B" in the name
						if id_elements.group(2):
							type_savant_1 = "B"
						else:
							type_savant_1 = "A"

						printrow  = '(\'' + id_savant +\
							'\', \'A\',\'' +\
							id_savant_1 + '\', \'' +\
							type_savant_1 +\
							'\', \'' + relation_type_a +\
							'\', \'' + lien_intensite +\
							'),\n'

						printrow  = printrow.replace("'NULL'", "NULL")

						printout += printrow

						printrow  = '(\'' + id_savant +\
							'\', \'A\',\'' +\
							id_savant_1 + '\', \'' +\
							type_savant_1 +\
							'\', \'' + relation_type_b +\
							'\', \'' + lien_intensite +\
							'),\n'

						printrow  = printrow.replace("'NULL'", "NULL")

						printout += printrow

						continue
						
					else:
						print(savant_1)
			else:
				# print("to be continued...")
				id_savant_1 = "to be continued"
				type_savant_1 = "to be continued"
				relation_type = "to be continued"
				lien_intensite = "to be continued"
		else:
			id_elements = re.search('no (\d{4})(\-B)?', savant_1)
			if id_elements:
				id_savant_1 = id_elements.group(1)
				relation_type = str(1)
				lien_intensite = str(1)
				# if there is "-B" in the name
				if id_elements.group(2):
					type_savant_1 = "B"
				else:
					type_savant_1 = "A" 
			else:
				print(savant_1)

		# check if savant_1 is in the savants of the current database

		printrow  = '(\'' + id_savant + '\', \'A\',\'' + id_savant_1 + '\', \'' + type_savant_1 + '\', \'' + relation_type + '\', \'' + lien_intensite + '),\n'

		printrow  = printrow.replace("'NULL'", "NULL")

		printout += printrow

	

print(printout)
#with open("data_for_sql/liens.sql", mode = "w", encoding = "utf8") as f: #mode "a" for the followings
#	f.write(printout[:-2]) #-2 to remove the last ",\n"
