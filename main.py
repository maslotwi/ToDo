import dataclasses
import json
import sqlite3
from typing import Iterable, Generator
from ctypes import cdll, c_time_t, POINTER, c_int
from datetime import datetime
from dataclasses import dataclass
from flask import Flask, send_file, Response, request

days = cdll.LoadLibrary('build/libdays.so')
days.calculate_days.argtypes = [POINTER(c_time_t), c_int]
days.calculate_days.restype = POINTER(c_int)

app = Flask(__name__)



@dataclass(order=True)
class Task:
    id: int
    name: str
    description: str | None = None
    due: datetime | None = None
    days: int | None = None

    @staticmethod
    def from_sql_row(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            if col[0] == 'due' and row[idx] is not None:
                d['due'] = datetime.fromisoformat(row[idx])
            else:
                d[col[0]] = row[idx]
        return Task(**d)


class TaskEncoder(json.JSONEncoder):
    def default(self, task):
        if isinstance(task, Task):
            x = dataclasses.asdict(task)
            if x['due'] is not None:
                x['due'] = f"{task.due:%Y-%m-%d}"
            return x
        return super().default(task)


def calculate_days(tasks: Iterable[Task]) -> Generator[Task,None,None]:
    tasks = list(tasks)
    dane = (c_time_t * len(tasks))()
    for i, task in enumerate(tasks):
        if task.due is None:
            dane[i] = 0
        else:
            dane[i] = int(task.due.timestamp())
    wynik = days.calculate_days(dane, len(dane))
    for i, task in enumerate(tasks):
        if task.due is not None:
            task.days = wynik[i]
        yield task


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
    return Response(json.dumps(list(calculate_days(tasks)), cls=TaskEncoder), mimetype='application/json')


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
