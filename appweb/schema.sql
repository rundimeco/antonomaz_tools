DROP TABLE IF EXISTS corpus;
DROP TABLE IF EXISTS item;
DROP TABLE IF EXISTS page;
DROP TABLE IF EXISTS similarity;
DROP TABLE IF EXISTS sim;

CREATE TABLE corpus(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_moreau INTEGER NOT NULL,
    nb_page INTEGER NOT NULL,
    titre TEXT NOT NULL,
    date TEXT NOT NULL,
    lieu TEXT NOT NULL
);

CREATE TABLE page (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_page INTEGER NOT NULL,
    item INTEGER NOT NULL,
    url_num TEXT NOT NULL,
    url_txt TEXT NOT NULL,
    url_alto TEXT NOT NULL,
    FOREIGN KEY(item) REFERENCES item(id_moreau)
);

CREATE TABLE similarity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE sim (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_sim INTEGER NOT NULL,
    id_p1 INTEGER NOT NULL,
    id_p2 INTEGER NOT NULL,
    val_sim REAL NOT NULL,
    FOREIGN KEY(id_sim) REFERENCES similarity(id),
    FOREIGN KEY(id_p1) REFERENCES page(id),
    FOREIGN KEY(id_p2) REFERENCES page(id)
);