import sqlite3
import glob
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import scipy.spatial.distance as distance

def insert_similarity_name(cur, sim_name):
    cur.execute("INSERT INTO similarity (name) VALUES (?)",
        (sim_name,)
        )
    sim_id = cur.execute("SELECT * FROM similarity WHERE name = ?",
                    (sim_name,)).fetchone()
    return sim_id[0] # On ne récupère pas la ligne, mais uniquement l'id


def insert_similarities(cur, corpus_path, sim_name, sim_id):
    # sim_name : char_ngram_1,8
    analyzer = sim_name.split('_')[0]
    ngram_range = (int(sim_name.split('_')[-1].split(',')[0]), int(sim_name.split('_')[-1].split(',')[1]))
    corpus = []
    for file in glob.glob(corpus_path + '*.txt'):
        txt = open(file).read()
        corpus.append(txt)
    vectorizer = CountVectorizer(analyzer=analyzer, ngram_range=ngram_range, max_features=50000)
    vectorizer.fit(corpus)

    for file1 in glob.glob(corpus_path + '*.txt'):
        # ./sources/Corpus/1-100/Moreau65_GALL.pdf-10.txt
        file_name = file1.split('/')[-1]
        id_moreau = file_name.split('_')[0].replace('Moreau', '')
        num_page = file_name.split('-')[-1].replace('.txt', '')
        id_p1 = cur.execute("SELECT * FROM page WHERE item = ? AND id_page = ?",
                            (id_moreau,num_page,)).fetchone()
        id_p1 = id_p1[0] # uniquement l'id
        for file2 in glob.glob(corpus_path + '*.txt'):
            file_name = file2.split('/')[-1]
            id_moreau = file_name.split('_')[0].replace('Moreau', '')
            num_page = file_name.split('-')[-1].replace('.txt', '')
            id_p2 = cur.execute("SELECT * FROM page WHERE item = ? AND id_page = ?",
                                (id_moreau,num_page,)).fetchone()
            id_p2 = id_p2[0] # uniquement l'id
            # On regarde si on n'a pas déjà calculé la similarité auparavant
            calculated_sim = cur.execute("SELECT * FROM sim WHERE id_sim = ? AND id_p1 = ? AND id_p2 = ?",
                                (sim_id,id_p1,id_p2,)).fetchone()
            if file1 != file2 and calculated_sim == None: # Si on n'a pas deux fois le même fichier + si on n'a pas déjà calculé la similarité en question
                txt1 = open(file1).read()
                txt2 = open(file2).read()
                vec1 = vectorizer.transform([txt1]).toarray()
                vec2 = vectorizer.transform([txt2]).toarray()
                sim = 1 - distance.cosine(vec1, vec2)
                cur.execute("INSERT INTO sim (id_sim, id_p1, id_p2, val_sim) VALUES (?, ?, ?, ?)",
                            (sim_id, id_p1, id_p2, sim)
                            )


connection = sqlite3.connect('database.db')

# Parcours du tableur qui contient les informations de la bibliographie de Moreau
liste_maz = {}
with open('./static/ListeMazarinades_all_22juin2021.csv') as f:
    line = f.readline()
    while line != '':
        line = line.strip().split(',')
        if len(line) > 5:
            liste_maz[line[0]] = [line[1], line[2], line[4], line[5]]
        line = f.readline()

cur = connection.cursor()

# Insertion des items dans la table ITEM
corpus_path = './static/Corpus/101-200/'
for file in glob.glob(corpus_path + '*.pdf'):
    id_moreau = file.split('/')[-1].split('_')[0].replace('Moreau', '')
    id_moreau_table = cur.execute("SELECT * FROM item WHERE id_moreau = ?",
                                (id_moreau,)).fetchone()
    if id_moreau_table != None: # Ca veut dire qu'on a déjà l'item dans la BDD
        continue
    else:
        if id_moreau in liste_maz.keys() and '-' not in id_moreau:
            info = liste_maz[id_moreau]
            cur.execute("INSERT INTO item (id_moreau, nb_page, titre, date, lieu) VALUES (?, ?, ?, ?, ?)",
                (id_moreau, liste_maz[id_moreau][3], liste_maz[id_moreau][0], liste_maz[id_moreau][1], liste_maz[id_moreau][2])
                )

# Insertion des pages dans la table PAGE
for file in glob.glob(corpus_path + '*.png'):
    # ./sources/Corpus/1-100/Moreau65_GALL.pdf-10.png
    file_name = file.split('/')[-1]
    id_moreau = file_name.split('_')[0].replace('Moreau', '')
    num_page = file_name.split('-')[-1].replace('.png', '')
    id_moreau_table = cur.execute("SELECT * FROM page WHERE item = ? AND id_page = ?",
                                (id_moreau, num_page,)).fetchone()
    if id_moreau_table != None: # Ca veut dire qu'on a déjà l'item dans la BDD
        continue
    else:
        cur.execute("INSERT INTO page (id_page, item, url_num, url_txt, url_alto) VALUES (?, ?, ?, ?, ?)",
            (num_page, id_moreau, file, file.replace('.png', '.txt'), file.replace('.png', '.alto'))
            )

# Similarity 1: char_ngram_1,8
sim_name = 'char_ngram_1,8'
sim_id = insert_similarity_name(cur, sim_name)
insert_similarities(cur, corpus_path, sim_name, sim_id)

connection.commit()
connection.close()