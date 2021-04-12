from antono_tools import *

def get_from_ID(ID):
  """
  A partir d'un ID, donne les informations de la base issue de Moreau
  Donne la sortie sous forme de dictionnaire Python
  Si l'ID n'existe pas, le "Statut" l'indique
  """
  dic_titres = get_json("data/dico_titres_ID.json")
  ID = str(ID)
  message = "Correspondance trouvée"
  if ID not in dic_titres:
    if ID+"*" in dic_titres:
      ID+="*"
    else:
      #Message d'erreur stocké dans un Json :
      message = get_json("data/messages.json")["ID_inconnue"]
  
  return {"Statut": message, "Requête":ID, "Résultat":dic_titres[ID]}

def get_from_title(title):
  """
  Donne le titre le plus proche trouvé dans la base issue de Moreau
  """
  plus_proches = get_closest(title, 1)
  if len(plus_proches)==0:
    return {"Statut": "Pas de correspondance", "Requête":titre, "Résultat":{}}
  ID = plus_proches[0][1]
  infos = get_from_ID(ID)
  infos["Requête"] = title
  return infos

if __name__=="__main__":

  # Chercher l'ID 78 :
  print(get_from_ID(78))
  
  #Chercher un titre proche de "badaud"
  print(get_from_title("badaud"))
