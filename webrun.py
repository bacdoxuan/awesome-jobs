import os
import sqlite3
from flask import Flask, render_template


app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'jobs.db'),
))


def connect_db():
    """Connect to database in app.config"""
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def show_jobs():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('select * from jobs')
    jobs = cur.fetchall()
    return render_template('show_jobs.html', jobs=jobs)
