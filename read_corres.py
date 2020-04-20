# -*- coding: utf-8 -*-

import pandas as pd
import re
import functools # to use "reduce"

dfsA  = pd.read_html('DATA/CorresA.htm', header = 0)
dfsB = pd.read_html('DATA/CorresB.htm', header = 0)

dataA = dfsA[0]
dataB = dfsB[0]



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
				#last bracket "\)" removed in regex, since once "(3X9" instead of "(3X)"
				# Now, corrected, but not useful to change
	#			print(parts)
				if parts:
					id_sav_2   = parts.group(2) 
					weight     = int(parts.group(4))
					type_sav_2 = "A"

				else:
					print(index, corr)
		for corr in colnames_corr_AB:
			if pd.notna(row[corr]) and row[corr] != "-----":
				parts = re.search(
					'(.+)(?:,|.) no ([0-9]{4}(\-B)?) \(([0-9])X', 
					row[corr]) 
				#last bracket "\)" removed in regex, since once "(3X9" instead of "(3X)"
				# Now, corrected, but not useful to change
	#			print(parts)
				if parts:
					id_sav_2   = parts.group(2) 
					weight     = int(parts.group(4))
					type_sav_2 = "B"

				else:
					print(index, corr)
		if pd.notna(row['Autres corr. A']):
			for scientist in row['Autres corr. A'].split(";"):
				parts = re.search(
					'(.+), no ([0-9]{4}(\-B)?) \(([0-9])X', 
					scientist)
				if parts:
					id_sav_2   = parts.group(2)
					weight     = int(parts.group(4))
					type_sav_2 = "A"
				else:
					print(index,row['Autres corr. A'])
		if pd.notna(row['Autres corr. B']):
			for scientist in row['Autres corr. B'].split(";"):
				parts = re.search(
					'(.+), no ([0-9]{4}(\-B)?) \(([0-9])X', 
					scientist)
				if parts:
					id_sav_2   = parts.group(2)
					weight     = int(parts.group(4))
					type_sav_2 = "B"
				else:
					print(index,row['Autres corr. B'])


colnames_corrB    = ["Corr. " + str(i+1) for i in range(28)]
colnames_corrB_BA = ["Corr. B" + str(i+1) for i in range(28)]

for index, row in dataB.iterrows():
	if pd.notna(row['Corr. 1']) or pd.notna(row['Corr. B1']):
		id_sav   = str(row['Numéro']).zfill(4)
		type_sav = "B"
		for corr in colnames_corrB:
			if pd.notna(row[corr]) and row[corr] != "-----":
				parts = re.search(
					'(.+), no ([0-9]{4}(\-B)?) \(([0-9])X', 
					row[corr]) 
				#last bracket "\)" removed in regex, since once "(3X9" instead of "(3X)"
				# Now, corrected, but not useful to change
	#			print(parts)
				if parts:
					id_sav_2   = parts.group(2) 
					weight     = int(parts.group(4))
					type_sav_2 = "A"
				else:
					print(index, corr)


		for corr in colnames_corrB_BA:
			if pd.notna(row[corr]) and row[corr] != "-----":
				parts = re.search(
					'(.+), no ([0-9]{4}(\-B)?) \(([0-9])X', 
					row[corr]) 
				#last bracket "\)" removed in regex, since once "(3X9" instead of "(3X)"
				# Now, corrected, but not useful to change
	#			print(parts)
				if parts:
					id_sav_2   = parts.group(2) 
					weight     = int(parts.group(4))
					type_sav_2 = "B"
				else:
					print(index, corr)