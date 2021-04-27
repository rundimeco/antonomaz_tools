import json
import jellyfish
import codecs
import re

def get_by_episode(nom):
  pass

def get_episode_by_id(ID):
  pass

def get_ids_same_episode(ID):
  pass

def get_episodes_by_year(year):
  """
  Avec une année, on a touss les épisodes de cette année
  """
  year = str(year)
  data = get_json("data/chronologie_moreau.json")
  if year not in data:
    res = {"Statut": f"Année '{year}' non trouvée", "Requête":year, "Années présentes":list(data.keys())}
    return res 
  etiquettes = [x["Etiquette Moreau"] for x in data[year]]
  res = {"Statut": "OK", "Requête":year, "Résultat":etiquettes}
  return res

def get_all_episodes():
  """
  TousAvec une année, on a toutes les Mazarinades datées de cette année
  """
  all_years = get_episodes_by_year(000)["Années présentes"]
  etiquettes = []
  for year in all_years:
    etiquettes.append({year : get_episodes_by_year(year)["Résultat"]})
  res = {"Statut": "OK", "Requête":year, "Résultat":etiquettes}
  return res

def get_chronological():
  pass


def get_json(path):
  """ Ouvre un fichier JSON"""
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
  liste = get_json("data/liste_titres_ID.json")
 
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

def open_utf8(path,lines=False):
  """Ouvre un fichier texte"""
  f = codecs.open(path,'r','utf-8')
  if  lines==True:
    out = f.readlines()
    out = [re.sub("\n|\r","",x) for x in out]
  else:
    out = f.read()
  f.close()
  return out

def write_utf8(path, out, verbose =True, is_json = False):
  """
  En entrée, un chemin et un contenu (chaîne)
  Ecrit le contenu dans le chemin indiqué 
  """
  w = codecs.open(path,'w','utf-8')
  if is_json==False:
    w.write(out)
  else:
    w.write(json.dumps(out, indent=2, ensure_ascii=False))
  w.close()
  if verbose:
    print("Output written in '%s'"%path)


