from flask import Flask, render_template, request, session, redirect
import sqlite3
from sqlite3 import Error

DB_NAME = "smile.db"

app = Flask(__name__)


# creates a connection to the database
# inputs: database file
# outputs: the connection to the db or none.
def create_connection(db_file):
    """ create a connection to the sqlite db"""
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)

    return None


@app.route('/')
def render_homepage():
    return render_template("home.html")


@app.route('/menu')
@app.route('/menu/<products>')
def render_menu_page():
    con = create_connection(DB_NAME)

    query = "SELECT name, description, volume, price, image FROM product"

    cur = con.cursor()
    cur.execute(query)
    product_list = cur.fetchall()
    con.close()

    return render_template("menu.html", products=product_list)


@app.route('/contact')
def render_contact():
    return render_template("contact.html")


@app.route('/login')
def render_login():
    return render_template("login.html")


@app.route('/signup', methods=['GET', 'POST'])
def render_signup_page():
    if request.method == 'POST':
        print(request.form)
        fname = request.form.get('fname').strip().title()
        lname = request.form.get('lname').strip().title()
        email = request.form.get('email').strip().lower()
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if password != password2:
            return redirect('/signup?error=Passwords+dont+match')

        if len(password) < 8:
            return redirect('/signup?error=Password+must+be+8+characters+or+more')

        con = create_connection(DB_NAME)

        query = "INSERT INTO customer(id, fname, lname, email, password) VALUES(NULL,?,?,?,?)"

        cur = con.cursor()
        try:
            cur.execute(query, (fname, lname, email, password))
        except sqlite3.IntegrityError:
            return redirect('/signup?error=Email+is+already+taken')


        con.commit()
        con.close()
    return render_template("signup.html")



app.run(host="0.0.0.0")