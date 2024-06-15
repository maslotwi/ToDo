import dataclasses
import json
import sqlite3
from datetime import datetime
from dataclasses import dataclass
from flask import Flask, send_file, Response, request

app = Flask(__name__)


@dataclass(frozen=True, order=True)
class Task:
    id: int
    name: str
    description: str | None = None
    due: datetime | None = None

    @staticmethod
    def from_sql_row(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return Task(**d)


class TaskEncoder(json.JSONEncoder):
    def default(self, task):
        if isinstance(task, Task):
            return dataclasses.asdict(task)
        return super().default(task)


@app.route('/')
def hello_world():
    return send_file('./static/index.html')


@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = sqlite3.connect('dane.db')
    conn.row_factory = Task.from_sql_row
    c = conn.cursor()
    c.execute('SELECT id, name, description, due FROM Tasks')
    tasks = c.fetchall()
    return Response(json.dumps(tasks, cls=TaskEncoder), mimetype='application/json')


@app.route('/tasks', methods=['POST'])
def add_task():
    conn = sqlite3.connect('dane.db')
    c = conn.cursor()
    c.execute("INSERT INTO Tasks VALUES (null, ?, ?, ?)", (request.json['name'], request.json['description'], request.json['due']))
    conn.commit()
    return '{}'


@app.route('/tasks', methods=['DELETE'])
def delete_task():
    conn = sqlite3.connect('dane.db')
    c = conn.cursor()
    c.execute("DELETE FROM Tasks where id=?", (request.json['id'],))
    conn.commit()
    return "{}"


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
    app.run(host='0.0.0.0', port=8080)


if __name__ == '__main__':
    main()
