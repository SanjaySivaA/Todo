import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)

c = sqlite3.connect('todo.db')
c.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT, status TEXT)')
c.close()

