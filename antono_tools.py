# -*- coding: utf-8 -*-
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
def get_closest_v2(title, number = 10, lowercase=True, 
                path_compare ="data/all_burlesque_pages_corrected.json", word_filter = True,
                seuil_simil = False, javeliser = False):
    """ 
  En entrée, une chaîne de caractère et en option :
    le nombre de titres proches à retourner, par défaut : 10
    mettre en minuscules, par défaut: non
    le chemin des documents à comparer
    word_filter: premier filtre sur le nombre de mots en commun (impact sur le temps de calcul ?)
    seuil_simil: si activé (flottant) on ne donne que les docs au delà du seuil
  En sortie, la liste triée par ordre décroissant de similarité sous forme d'un triplet:
    distance, ID_moreau, titre concerné
  """
    liste_depart = get_json(path_compare)
    #all_burlesque_pages_original_ocr.json
    #all_burlesque_pages_ocr_without_linebreak.json
    #all_burlesque_pages_corrected_without_linebreak.json
    #all_burlesque_pages_corrected.json
    #all_burlesque_pages_ocr_without_space.json
    liste=[]
    if lowercase==True:
        for i in liste_depart:
            liste.append(word.lower() for word in i)
    mots_titre = set(title.split())
    filtered_list = []
    for ID, chaine in  liste:
        mots_candidat = set(chaine.split())
        inter = mots_titre.intersection(mots_candidat)
    ##Si moins de 5 mots en commun (ou de la moitié) inutile de garder le candidat
        if len(inter)>5 or len(inter)>(len(mots_titre)/2) or word_filter==False:
            filtered_list.append([len(inter), ID, chaine])
    f2 = []
    for len_inter, ID, chaine in filtered_list:
        if javeliser==True:
            title  = re.sub("\n| {2,}", " ", title)
            chaine = re.sub("\n| {2,}", " ", chaine)
        sim = jellyfish.jaro_winkler(title,chaine)
    ## On garde quand la similarité est supérieure à 0.5
        f2.append([sim, ID, chaine])
    if seuil_simil!=False:
        f2 = [x for x in f2 if x[0]>seuil_simil]
    return sorted(f2, reverse=True)[:number]

# old function :
def get_closest(title, path_data="data/liste_titres_ID.json", number = 5, lowercase =True):
  """ 
  En entrée, une chaîne de caractère (
      en option:
          le chemin du json du corpus considéré (par défaut: data/liste_titres_ID.json)
          le nombre de titres proches à retourner ( par défaut : 5)
  En sortie, la liste triée par ordre décroissant de similarité sous forme d'un triplet:
    distance, ID_moreau, titre concerné
  """
  liste = get_json(path_data)
  if lowercase==True:
    title = title.lower()
 
  mots_titre = set(title.split())
  filtered_list = []
  for ID, chaine in  liste:
    if lowercase==True:
        chaine = chaine.lower()
    mots_candidat = set(chaine.split())
    inter = mots_titre.intersection(mots_candidat)
    ##Si moins de 5 mots en commun (ou de la moitié) inutile de garder le candidat
    if len(inter)>3 or len(inter)>=(len(mots_titre)/2):
        filtered_list.append([len(inter), ID, chaine])
  f2 = []
  for len_inter, ID, chaine in filtered_list:
    if lowercase==True:
        chaine = chaine.lower()
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

# +
##get_closest("reine de france", number = 2)

# +
#get_closest("Reine de France", number = 2)

# +
#get_closest("Reine de France", number = 2, path_data = "clean.json")
#get_closest("Reine de France", number = 2, path_data = "dirty.json")
# -


