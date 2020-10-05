from flask import Flask, render_template, request, g
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

def create_conn(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def insert_users(conn, insert_user):
    sql = ''' INSERT INTO users(username, email, password) VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, insert_user)
    conn.commit()
    return cur.lastrowid

def find_users(conn, auth_user):
    sql = ''' SELECT * users WHERE username = ? AND password = ? '''
    cur = conn.cursor()
    cur.execute(sql, auth_user)
    conn.commit()
    return cur.lastrowid

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

    database = r"/home/lumina/backend/projects/project2/twitter.db"

    conn = create_conn(database)
    with conn:
        insert_user = (username, email, password)
        insert_users(conn, insert_user)

    return render_template("home.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def authenticateUser():
    username = request.form['username']
    password = request.form['password']

    database = r"/home/lumina/backend/projects/project2/twitter.db"

    conn = create_conn(database)
    with conn:
        auth_login = (username, password)
        if find_users(conn, auth_login):
            login = True
        else:
            login - False

    if login == True:
        return render_template("home.html")
    else:
        return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)