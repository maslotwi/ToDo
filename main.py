import dataclasses
import json
import sqlite3
from datetime import datetime
from dataclasses import dataclass
from flask import Flask, send_file, Response

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


@app.route('/tasks')
def get_tasks():
    conn = sqlite3.connect('dane.db')
    conn.row_factory = Task.from_sql_row
    c = conn.cursor()
    c.execute('SELECT id, name, description, due FROM tasks')
    tasks = c.fetchall()
    return Response(json.dumps(tasks, cls=TaskEncoder), mimetype='application/json')




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
