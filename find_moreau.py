from antono_tools import *
def get_from_ID(ID):
  dic_titres = get_json("dico_titres_ID.json")
  ID = str(ID)
  message = "Correspondance trouvée"
  if ID not in dic_titres:
    if ID+"*" in dic_titres:
      ID+="*"
    else:
      message = "Identifiant inconnu. La liste Moreau va de 1 à 4082, le supplémente 1 va de  1 à 209, le supplément 2 va de 1 à 90. Pour les suppléments Moreau la syntae est la suivante: SupX_ID où X est le numéro du supplément (1 ou 2) et ID est le numéro du titre dans le supplément."
  
  return {"Statut": message, "Requête":ID, "Résultat":dic_titres[ID]}

def get_from_title(title):
  plus_proches = get_closest(title, 1)
  if len(plus_proches)==0:
    return {"Statut": "Pas de correspondance", "Requête":titre, "Résultat":{}}
  ID = plus_proches[0][1]
  infos = get_from_ID(ID)
  infos["Requête"] = title
  return infos

if __name__=="__main__":
  print(get_from_ID(78))

  print(get_from_title("badaud"))
