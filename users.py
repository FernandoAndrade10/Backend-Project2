from flask import Flask, render_template, request, g
import sqlite3

DATABASE = '/home/lumina/backend/projects/project2/twitter.db'

app = Flask(__name__)

def get_db():
    db = getattr(g, '_twitter', None)
    if db is None:
        db = g._twitter = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_twitter', None)
    if db is not None:
        db.close()


@app.route('/')
def main():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def createUser():
    # username = request.form['username']
    # email = request.form['email']
    # password = request.form['password']

    # query_db('INSERT INTO users (username, email, password) values(?,?,?)',(username,email,password))

    # return render_template("index.html")
    if request.method == 'POST':
        try:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']

            # with sql.connect("twitter.db") as con:
            #     cur = con.cursor()
            #     cur.execute("INSERT INTO users (username, email, password) VALUES (?,?,?,?", (username, email, password) )
            #     con.commit()
            query_db('INSERT INTO users (username, email, password) values(?,?,?)',(username,email,password))

            msg = "Added"

        except:
            msg = "error"

        finally:
            return render_template("result.html",msg = msg)


if __name__ == "__main__":
    app.run(debug=True)