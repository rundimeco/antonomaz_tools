import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_pages(id_moreau):
    conn = get_db_connection()
    pages = conn.execute('SELECT * FROM page WHERE item = ? ORDER BY id_page',
                        (id_moreau,)).fetchall()
    conn.close()
    print(pages)
    if pages is None:
        abort(404)
    return pages

def get_items():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM item').fetchall()
    conn.close()
    return items

def get_pages_best_sim(page_id):
    conn = get_db_connection()
    sims = conn.execute('SELECT * FROM sim WHERE id_p1 = ? ORDER BY val_sim DESC',
                        (page_id,)).fetchall()
    cpt = 0
    pages = []
    while cpt < 10:
        id_p2 = sims[cpt]['id_p2']
        pages.append(conn.execute('SELECT * FROM page WHERE id = ?',
                    (id_p2,)).fetchone())
        cpt += 1
    return pages

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

@app.route('/')
def index():
    conn = get_db_connection()
    pages = conn.execute('SELECT * FROM page').fetchall()
    conn.close()
    return render_template('index.html', pages=pages)

@app.route('/a_propos/')
def a_propos():
    return render_template('a_propos.html')

@app.route('/search_item', methods=('GET', 'POST'))
def search_item():
    items = get_items()
    if request.method == 'POST':
        id_moreau = request.form['id_moreau']
        return redirect(url_for('pages', id_moreau=id_moreau))
    return render_template('search_item.html', items=items)

@app.route('/similarites/<int:page_id>')
def similarites(page_id):
    pages_best_sim = get_pages_best_sim(page_id)
    return render_template('similarites.html', pages=pages_best_sim)

@app.route('/<string:id_moreau>')
def pages(id_moreau):
    pages = get_pages(id_moreau)
    return render_template('pages.html', pages=pages)

"""
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create.html')"""