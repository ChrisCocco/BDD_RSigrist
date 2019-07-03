# -*- coding: utf-8 -*-

import pandas as pd
import re


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

print(list(set(dataA.champ1.unique(),dataA.champ2.unique())))


all_fields = set(
	list(dataA.champ1.unique())+
	list(dataA.champ2.unique())+
	list(dataA.champ3.unique())+
	list(dataA.champ4.unique())+
	list(dataB['Champ 1'].unique())+
	list(dataB['Champ 2'].unique())+
	list(dataB['Champ 3'].unique())
	)

accents = (u'\x92', u"'"), ('é', 'e'), ('è', 'e'), ('â', 'a'), ('ö', 'o'), \
		('ü', 'u'), ("(",""), (")","")

import functools # to use "reduce"



for item in all_fields:
	if not pd.isna(item):
		print(item.replace("(",""))
		print(functools.reduce(
				lambda a, kv: a.replace(*kv), accents, item
				))

all_fields = [functools.reduce(
				lambda a, kv: a.replace(*kv), accents, field
				) 
				for field in all_fields if not pd.isna(field)]

# len(set(
# 	list(dataA.champ1.unique())+
# 	list(dataA.champ2.unique())+
# 	list(dataA.champ3.unique())+
# 	list(dataA.champ4.unique())+
# 	list(dataB['Champ 1'].unique())+
# 	list(dataB['Champ 2'].unique())+
# 	list(dataB['Champ 3'].unique())
# 	))

# remove accents
# remove brackets 
# Levenshtein Distance: 
# https://stackabuse.com/levenshtein-distance-and-text-similarity-in-python/
# https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
# https://pypi.org/project/python-Levenshtein/0.12.0/
# https://pypi.org/project/jellyfish/
# https://www.python-course.eu/levenshtein_distance.php

#################
#### A bases ####
#################

# for index, row in dataA.iterrows():
