# -*- coding: utf-8 -*-

import pandas as pd
import re
import functools # to use "reduce"

def string_print(id_sav, type_sav, id_sav_2, type_sav_2, weight):
	return('(' + id_sav + ',\'' + type_sav + '\',' + id_sav_2 +\
		', \'' + type_sav_2 + '\', \'' + weight + '\'),\n')

dfsA  = pd.read_html('DATA/CorresA.htm', header = 0)
dfsB = pd.read_html('DATA/CorresB.htm', header = 0)

dataA = dfsA[0]
dataB = dfsB[0]

printout   = str()

printout = "INSERT INTO Correspondances (id_savant, type_savant, id_savant_1, " +\
	"type_savant_1, corresp_intensite) VALUES\n"

# From CorresA

colnames_corr    = ["Corr. " + str(i+1) for i in range(38)]
colnames_corr_AB = ["Corr. B" + str(i+1) for i in range(32)]

for index, row in dataA.iterrows():
#	print(index)
	if pd.notna(row['Corr. 1']) or pd.notna(row['Corr. B1']):
		id_sav   = str(row['Numéro']).zfill(4)
		type_sav = "A"

		for corr in colnames_corr:
			if pd.notna(row[corr]) and row[corr] != "-----":
				parts = re.search(
					'(.+)(?:,|.) no ([0-9]{4}(\-B)?) \(([0-9])X', 
					row[corr])
				if parts:
					id_sav_2   = parts.group(2) 
					weight     = parts.group(4)
					type_sav_2 = "A"

				else:
					print(index, corr)

				if int(id_sav_2) == 2053 or int(id_sav_2) == 1823 or int(id_sav_2) == 2023 or int(id_sav_2) == 1939:
					continue
				
				printrow  = string_print(id_sav, type_sav, 
					id_sav_2, type_sav_2, weight)

				printout += printrow
				
		for corr in colnames_corr_AB:
			if pd.notna(row[corr]) and row[corr] != "-----":
				parts = re.search(
					'(.+)(?:,|.) no ([0-9]{4})(\-B)? \(([0-9])X', 
					row[corr]) 
				if parts:
					id_sav_2   = parts.group(2) 
					weight     = parts.group(4)
					type_sav_2 = "B"

				else:
					print(index, corr)

				if int(id_sav_2) == 4796:
					continue

				printrow  = string_print(id_sav, type_sav, 
					id_sav_2, type_sav_2, weight)

				printout += printrow

		if pd.notna(row['Autres corr. A']):
			for scientist in row['Autres corr. A'].split(";"):
				parts = re.search(
					'(.+), no ([0-9]{4}(\-B)?) \(([0-9])X', 
					scientist)
				if parts:
					id_sav_2   = parts.group(2)
					weight     = parts.group(4)
					type_sav_2 = "A"
				else:
					print(index,row['Autres corr. A'])

				printrow  = string_print(id_sav, type_sav, 
					id_sav_2, type_sav_2, weight)

				printout += printrow

		if pd.notna(row['Autres corr. B']):
			for scientist in row['Autres corr. B'].split(";"):
				parts = re.search(
					'(.+), no ([0-9]{4})(\-B)? \(([0-9])X', 
					scientist)
				if parts:
					id_sav_2   = parts.group(2)
					weight     = parts.group(4)
					type_sav_2 = "B"
				else:
					print(index,row['Autres corr. B'])

				printrow  = string_print(id_sav, type_sav, 
					id_sav_2, type_sav_2, weight)

				printout += printrow



# From CorresB

colnames_corrB    = ["Corr. " + str(i+1) for i in range(28)]
colnames_corrB_BA = ["Corr. B" + str(i+1) for i in range(28)]

for index, row in dataB.iterrows():
	if pd.notna(row['Corr. 1']) or pd.notna(row['Corr. B1']):
		id_sav   = str(row['Numéro'])[0:4]
		type_sav = "B"
		for corr in colnames_corrB:
			if pd.notna(row[corr]) and row[corr] != "-----":
				parts = re.search(
					'(.+), no ([0-9]{4}(\-B)?) \(([0-9])X', 
					row[corr]) 

				if parts:
					id_sav_2   = parts.group(2) 
					weight     = parts.group(4)
					type_sav_2 = "A"
				else:
					print(index, corr)

				printrow  = string_print(id_sav, type_sav, 
					id_sav_2, type_sav_2, weight)

				printout += printrow


		for corr in colnames_corrB_BA:
			if pd.notna(row[corr]) and row[corr] != "-----":
				parts = re.search(
					'(.+), no ([0-9]{4})(\-B)? \(([0-9])X', 
					row[corr]) 

				if parts:
					id_sav_2   = parts.group(2) 
					weight     = parts.group(4)
					type_sav_2 = "B"
				else:
					print(index, corr)

				printrow  = string_print(id_sav, type_sav, 
					id_sav_2, type_sav_2, weight)

				printout += printrow

#print(printout)
with open("data_for_sql/corresp.sql", mode = "w", encoding = "utf8") as f:
	f.write(printout[:-2]) #-2 to remove the last ",\n"
