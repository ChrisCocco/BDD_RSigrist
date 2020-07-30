# -*- coding: utf-8 -*-

import pandas as pd
import re

dfsA1_base = pd.read_html('DATA/LiensA1.htm', header = 0)

dataA1_base = dfsA1_base[0]



log = str()

printout   = str()

printout = "INSERT INTO Liens (id_savant, type_savant, id_savant_1, \
	type_savant_1, id_type_lien, type_lien_comment, lien_intensite)\n"


#################
#### A bases ####
#################

for index, row in dataA1_base.iterrows():

	id_savant = str(row['Numéro']).zfill(4)

	#need loop on columns...!!! columns_M = ['Maître 1']
	if pd.notna(row['Maître 1']):
		savant_1 = str(row['Maître 1'])
		elements = re.findall('\(.*?\)', savant_1)

		lien_comment = "NULL"

		if elements:
			
			if len(elements) == 1:
				id_elements = re.search('no (\d{4})(\-B)?', savant_1)
				# master with only an intensity
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
						log += savant_1 + "\n"

				elif not re.match('\(\+.*\)',elements[0]):

					if id_elements:
						id_savant_1 = id_elements.group(1)

						if elements[0] == "(patron)":
							relation_type = str(3)
						elif elements[0] == "(influence)":
							relation_type = str(5)
						elif elements[0] == "(directeur)":
							lien_comment = "succession népotique"
						else:
							log += savant_1 + "\n"
						lien_intensite = str(1)
						# if there is "-B" in the name
						if id_elements.group(2):
							type_savant_1 = "B"
						else:
							type_savant_1 = "A" 
					else:
						log += savant_1 + "\n"

				else:

					if id_elements:
						id_savant_1 = id_elements.group(1)
						
						lien_intensite = str(1)
						# if there is "-B" in the name
						if id_elements.group(2):
							type_savant_1 = "B"
						else:
							type_savant_1 = "A"

						relation_type_a = str(1)

						if (elements[0] == "(+patron)" or 
						    elements[0] == "(+ patron)"):
							relation_type_b = str(3)
						elif (elements[0] == "(+influence)" or
						      elements[0] == "(+ influence)"):
							relation_type_b = str(5)
						elif elements[0] == "(+SN)":
							lien_comment = "succession népotique"
							printrow  = '(\'' + id_savant +\
							'\', \'A\',\'' +\
							id_savant_1 + '\', \'' +\
							type_savant_1 +\
							'\', \'' + relation_type_a +\
							'\', \'' + lien_comment +\
							'\', \'' + lien_intensite +\
							'),\n'

							printrow  = printrow.replace("'NULL'", "NULL")

							printout += printrow
							continue

						elif elements[0] == "(+directeur)":
							lien_comment = "directeur de thèse"
							printrow  = '(\'' + id_savant +\
							'\', \'A\',\'' +\
							id_savant_1 + '\', \'' +\
							type_savant_1 +\
							'\', \'' + relation_type_a +\
							'\', \'' + lien_comment +\
							'\', \'' + lien_intensite +\
							'),\n'

							printrow  = printrow.replace("'NULL'", "NULL")

							printout += printrow
							continue
						else:
							log += savant_1 + "\n"

						printrow  = '(\'' + id_savant +\
							'\', \'A\',\'' +\
							id_savant_1 + '\', \'' +\
							type_savant_1 +\
							'\', \'' + relation_type_a +\
							'\', \'' + lien_comment +\
							'\', \'' + lien_intensite +\
							'),\n'

						printrow  = printrow.replace("'NULL'", "NULL")

						printout += printrow

						printrow  = '(\'' + id_savant +\
							'\', \'A\',\'' +\
							id_savant_1 + '\', \'' +\
							type_savant_1 +\
							'\', \'' + relation_type_b +\
							'\', \'' + lien_comment +\
							'\', \'' + lien_intensite +\
							'),\n'

						printrow  = printrow.replace("'NULL'", "NULL")

						printout += printrow

						continue
						
					else:
						log += savant_1 + "\n"
			else:
				print(savant_1)

				id_elements = re.search(
					'no (\d{4})(\-B)? ?(\(\dX\))? ?'
					'(\(\+?.*?\)) ?(\(\dX\))? ?'
					'((\(\+?.*?\)) ?(\(\dX\))?)?', 
					savant_1)

				if id_elements:
					id_savant_1 = id_elements.group(1)
					# if there is "-B" in the name
					if id_elements.group(2):
						type_savant_1 = "B"
					else:
						type_savant_1 = "A"
					
					if (not id_elements.group(6) and
					    not re.match('\(\+.*\)',id_elements.group(4))):
						if id_elements.group(4) == "(patron)":
							relation_type = str(3)
						elif id_elements.group(4) == "(influence)":
							relation_type = str(5)
						elif id_elements.group(4) == "(directeur)":
							lien_comment = "directeur de thèse"
							relation_type = str(1)
						else:
							log += savant_1 + "\n"

						if id_elements.group(5):
							lien_intensite = re.search('\d', id_elements.group(5)).group(0)
						else:
							lien_intensite = str(1)

					elif (not id_elements.group(6) and
					    re.match('\(\+.*\)',id_elements.group(4))):
					    
						# first link
						relation_type = str(1)
						if id_elements.group(3):
							lien_intensite = re.search('\d', id_elements.group(3)).group(0)
						else:
							lien_intensite = str(1)
							
						#second link
						if (id_elements.group(4) == "(+patron)" or 
						    id_elements.group(4) == "(+ patron)"):
							relation_type_a = str(3)
						elif (id_elements.group(4) == "(+influence)" or
						      id_elements.group(4) == "(+ influence)"):
							relation_type_a = str(5)
						elif id_elements.group(4) == "(+SN)":
							lien_comment = "succession népotique"
							printrow  = '(\'' + id_savant +\
							'\', \'A\',\'' +\
							id_savant_1 + '\', \'' +\
							type_savant_1 +\
							'\', \'' + relation_type +\
							'\', \'' + lien_comment +\
							'\', \'' + lien_intensite +\
							'),\n'

							printrow  = printrow.replace("'NULL'", "NULL")

							printout += printrow
							continue
						elif id_elements.group(4) == "(+directeur)":
							lien_comment = "directeur de thèse"
							printrow  = '(\'' + id_savant +\
							'\', \'A\',\'' +\
							id_savant_1 + '\', \'' +\
							type_savant_1 +\
							'\', \'' + relation_type +\
							'\', \'' + lien_comment +\
							'\', \'' + lien_intensite +\
							'),\n'

							printrow  = printrow.replace("'NULL'", "NULL")

							printout += printrow
							continue
						else:
							log += savant_1 + "\n"
							
						if id_elements.group(5):
							lien_intensite_a = re.search('\d', id_elements.group(5)).group(0)
						else:
							lien_intensite_a = str(1)
						
						lien_comment_a = "NULL"
						
						# print second link	
						printrow  = '(\'' + id_savant +\
						'\', \'A\',\'' +\
						id_savant_1 + '\', \'' +\
						type_savant_1 +\
						'\', \'' + relation_type_a +\
						'\', \'' + lien_comment_a +\
						'\', \'' + lien_intensite_a +\
						'),\n'

						printrow  = printrow.replace("'NULL'", "NULL")

						printout += printrow
						
					elif (id_elements.group(6) and
						  not re.match('\(\+.*\)',id_elements.group(4))):
						print(savant_1)
					    #first link
						if id_elements.group(4) == "(patron)":
							relation_type = str(3)
						elif id_elements.group(4) == "(influence)":
							relation_type = str(5)
						elif id_elements.group(4) == "(directeur)":
							relation_type = str(1)
							lien_comment = "succession népotique"
						else:
							log += savant_1 + "\n"
							
						if id_elements.group(5):
							lien_intensite = re.search('\d', id_elements.group(5)).group(0)
						else:
							lien_intensite = str(1)
						
					    #second link
						if (id_elements.group(7) == "(+patron)" or 
						    id_elements.group(7) == "(+ patron)"):
							relation_type_a = str(3)
						elif (id_elements.group(7) == "(+influence)" or
						      id_elements.group(7) == "(+ influence)"):
							relation_type_a = str(5)
						elif id_elements.group(7) == "(+SN)":
							lien_comment = "succession népotique"
							printrow  = '(\'' + id_savant +\
							'\', \'A\',\'' +\
							id_savant_1 + '\', \'' +\
							type_savant_1 +\
							'\', \'' + relation_type +\
							'\', \'' + lien_comment +\
							'\', \'' + lien_intensite +\
							'),\n'

							printrow  = printrow.replace("'NULL'", "NULL")

							printout += printrow
							continue
						elif id_elements.group(7) == "(+directeur)":
							lien_comment = "directeur de thèse"
							printrow  = '(\'' + id_savant +\
							'\', \'A\',\'' +\
							id_savant_1 + '\', \'' +\
							type_savant_1 +\
							'\', \'' + relation_type +\
							'\', \'' + lien_comment +\
							'\', \'' + lien_intensite +\
							'),\n'

							printrow  = printrow.replace("'NULL'", "NULL")

							printout += printrow
							continue
						else:
							log += savant_1 + "\n"
							
						if id_elements.group(8):
							lien_intensite_a = re.search('\d', id_elements.group(8)).group(0)
						else:
							lien_intensite_a = str(1)
						
						lien_comment_a = "NULL"
						
						# print second link	
						printrow  = '(\'' + id_savant +\
						'\', \'A\',\'' +\
						id_savant_1 + '\', \'' +\
						type_savant_1 +\
						'\', \'' + relation_type_a +\
						'\', \'' + lien_comment_a +\
						'\', \'' + lien_intensite_a +\
						'),\n'

						printrow  = printrow.replace("'NULL'", "NULL")

						printout += printrow
						
					elif (id_elements.group(6) and
					    re.match('\(\+.*\)',id_elements.group(4))):
					    print("To be continued...")
					    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
					    #first link
					    #second link
					    #third link
					    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
					else:
						log += savant_1 + "\n"
				else:
					log += savant_1 + "\n"
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
				log += savant_1 + "\n"

		# check if savant_1 is in the savants of the current database

		printrow  = '(\'' + id_savant + '\', \'A\',\'' + id_savant_1 + '\', \'' + type_savant_1 + '\', \'' + relation_type + '\', \'' + lien_comment + '\', \'' + lien_intensite + '),\n'

		printrow  = printrow.replace("'NULL'", "NULL")

		printout += printrow

	

# what to do with "+A"

print(printout)
#with open("data_for_sql/liens.sql", mode = "w", encoding = "utf8") as f: #mode "a" for the followings
#	f.write(printout[:-2]) #-2 to remove the last ",\n"

#print(log)
#do a log file