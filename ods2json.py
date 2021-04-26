from pandas_ods_reader import read_ods
import re
import json

path = "data/ListeMazarinades_light.ods"

#sheet_idx = 1
#df = read_ods(path, sheet_idx)

sheet_name = "Documents_all"
df = read_ods(path, sheet_name)
##colonnes : ID, titre, date, date_precise, lieu, nb pages, Notice, note, ?
dic = {}

for line in df.iterrows():
  id_base = line[1][0]
  if "*" in str(id_base) or "-" in str(id_base) or "_" in str(id_base):
    ID = str(id_base)
  else:
    ID = str(int(id_base))
  value = list(line[1].values[1:])
  nom_infos = ["Titre", "Année", "Date Précise", "Lieu", "Nb. Pages", "Notice", "Note"]
  try:
    value[1] = int(value[1])
  except:
    pass
  try:
    value[4] = int(value[4])
  except:
    pass
  value = {nom_infos[i]:value[i] for i in range(len(value))}
  if ID in dic:
    print("ID déjà présente", ID)
    1/0
  dic[ID] = value
as_list = [[cle, val["Titre"]] for cle, val in dic.items()]

for nom, struct in [["liste", as_list], ["dico", dic]]:
  path_out = f"{nom}_titres_ID.json"
  print(path_out)
  w = open(path_out, "w")
  w.write(json.dumps(struct, indent =2, ensure_ascii=False))
  w.close()
