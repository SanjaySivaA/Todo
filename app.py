import sqlite3
from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)

def initialise_database():
    c = sqlite3.connect('todo.db')
    c.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, email TEXT, hashed_password TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT, status TEXT DEFAULT "Pending", user_id)')
    c.close()

initialise_database()

@app.route('/user-reg', methods=['POST','GET'])
def user_registration():
    username = request.form['username']
    email = request.form['email']
    password = (request.form['password']).encode('utf-8')
    hashed_password = generate_password_hash(password)

    with sqlite3.connect('todo.db') as c:
        cur = c.cursor()
        cur.execute('INSERT INTO users (username, email, hashed_password) VALUES (?, ?, ?)', (username, email, hashed_password))
        c.commit()
        resp = "User registration successful"
    return jsonify({"response" : resp})

@app.route('/user-login', methods=['POST', 'GET'])
def user_login():
    email = request.form['email']
    password = request.form['password']

    with sqlite3.connect('todo.db') as c:
        cur = c.cursor()
        cur.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cur.fetchone()
        if user and check_password_hash(user[3], password): 
            access_token = create_access_token(identity={"id": user[0], "username": user[1], "email": user[2]}) 
            return jsonify(access_token)
        else:
            return jsonify({"response" : "Invalid credentials!"})
    

@app.route('/add-task', methods=['POST', 'GET'])
@jwt_required()
def add_task():
    if request.method == 'POST':
        user_id = get_jwt_identity()['id']
        task = request.form['task']
        with sqlite3.connect('todo.db') as c:
            cur = c.cursor()
            cur.execute("INSERT INTO tasks (task, user_id) VALUES (?, ?)", (task, user_id))
            c.commit()
            resp = "Task added to database"
        return jsonify({"response" : resp})
    

@app.route('/remove-task', methods=['POST', 'GET'])
@jwt_required()
def remove_task():
    if request.method == 'POST':
        id = request.form['id']                         # id means task_id
        with sqlite3.connect('todo.db') as c:
            cur = c.cursor()
            cur.execute("DELETE FROM tasks WHERE id = ?", (id,))
            c.commit()
            resp = "Task deleted from database"
        return jsonify({"response" : resp})


@app.route('/update-task', methods=['POST', 'GET'])
@jwt_required()
def update_task():
    if request.method == 'POST':
        user_id = get_jwt_identity()['id']
        id = request.form['id']
        task = request.form['task']
        status = request.form['status']
        with sqlite3.connect('todo.db') as c:
            cur = c.cursor()
            cur.execute("SELECT * FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id)) 
            if cur.fetchone():
                cur.execute("UPDATE tasks SET task = ?, status = ? WHERE id = ?", (task, status, id))
                c.commit()
                resp = "Task data updated"
                return jsonify({"response" : resp})
            else:
                return jsonify({"response": "Unauthorized"})
    

if __name__ == '__main__' :
    app.run(debug=True)