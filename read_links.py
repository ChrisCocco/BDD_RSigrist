# -*- coding: utf-8 -*-

import pandas as pd
import re

dfsA1_base = pd.read_html('DATA/LiensA1.htm', header = 0)

dataA1_base = dfsA1_base[0]




printout   = str()

printout = "INSERT INTO Liens (id_savant)\n"


#################
#### A bases ####
#################

for index, row in dataA1_base.iterrows():

	id_savant = str(row['Numéro']).zfill(4)

	printrow  = '(\'' + id_savant + '\', \'A\'' + '),\n'

	printrow  = printrow.replace("'NULL'", "NULL")

	printout += printrow

print(printout)