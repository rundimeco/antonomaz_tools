from antono_tools import *

def get_supp(ID, dic_titres):
  liste_cles = dic_titres.keys()
  supps = [re.split("-", x) for x in liste_cles]
  nom_sup = set([x[0] for x in supps if len(x)>1 and len(x[0])>0])
  has_supp = []
  for n in nom_sup:
    ID_supp = f"{n}-{ID}"
    if ID_supp in dic_titres:
      has_supp.append(ID_supp)
  if len(has_supp)>0:
    S = ", ".join(has_supp)
    return ", le numéro %s existe aussi dans des suppléments (%s)"%(ID, S)
  else:
    return ""

def get_from_ID(ID, check_supp=True):
  """
  A partir d'un ID, donne les informations de la base issue de Moreau
  Donne la sortie sous forme de dictionnaire Python
  Si l'ID n'existe pas, le "Statut" l'indique
  """
  ID = re.sub("_", "-", str(ID))
  dic_titres = get_json("data/dico_titres_ID.json")
  dic_titres = {str(re.sub("_", "-", x)):y for x,y in dic_titres.items()}

  message = "Correspondance trouvée"
  if ID not in dic_titres:
    if ID+"*" in dic_titres:
      ID+="*"
    else:
      #Message d'erreur stocké dans un Json :
      message = get_json("data/messages.json")["ID_inconnue"]
  elif check_supp==True:#on regarde les suppléments possibles pour l'ID
    msg_supp = get_supp(ID, dic_titres)
    message+=msg_supp
  return {"Statut": message, "Requête":ID, "Résultat":dic_titres[ID]}

def get_from_title(title):
  """
  Donne le titre le plus proche trouvé dans la base issue de Moreau
  """
  plus_proches = get_closest(title, 1)
  if len(plus_proches)==0:
    return {"Statut": "Pas de correspondance", "Requête":titre, "Résultat":{}}
  ID = plus_proches[0][1]
  infos = get_from_ID(ID, check_supp=False)
  infos["Requête"] = title
  return infos

if __name__=="__main__":

  print("Recherche de l'ID 78 :")
  print(get_from_ID(78))

  print("\nRecherche de soc_1 :")
  print(get_from_ID("soc_1"))
  
  print("\nChercher un titre proche de 'badaud'")
  print(get_from_title("badaud"))

  print("\nTest numéro dans plusieurs suppléments (3)")
  #Numéro présent dans plusieurs suppléments
  print(get_from_ID(3)["Statut"])
