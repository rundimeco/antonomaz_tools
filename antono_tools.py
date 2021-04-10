import json
import jellyfish

def get_json(path):
  f = open(path)
  liste = json.load(f)
  f.close()
  return liste

def get_closest(title, number = 5):
  """ 
  En entrée, une chaîne de caractère (et en option le nombre de titres proches à retourner, par défaut : 5)
  En sortie, la liste triée par ordre décroissant de similarité sous forme d'un triplet:
    distance, ID_moreau, titre concerné
  """
  liste = get_json("liste_titres_ID.json")
 
  mots_titre = set(title.split())
  filtered_list = []
  for ID, chaine in  liste:
    mots_candidat = set(chaine.split())
    inter = mots_titre.intersection(mots_candidat)
    ##Si moins de 5 mots en commun (ou de la moitié) inutile de garder le candidat
    if len(inter)>5 or len(inter)>(len(mots_titre)/2):
        filtered_list.append([len(inter), ID, chaine])
  f2 = []
  for len_inter, ID, chaine in filtered_list:
    sim = jellyfish.jaro_winkler(title,chaine)
    ## On garde quand la similarité est supérieure à 0.5
    if sim>0.5:
      f2.append([sim, ID, chaine])
  return sorted(f2, reverse=True)[:number]
