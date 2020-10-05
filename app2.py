from flask import Flask, render_template, request, g, jsonify
import sqlite3
from sqlite3 import Error
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = "/home/lumina/backend/projects/project2/twitter.db"

app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def add_user(username, email, password):
    sql = "INSERT INTO users (username, email, password) VALUES(?, ?, ?);"
    db = get_db()
    db.execute(sql, (username, email, password))
    res = db.commit()
    return res

def login_user(username):
    sql = "SELECT * FROM users WHERE username = (?);"
    db = get_db()
    rv = db.execute(sql, (username,))
    res = rv.fetchall()
    rv.close()
    return res[0]

def retrieve_password(username):
    sql = "SELECT password FROM users WHERE username = (?);"
    db = get_db()
    rv = db.execute(sql, (username,))
    res = rv.fetchall()
    rv.close()
    return res[0]

@app.route('/')
def main():
    return render_template("home.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/register', methods=['POST'])
def createUser():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    hashed_password = generate_password_hash(password)

    add_user(username, email, hashed_password)

    return render_template("home.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def authenticateUser():
    username = request.form['username']
    password = request.form['password']

    password_in_db = retrieve_password(username)
    
    authPassword = check_password_hash(password_in_db, password)

    if authPassword == True:
        results = login_user(username)
        return jsonify(results)
    else:
        return render_template("fail.html")


if __name__ == "__main__":
    app.run(debug=True)