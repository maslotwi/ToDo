import json
import sqlite3
from flask import Flask, send_file, Response

app = Flask(__name__)


@app.route('/')
def hello_world():
    return send_file('./static/index.html')


@app.route('/tasks')
def get_tasks():
    conn = sqlite3.connect('dane.db')
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

