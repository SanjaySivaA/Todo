import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)

def initialise_database():
    c = sqlite3.connect('todo.db')
    c.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT, status TEXT DEFAULT "Pending")')
    c.close()

initialise_database()

@app.route('/add-task', methods=['POST', 'GET'])
def add_task():
    if request.method == 'POST':
        task = request.form['task']
        with sqlite3.connect('todo.db') as c:
            cur = c.cursor()
            cur.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
            c.commit()
            resp = "Task added to database"
        return jsonify({"response" : resp})
    

@app.route('/remove-task', methods=['POST', 'GET'])
def remove_task():
    if request.method == 'POST':
        id = request.form['id']
        with sqlite3.connect('todo.db') as c:
            cur = c.cursor()
            cur.execute("DELETE FROM tasks WHERE id = ?", (id,))
            c.commit()
            resp = "Task deleted from database"
        return jsonify({"response" : resp})


@app.route('/update-task', methods=['POST', 'GET'])
def update_task():
    if request.method == 'POST':
        id = request.form['id']
        task = request.form['task']
        status = request.form['status']
        with sqlite3.connect('todo.db') as c:
            cur = c.cursor()
            cur.execute("UPDATE tasks SET task = ?, status = ? WHERE id = ?", (task, status, id))
            c.commit()
            resp = "Task data updated"
        return jsonify({"response" : resp})


if __name__ == '__main__' :
    app.run(debug=True)