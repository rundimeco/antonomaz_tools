#! /usr/bin/python3.5
#from antono_tools import get_closest_v2
# -*- coding:utf-8 -*-
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy import spatial
import sys
import os    
import cgi                        # Module d'interface avec le serveur web
import json
import codecs
#import jellyfish
from jaro import get_jaro_distance
import re
import pickle
import scipy.sparse
def longest_common_substring(s1, s2):
  m = [[0] * (1 + len(s2)) for i in range(1 + len(s1))]
  longest, x_longest = 0, 0
  for x in range(1, 1 + len(s1)):
    for y in range(1, 1 + len(s2)):
      if s1[x - 1] == s2[y - 1]:
        m[x][y] = m[x - 1][y - 1] + 1
        if m[x][y] > longest:
          longest = m[x][y]
          x_longest = x
      else:
        m[x][y] = 0
  return s1[x_longest - longest: x_longest]

#def enc_print(string='', encoding='utf8'):
#    sys.stdout.buffer.write(string.encode(encoding) + b'\n')

def get_json(path):
  """ Ouvre un fichier JSON"""
  f = codecs.open(path, "r", "utf-8")
  liste = json.load(f, strict=False)
  f.close()
  return liste

def ouvrir(path):
  f = codecs.open(path, "r", "utf-8")
  chaine = f.read()
  f.close()
  return chaine

def get_closest_v2(title, number = 10, lowercase=True, 
                path_compare ="../../data/all_burlesque_pages_corrected.json", 
                seuil_simil = False, javeliser = True, vectorize=True):
    """ 
  En entrée, une chaîne de caractère et en option :
    le nombre de titres proches à retourner, par défaut : 10
    mettre en minuscules, par défaut: non
    le chemin des documents à comparer
    seuil_simil(obsolète): si activé (flottant) on ne donne que les docs au delà du seuil
  En sortie, la liste triée par ordre décroissant de similarité sous forme d'un triplet:
    distance, ID_moreau, titre concerné
  """
    L = get_json(path_compare)
    #all_burlesque_pages_original_ocr.json
    #all_burlesque_pages_ocr_without_linebreak.json
    #all_burlesque_pages_corrected_without_linebreak.json
    #all_burlesque_pages_corrected.json
    #all_burlesque_pages_ocr_without_space.json
    liste=[]
    if javeliser==True:
      L = [[ID, re.sub("\n| {2,}", " ",txt)] for ID, txt in L]
      title  = re.sub("\n| {2,}", " ", title)
    if lowercase==True:
      L = [[ID, txt.lower()] for ID, txt in L]
      title = title.lower()
    if vectorize ==True:
      path_pickle = "%s.pickle"%path_compare
      if 2<1:#os.path.exists(path_pickle):#Gain vitesse: 10 à 30% selon taille matrice
        print("loading index")
        vect = pickle.load(open(path_pickle, "rb"))
        X = scipy.sparse.load_npz('%s.npz'%path_compare)
      else:
        V = TfidfVectorizer(ngram_range=(5, 7), analyzer = "char", max_features=50000)#max features 10000: temps de calcul/40, 50000 tps/5
        vect = V.fit([txt for ID, txt in L])
        pickle.dump(vect, open(path_pickle, "wb"))
        X = vect.transform([txt for ID, txt in L])
        scipy.sparse.save_npz('%s.npz'%path_compare, X)
      X = X.toarray()
      y = vect.transform([title]).toarray()[0]
      print(" computing distances")#C'est le verrou en terme de temps de calcul
      #braycurtis, cosine, jaccard équivalent en temps
      #dice (un peu plus long)
      #dist =[spatial.distance.cosine(y,x) if sum(x)>0 else 1  for x in X]
      dist =[spatial.distance.dice(y,x) if sum(x)>0 else 1  for x in X]
    cpt = 0
    f2 = []
    for ID, chaine in L:
        if vectorize==True:
          sim = 1-dist[cpt]
        else: 
          #sim = jellyfish.jaro_winkler(title,chaine)##problème import
          sim = 1-get_jaro_distance(title,chaine)
        cpt+=1
        if len(chaine)<5:
          continue
        f2.append([sim, ID, chaine])
    if seuil_simil!=False:
        f2 = [x for x in f2 if x[0]>seuil_simil]
    return sorted(f2, reverse=True)[:number]

def prettify(liste, content, test):
  out = {"query":content, "results":[]}
  str_prediction = "<table class='styled-table' border = '1'>\n"
  content= re.sub(" {2,}", " ", content)
  lines = re.split("\n", content)
  if len(lines)>100:
    portions = 10
  elif len(lines)<10:
    portions = 5
  else:
    portions = int(len(lines)/10)
  for sim, ID ,chaine in liste:
    chaine = re.sub("\n| {2,}", " ", chaine)
    desc_base = []
    for i in range(0, len(lines), portions):
      s = longest_common_substring(chaine, "".join(lines[i:i+5]))
      desc_base.append(s)
    descs = [[len(x), x] for x in set(desc_base)]
    descs = sorted(descs, reverse=True)[:20]
    minilen = len(descs[-1])
    all_descs_order = [x for x in desc_base if len(x)>minilen]
    result ={"ID":ID,"content":chaine,"score":sim,"descriptors":all_descs_order}
    out["results"].append(result)
    all_descs_order = "</li>\n  <li>".join(all_descs_order)
    uniq = set([y for x, y in descs])
    for u in uniq:
      chaine = re.sub(u, "<span class='desc'>%s</span>"%u, chaine)
    sim = round(sim, 4)
    ss = "<ul>\n <li>"+all_descs_order+"</li></ul>"
    chaine = "<p>%s</p>"%(re.sub("\n{1,}", "</p>\n<p>", chaine))
    source, filename, numpage = re.split("_", ID)
    numpage = str(int(numpage)+1)
    ID_gallica = re.sub("\.xml", "", filename)
    url = "https://gallica.bnf.fr/ark:/12148/%s/f%s.item"%(ID_gallica,numpage)
    link = "<a target ='_blank' href='%s'>%s</a>"%(url, str(ID))
    str_prediction +="<tr><td><p>%s</p><p>%s</p></td><td>%s</td><td>%s</tr>\n"%(str(sim), link, ss, chaine)
  str_prediction +="</table>\n"
  #dd = input("continue?")
  return str_prediction, out


fic_json = open("chemins_GL.json", "r")
dic = json.load(fic_json)
fic_json.close()
test = False

path_save_texte = dic["sauvegarde_texte"]
if len(sys.argv)==2:
  test = True
  path_save_texte = sys.argv[1]

path_prediction = dic["prediction"]
path_model = dic["model"]
path_dic_features = dic["dic_features"]

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())#sinon pb encoding
print("Content-type:text/html\r\n\r\n")
print('<html>\n<head> \n<meta charset="utf-8" />\n')
print('<link rel="stylesheet" href="memes.css" />\n')
print('<title>Test de Similarité</title>\n</head>')
print('<body>')

form = cgi.FieldStorage()

if "fichier" in form:
  f = form["fichier"]
  if f.file:
    content = f.value.decode("utf-8")
    fic = codecs.open(path_save_texte, "w", "utf-8")
    fic.write(content)
    fic.close()
else:
  print("<p>No file provided, default file loaded</p>")
  content = ouvrir(path_save_texte)

print("<h2>Source</h2>")

extrait = re.sub(" {2,}", "", content)
extrait = "<p>%s</p>"%(re.sub("[\n\r]{1,}", "</p>\n<p>", extrait))

print("<div class = 'scroll'><p>%s </p></div>"%extrait)

print("<p> (%i lignes)</p>"%len(re.split("\n", content)))
print("starting similarity computing ...")

str_prediction = get_closest_v2(content, number = 20, vectorize = True)

str_prediction, out = prettify(str_prediction, content, test)
w = open("%s.json"%path_save_texte, "w")
w.write(json.dumps(out, indent=2))
w.close()

print("<p>Done...</p>")
#if test!=True:
print(str_prediction)

print('</body>')
print('</html>')
