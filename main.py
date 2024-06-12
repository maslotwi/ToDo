import json
import sqlite3
from flask import Flask, send_file, Response

app = Flask(__name__)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/')
def hello_world():
    return send_file('./static/index.html')


@app.route('/tasks')
def get_tasks():
    conn = sqlite3.connect('dane.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute('SELECT id, name, description, due FROM tasks')
    tasks = c.fetchall()
    return Response(json.dumps(tasks), mimetype='application/json')


def main():
    conn = sqlite3.connect('dane.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS Tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(20) NOT NULL,
    description VARCHAR(1000),
    due DATE
    );''')
    app.run()


if __name__ == '__main__':
    main()

