# -*- coding: utf-8 -*-

import pandas as pd


# pd.read_csv('../BDD/Essais_conversions/A1Base_depuis_FM5_tab.tab', sep = '\t')

# problèmes de lecture, passer par autre chose que pandas... (UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe8 in position 4: invalid continuation byte)

dfs = pd.read_html('../BDD/Conversions_tab/A1_base_a_ouvrir_avec_Excel.htm', 
    header = 0)

data = dfs[0]    

#print(data["Numéro"])

print(data.loc[:,"Numéro"])
print(data["Numéro"]) #is equivalent to the line above

#print(data["Numéro"] == 1)
data.loc[lambda df: df.Numéro == 1, :]
#data.get_indexer(data["Numéro"] == 1) #Faux comme ça, il faut trouver comment faire...


##html = open('../BDD/Conversions_tab/A1_base_a_ouvrir_avec_Excel.htm').read().splitlines()
##for line in html:
##    print("line:")
##    print(line)
##    print()
#
#import csv
#
## AVANT EXPORT, FAIRE DEFINE FIELD ET CLIQUER SUR FIELD POUR ORDRER PAR ORDRE ALPHABETIQUE
#
#data = []
#
#with open ('../BDD/Conversions_tab/A1_base.tab') as csvfile:
#    datareader = csv.reader(csvfile, delimiter = '\t')
#    for row in datareader:
#        print(row)
#        print(','.join(row))
#        data.append(row)
#    
#labels = ['A. Berlin','A. Bologne','A. Londres','A. Paris','A. Pétersb.','A. Stockh.','Acad. 7','Acad. 8','Acad. 9','catg. DSB1','catg. DSB2','catg. DSB3','catg. DSB4','Discipl. 1',
#              'Discipl. 2','Discipl. 3','Discipl. 4','Discipl. 5','Equipement','Lieu 1','Lieu 2','Lieu 3','Lieu 4','Lieu mort','Lieu naiss.','Mort','Nom','Numéro',
#              'Né','Pays 1','Pays 2','Pays 3','Pos. acad. 1','Prix 1','Prix 2','Prov. 1','Prov. 2','Empire','Prénom','Remarques','Source 1','Source 2',
#              'Source 3','titre nob.','Nbre acad.','DSB et Macmill.','AA et AAA','Pos. acad. 2','Corrections','Gasc.','Source 5','Source 4']
#df = pd.DataFrame.from_records(data,columns = labels)
#
## Pour l'instant ne marche pas...
#df2 = pd.ExcelFile('../BDD/Conversions_tab/A1_base_a_ouvrir_avec_Excel.xlsx')



