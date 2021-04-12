from pandas_ods_reader import read_ods
import re
import json

path = "data/ListeMazarinades.ods"

#sheet_idx = 1
#df = read_ods(path, sheet_idx)

sheet_name = "Moreau_all"
df = read_ods(path, sheet_name)
##colonnes : ID, titre, date, date_precise, lieu, nb pages, Notice, note, ?
dic = {}
volume = 0
Sup = ["", "Sup1_", "Sup2_"]

for line in df.iterrows():
  str_volume = Sup[volume]
  if "*" in str(line[1][0]):
    ID = str(line[1][0])
  else:
    ID = str_volume+str(int(line[1][0]))
  value = list(line[1].values[1:])
  nom_infos = ["Titre", "Année", "Date Précise", "Lieu", "Nb. Pages", "Notice", "Note"]
  try:
    value[1] = int(value[1])
  except:
    pass
  value = {nom_infos[i]:value[i] for i in range(len(value))}
  if ID in dic:
    volume+=1
    str_volume = Sup[volume]
    print(ID, "switching volume")
    ID = str_volume+str(int(line[1][0]))
    print(ID)
  dic[ID] = value
as_list = [[cle, val["Titre"]] for cle, val in dic.items()]

for nom, struct in [["liste", as_list], ["dico", dic]]:
  print(nom)
  w = open(f"{nom}_titres_ID.json", "w")
  w.write(json.dumps(struct, indent =2, ensure_ascii=False))
  w.close()
