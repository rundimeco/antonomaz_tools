**Données** (dossier data)

 - ListeMazarinades.json : dernière version de la base issue de Moreau (09/04/2021)
 - messages.json : message utilisés pour renseigner les réponses aux requêtes
 - dico_titres_ID.json : correspondance entre les ID Moreau et informations de la base
 - liste_titres_ID.json : liste des couprs ID, titre de la base

**Programmes**

***find_moreau.py***

Lancer ce programme donne un exemple de requête sur des IDs et un exemple de requête sur les titres grâce aux deux fonctions suivantes :
  - get_from_ID(ID) : à partir d'un ID moreau, donne les informations de la base issue de Moreau
  - get_form_title(titre) : à partir d'un titre, donne le titre le plus proche dans la base


***ods2json.py***

Génère deux Json (dico_titres_ID et liste_titres_ID) à partir du tableur ods

***json_to_vizu.py*** (Beta)

Génère un tableau Html à partir de dico_titres_ID.json


Avancée sur la similarité:

- stocker le vectoriseur (tf-df ou count ?)
- observer les alignements
- comment régler la question des pages 1 ?

Comparer avec text-pair ?

Qu'en tirer pour la phraséologie ?

