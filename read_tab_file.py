# -*- coding: utf-8 -*-

import pandas as pd
import re


dfsA1  = pd.read_html('DATA/BaseA1.htm', header = 0)
dfsA2  = pd.read_html('DATA/BaseA2.htm', header = 0)

dfsB1  = pd.read_html('DATA/BaseB1.htm', header = 0)
dfsB2  = pd.read_html('DATA/BaseB2.htm', header = 0, 
	converters= {'Ac. Bol.': str}) # To avoid transformation of dates into floats
 
dataA1 = dfsA1[0]
dataA2 = dfsA2[0]

dataB1 = dfsB1[0]
dataB2 = dfsB2[0]

dataA  = pd.concat([dataA1, dataA2], sort = False, ignore_index = True)
# Two columns do not have the same name in both databases: 
# "Corrections" for A1 and "Corr. BMS" for A2 (no prob, not used)

#dataA = dataA1


dataB2.rename(columns = {"Pays":"Pays 1"}, inplace = True)
# Eleven columns still not have the same name (Pays corrected), maybe to 
# correct later depending on the useful columns
dataB  = pd.concat([dataB1, dataB2], sort = False, ignore_index = True)


# print(dataA1.loc[:,"Numéro"])
# print(dataA1["Numéro"]) #is equivalent to the line above

# #print(dataA1["Numéro"] == 1) # => TRUE or FALSE
# dataA1.loc[lambda df: df.Numéro == 1, :]

# To remove empty row in dataB
dataB    = dataB[dataB.Nom != "(vide)"]

printout   = str()

printout = "INSERT INTO Savants (id_savant, type_savant, nom, prenom, " +\
	"naissance_date, naissance_date_certitude, naissance_date_comment," +\
	"mort_date, mort_date_certitude, mort_date_comment, naissance_lieu, "+\
	"mort_lieu, discipl_1, discipl_2, discipl_3, discipl_4, discipl_5, "+\
	"nbre_acad, gasc, id_type_eminence, pays_principal, "+\
	"pays_2, pays_3, empire, lieu_1, lieu_2, lieu_3, lieu_4, a_paris, "+\
	"a_londres, a_berlin, a_petersb, a_stockh, a_bologne, acad_7, acad_8, "+\
	"acad_9, pos_acad_1, pos_acad_2, prix_1, prix_2, dsb, macmill) VALUES\n"


#################
#### A bases ####
#################

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
		born_comment   = born_date[5:] #Could be improved
		born_date      = born_date[0:4] 

	if isinstance(row['Mort'], float):
		death_date = str(int(row['Mort']))
	else:
		death_date = str(row['Mort'])

	if re.match('^[0-9]{4}$', death_date):
		death_date_cert = str(1)
		death_comment   = 'NULL'
	else:
		death_date_cert = str(0)
		if death_date[4:5] == ' ':
			death_comment   = death_date[5:]
		else:
			death_comment   = death_date[4:]
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

	if pd.notna(row['Discipl. 2']):
		discipl_2   = str(row['Discipl. 2'])
		discipl_2   = discipl_2.replace("'", "\\\'")
	else:
		discipl_2	= 'NULL'

	if pd.notna(row['Discipl. 3']):
		discipl_3   = str(row['Discipl. 3'])
		discipl_3   = discipl_3.replace("'", "\\\'")
	else:
		discipl_3	= 'NULL'

	if pd.notna(row['Discipl. 4']):
		discipl_4   = str(row['Discipl. 4'])
		discipl_4   = discipl_4.replace("'", "\\\'")
	else:
		discipl_4	= 'NULL'

	if pd.notna(row['Discipl. 5']):
		discipl_5   = str(row['Discipl. 5'])
		discipl_5   = discipl_5.replace("'", "\\\'")
	else:
		discipl_5	= 'NULL'
	

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

	if pd.notna(row['Pays 1']):
		country_1 = str(row['Pays 1'])
	else:
		country_1 = 'NULL'

	if pd.notna(row['Pays 2']):
		country_2 = str(row['Pays 2'])
	else:
		country_2 = 'NULL'

	if pd.notna(row['Pays 3']):
		country_3 = str(row['Pays 3'])
	else:
		country_3 = 'NULL'

	if pd.notna(row['Empire']):
		empire    = str(row['Empire'])
	else:
		empire    = 'NULL'


	if pd.notna(row['Lieu 1']):
		place_1   = str(row['Lieu 1'])
		place_1   = place_1.replace("'", "\\\'")
	else:
		place_1   = 'NULL'

	if pd.notna(row['Lieu 2']):
		place_2   = str(row['Lieu 2'])
		place_2   = place_2.replace("'", "\\\'")
	else:
		place_2   = 'NULL'

	if pd.notna(row['Lieu 3']):
		place_3   = str(row['Lieu 3'])
		place_3   = place_3.replace("'", "\\\'")
	else:
		place_3   = 'NULL'

	if pd.notna(row['Lieu 4']):
		place_4   = str(row['Lieu 4'])
		place_4   = place_4.replace("'", "\\\'")
	else:
		place_4   = 'NULL'

        
	if pd.notna(row['A. Paris']):
		a_paris   = str(row['A. Paris'])
		a_paris   = a_paris.replace("'", "\\\'")
	else:
		a_paris   = 'NULL'		

	if pd.notna(row['A. Londres']):
		a_london  = str(row['A. Londres'])
		a_london  = a_london.replace("'", "\\\'")
	else:
		a_london  = 'NULL'

	if pd.notna(row['A. Berlin']):
		a_berlin  = str(row['A. Berlin'])
		a_berlin  = a_berlin.replace("'", "\\\'")
	else:
		a_berlin  = 'NULL'

	if pd.notna(row['A. Pétersb.']):
		a_petersb = str(row['A. Pétersb.'])
		a_petersb = a_petersb.replace("'", "\\\'")
	else:
		a_petersb = 'NULL'

	if pd.notna(row['A. Stockh.']):
		a_stockh  = str(row['A. Stockh.'])
		a_stockh  = a_stockh.replace("'", "\\\'")
	else:
		a_stockh  = 'NULL'

	if pd.notna(row['A. Bologne']):
		a_bologna = str(row['A. Bologne'])
		a_bologna = a_bologna.replace("'", "\\\'")
	else:
		a_bologna = 'NULL'

	if pd.notna(row['Acad. 7']):
		acad_7    = str(row['Acad. 7'])
		acad_7    = acad_7.replace("'", "\\\'")
	else:
		acad_7    = 'NULL'

	if pd.notna(row['Acad. 8']):
		acad_8    = str(row['Acad. 8'])
		acad_8    = acad_8.replace("'", "\\\'")
	else:
		acad_8    = 'NULL'

	if pd.notna(row['Acad. 9']):
		acad_9    = str(row['Acad. 9'])
		acad_9    = acad_9.replace("'", "\\\'")
	else:
		acad_9    = 'NULL'


	if pd.notna(row['Pos. acad. 1']):
		ac_pos_1  = str(row['Pos. acad. 1'])
		ac_pos_1  = ac_pos_1.replace("'", "\\\'")
	else:
		ac_pos_1  = 'NULL'

	if pd.notna(row['Pos. acad. 2']):
		ac_pos_2  = str(row['Pos. acad. 2'])
		ac_pos_2  = ac_pos_2.replace("'", "\\\'")
	else:
		ac_pos_2  = 'NULL'


	if pd.notna(row['Prix 1']):
		price_1   = str(row['Prix 1'])
		price_1   = price_1.replace("'", "\\\'")
	else:
		price_1   = 'NULL'

	if pd.notna(row['Prix 2']):
		price_2   = str(row['Prix 2'])
		price_2   = price_2.replace("'", "\\\'")
	else:
		price_2   = 'NULL'


	if pd.notna(row['DSB et Macmill.']):
		dsb_macmil      = str(row['DSB et Macmill.'])
		dsb_macmil_list = dsb_macmil.replace("//","/").replace(" ","").split("/")
		dsb             = dsb_macmil_list[0]
		macmil          = dsb_macmil_list[1]

		if dsb == "oui":
			dsb_bin = 1
		elif dsb == "non":
			dsb_bin = 0
		else:
			print("Prob about DSB with ", id_savant, dsb)

		if macmil == "oui":
			macmil_bin = 1
		elif macmil == "non":
			macmil_bin = 0
		else:
			print("Prob about Macmillan with ", id_savant, macmil)

	else:
		dsb_bin = "NULL"
		macmil_bin = "NULL"

		
	printrow  = '(\'' + id_savant + '\', \'A\',\'' + name + '\', \'' +\
				 firstname + '\',' + born_date + ',' + born_date_cert + ',\''+\
				 born_comment + '\',' + death_date + ',' + death_date_cert +\
				 ',\'' + death_comment + '\', \'' + born_place + '\', \'' +\
				 death_place + '\', \'' + discipl_1 + '\', \'' + discipl_2 + \
				 '\', \'' + discipl_3 + '\', \'' + discipl_4 + '\', \'' + \
				 discipl_5 + '\',' +\
				 nbre_acad + ',' + str(gasc_bin) + ',' + str(type_eminence) +\
				 ', \'' + country_1 + '\', \'' + country_2 + '\', \'' +\
				 country_3 + '\', \'' + empire + '\', \'' + place_1 + \
				 '\', \'' + place_2 + '\', \'' + place_3 + '\', \'' + \
				 place_4 + '\', \'' + a_paris + '\', \'' + a_london + \
				 '\', \'' + a_berlin + '\', \'' + a_petersb + '\', \'' + \
				 a_stockh + '\', \'' + a_bologna + '\', \'' + acad_7 + \
				 '\', \'' + acad_8 + '\', \'' + acad_9 + '\', \'' + ac_pos_1 +\
				 '\', \'' + ac_pos_2 + '\', \'' + price_1 + '\', \'' + \
				 price_2 + '\',' + str(dsb_bin) + ',' + str(macmil_bin) + '),\n'

	printrow  = printrow.replace("'NULL'", "NULL")

	printout += printrow


#################
#### B bases ####
#################


for index, row in dataB.iterrows():

	id_savant = str(row['Numéro'])[0:4] # Take numbers, not "-B"

	name = str(row['Nom'])
	if name == "nan" or name == "vide":
		continue
	name = name.replace("'", "\\\'")

	if pd.notna(row['Prénom']):
		firstname = str(row['Prénom'])
		firstname = firstname.replace("'", "\\\'")
	else:
		firstname = "NULL"

	born_date = str(row['Né'])
	if re.match('^[0-9]{4}$', born_date):
		born_date_cert = str(1)
		born_comment   = 'NULL'
	else:
		born_date_cert = str(0)
		if born_date[4:5] == ' ':
			born_comment   = born_date[5:]
		else:
			born_comment   = born_date[4:]
		born_comment   = born_comment.replace("'", "\\\'")
		born_date      = born_date[0:4] 

	if pd.notna(row['Mort']) and str(row['Mort']) != "XXX":
		death_date = str(row['Mort'])
		if re.match('^[0-9]{4}$', death_date):
			death_date_cert = str(1)
			death_comment   = 'NULL'
		elif re.match('^[0-9]{4}', death_date):
			death_date_cert = str(0)
			if death_date[4:5] == ' ':
				death_comment   = death_date[5:]
			else:
				death_comment   = death_date[4:]
			death_comment   = death_comment.replace("'", "\\\'")
			death_date      = death_date[0:4]
		else:
			death = re.search('(.+)([0-9]{4})', death_date)
			death_date = death.group((2))
			death_date_cert = str(0)
			death_comment = death.group(1).replace("'", "\\\'")
	else:
		death_date = 'NULL'
		death_date_cert = str(0)
		if int(id_savant) > 5000:
			death_comment = "ap." + born_date
		else:
			death_comment   = 'NULL'


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

	if pd.notna(row['Discipl. 1']):
		discipl_1   = str(row['Discipl. 1'])
		discipl_1   = discipl_1.replace("'", "\\\'")
	else:
		discipl_1   = "xxx"
		print("Prob about 1st discipline with ", id_savant, "B", 
			row['Discipl. 1'], "xxx introduced")
	
	if pd.notna(row['Discipl. 2']):
		discipl_2   = str(row['Discipl. 2'])
		discipl_2   = discipl_2.replace("'", "\\\'")
	else:
		discipl_2	= 'NULL'

	if pd.notna(row['Discipl. 3']):
		discipl_3   = str(row['Discipl. 3'])
		discipl_3   = discipl_3.replace("'", "\\\'")
	else:
		discipl_3	= 'NULL'

	if pd.notna(row['Discipl. 4']):
		discipl_4   = str(row['Discipl. 4'])
		discipl_4   = discipl_4.replace("'", "\\\'")
	else:
		discipl_4	= 'NULL'

	discipl_5	= 'NULL'

	try:
		nbre_acad   = str(int(row['Nbre acad.']))
	except:
		print("Prob about nbre_acad with ", id_savant, "B", row['Nbre acad.'], 
			"NULL introduced")
		nbre_acad   = 'NULL'

	if str(row['Source 1']) == "Gasc.":
		gasc_bin = 1
	else:
		gasc_bin = 0

	type_eminence = 4

	if pd.notna(row['Pays 1']):
		country_1 = str(row['Pays 1'])
	else:
		country_1 = 'NULL'

	if pd.notna(row['Pays 2']):
		country_2 = str(row['Pays 2'])
	else:
		country_2 = 'NULL'

	country_3 = 'NULL'

	if pd.notna(row['Empire']):
		empire    = str(row['Empire'])
	else:
		empire    = 'NULL'

	places  = []
	place_1 = place_2 = place_3 = place_4 = 'NULL'
	
	if pd.notna(row['Ville 1']):
		place_1_temp = str(row['Ville 1'])
		places.extend(
			re.split(r'& (?=[A-Z])|; (?=[A-Z])|@ (?=[A-Z])', place_1_temp)
			)
	if pd.notna(row['Ville 2']):
		place_2_temp = str(row['Ville 2'])
		places.extend(
			re.split(r'& (?=[A-Z])|; (?=[A-Z])|@ (?=[A-Z])', place_2_temp)
			)
	if pd.notna(row['Ville 3']):
		place_3_temp = str(row['Ville 3'])
		places.extend(
			re.split(r'& (?=[A-Z])|; (?=[A-Z])|@ (?=[A-Z])', place_3_temp)
			)

	if len(places) == 0:
		place_1 = place_2 = place_3 = place_4 = 'NULL'
	else:
		place_1 = places[0]
		place_1   = place_1.replace("'", "\\\'")
		if len(places) > 1:
			place_2 = places[1]
			place_2   = place_2.replace("'", "\\\'")
			if len(places) > 2:
				place_3 = places[2]
				place_3   = place_3.replace("'", "\\\'")
				if len(places) > 3:
					place_4 = places[3]
					place_4   = place_4.replace("'", "\\\'")
					if len(places) > 4:
						print(id_savant, "B: There are too many places")

	#NOT SOLVED FOR PLACES: Remove "----", must be replaced by "NULL" or NOT?

	if pd.notna(row['Ac. Paris']):
		a_paris   = str(row['Ac. Paris'])
		a_paris   = a_paris.replace("'", "\\\'")
	else:
		a_paris   = 'NULL'

	if pd.notna(row['Ac. Londres']):
		a_london  = str(row['Ac. Londres'])
		a_london  = a_london.replace("'", "\\\'")
	else:
		a_london  = 'NULL'

	if pd.notna(row['Ac. Berlin']):
		a_berlin  = str(row['Ac. Berlin'])
		a_berlin  = a_berlin.replace("'", "\\\'")
	else:
		a_berlin  = 'NULL'

	if pd.notna(row['Ac. SP']):
		a_petersb = str(row['Ac. SP'])
		a_petersb = a_petersb.replace("'", "\\\'")
	else:
		a_petersb  = 'NULL'

	if pd.notna(row['Ac. Stock.']):
		a_stockh  = str(row['Ac. Stock.'])
		a_stockh = a_stockh.replace("'", "\\\'")
	else:
		a_stockh  = 'NULL'

	if pd.notna(row['Ac. Bol.']):
		a_bologna = str(row['Ac. Bol.'])
		a_bologna = a_bologna.replace("'", "\\\'")
	else:
		a_bologna = 'NULL'

	acad_7 = 'NULL'

	acad_8 = 'NULL'

	acad_9 = 'NULL'


	if pd.notna(row['Titre acad.']):
		ac_pos_1  = str(row['Titre acad.'])
		ac_pos_1  = ac_pos_1.replace("'", "\\\'")
	else:
		ac_pos_1    = 'NULL'

	ac_pos_2 = 'NULL'


	price_1  = 'NULL'

	price_2  = 'NULL'

	dsb      = 'NULL'
	macmil   = 'NULL'
		
	printrow  = '(\'' + id_savant + '\', \'B\',\'' + name + '\', \'' +\
				 firstname + '\',' + born_date + ',' + born_date_cert + ',\''+\
				 born_comment + '\',' + death_date + ',' + death_date_cert +\
				 ',\'' + death_comment + '\', \'' + born_place + '\', \'' +\
				 death_place + '\', \'' + discipl_1 + '\', \'' + discipl_2 + \
				 '\', \'' + discipl_3 + '\', \'' + discipl_4 + '\', \'' + \
				 discipl_5 + '\',' +\
				 nbre_acad + ',' + str(gasc_bin) + ',' + str(type_eminence) +\
				 ', \'' + country_1 + '\', \'' + country_2 + '\', \'' +\
				 country_3 + '\', \'' + empire + '\', \'' + place_1 + \
				 '\', \'' + place_2 + '\', \'' + place_3 + '\', \'' + \
				 place_4 + '\', \'' + a_paris + '\', \'' + a_london + \
				 '\', \'' + a_berlin + '\', \'' + a_petersb + '\', \'' +\
				 a_stockh + '\', \'' + a_bologna + '\', \'' + acad_7 + \
				 '\', \'' + acad_8 + '\', \'' + acad_9 + '\', \'' + ac_pos_1 +\
				 '\', \'' + ac_pos_2 + '\', \'' + price_1 + '\', \'' + \
				 price_2 + '\', \'' + dsb + '\', \'' + macmil + '\'),\n'

	printrow  = printrow.replace("'NULL'", "NULL")

	printrow  = printrow.replace(u'\x92', u"\\\'")

	printout += printrow


# print(printout)
with open("data_for_sql/savants.sql", mode = "w", encoding = "utf8") as f: #mode "a" for the followings
	f.write(printout[:-2]) #-2 to remove the last ",\n"






