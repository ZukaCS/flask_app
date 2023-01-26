import os
import sqlite3
from datetime import date
from tempfile import mkdtemp

import requests
from flask import (Flask, current_app, flash, jsonify, make_response, redirect,
                   render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from email.message import EmailMessage
import ssl
import smtplib
from flask_session import Session

#connect to database
conn = sqlite3.connect('static/database.db', check_same_thread=False)
print("opened successfully")

#configure email
email_sender = 'bugscountryinfo@gmail.com'
email_password = 'zazsazegqycndlom'
email_receiver = 'zukakekelidze4@gmail.com'


app = Flask(__name__)
app.secret_key = 'aaccssdd321'
app.config["TEMPLATES_AUTO_RELOAD"] = True

#configure cookies
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


headers = {
	"X-RapidAPI-Key": "8451bff402msh94c0c09e88de1a8p11369ejsn97e8c47c557a",
	"X-RapidAPI-Host": "ajayakv-rest-countries-v1.p.rapidapi.com"
}

url = "https://restcountries.com/v3.1/all"


response = requests.request("GET", url, headers=headers)
country_index = {}
i = 0
countries = set()
DATA = response.json()
for index in DATA:
    country_index[index["name"]["common"]]=i
    countries.add(index["name"]["common"])
    i+=1
countries = sorted(countries)

@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html", countries=countries)


@app.route("/country", methods=["POST", "GET"])
def country():
    if request.method == "GET":
        country = request.args.get("name").lower()
        if country not in [name.lower() for name in countries]:
            return render_template("error.html", error="Country named '" + country + "' does not exist")
        else:
            if "user_id" in session:
                inFavourites = conn.execute("SELECT id from favourites where person_id = ? and country = ?", (session["user_id"], country)).fetchone()
                print(country_index)
                country = country.title()
                return render_template("country.html", data=DATA[country_index[country]], inFavourites=inFavourites)
            else:
                country = country.title()
                return render_template("country.html", data=DATA[country_index[country]])


@app.route("/login", methods=["POST", "GET"])
def login():

    session.clear()

    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        print(request.form)
        username = request.form.get("username")
        password = request.form.get("pass")
        users_check = conn.execute("SELECT username from users where username=?", [username]).fetchone()
        if users_check:
            print(conn.execute("SELECT hash from users where username=?", [username]).fetchone()[0])
            valid = check_password_hash(conn.execute("SELECT hash from users where username=?", [username]).fetchone()[0], password)
            if valid:
                session["user_id"] = conn.execute("SELECT id from users where username=?", [username]).fetchone()[0]
                return ("Succesful login")
            else:
                return ("Username or password is incorrect")
        else:
            return ("Username or password is incorrect")


@app.route("/logOut")
def logout():
    session.clear()

    return redirect("/")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        print(request.form) 
        username = request.form.get('username')
        if len(conn.execute("SELECT username from users where username=?", [username]).fetchall()):
            return("Username already exists")
        else:
            hash = generate_password_hash(request.form.get('pass'))
            conn.execute("INSERT INTO users (username, hash) VALUES(?, ?)", (username, hash))
            conn.commit()
            print(conn.execute("SELECT * from users").fetchall())
            session["user_id"] = conn.execute("SELECT id from users where username=?",[username]).fetchone()[0]
            return ("Successful register")
    else:
        return render_template("register.html")
        

@app.route("/favourites", methods=["POST", "GET"])
def favourites():
    
    if request.method == "GET":
        if "user_id" not in session:
            return render_template("error.html", error="You need to be logged in to access favourites")
        else:
            print(conn.execute("SELECT country from favourites where person_id=?", (session["user_id"], )).fetchall())
            favourites = conn.execute("SELECT country from favourites where person_id=?", (session["user_id"], )).fetchall()
            countries = set()
            for item in favourites:
                countries.add(item[0])
            
            print(countries)
            DATAS = []
            for country in countries:
                DATAS.append({
                    "name":DATA[country_index[country]]["name"]["common"],
                    "flag":DATA[country_index[country]]["flags"]["png"]
                    })
            favouritesLength = len(DATAS)
            
            return render_template("favourites.html", DATAS=DATAS, favouritesLength=favouritesLength)

#add to favourites     
@app.route("/add", methods=["POST"])
def addFav():
    if request.method == "POST":
        country = request.form.get("country")
        if conn.execute("SELECT id from favourites where person_id = ? and country = ?", (session["user_id"], country)).fetchone():
            conn.execute("DELETE FROM favourites where id in (SELECT id from favourites where person_id = ? and country = ?)", (session["user_id"], country))
            conn.commit()
            return ("removed from favourites")
        conn.execute("INSERT INTO favourites (country, person_id) values(?, ?)", (country, session["user_id"]))
        conn.commit()
        return("success")

@app.route("/remove", methods=["POST"])
def remove():
    if request.method=="POST":
        country = request.form.get("country")
        conn.execute("DELETE FROM favourites where id in (SELECT id from favourites where person_id = ? and country = ?)", (session["user_id"], country))
        conn.commit()
        return ("removed from favourites")
    
@app.route("/reportpage", methods=[ "GET"])
def reportPage():
    if request.method == "GET":
        return render_template("bug.html")
    
@app.route("/reported", methods=["POST"])
def reported():
    if request.method == "POST":
        subject = request.form.get("subject")
        text = request.form.get("text")
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        if text == "" and subject == "":
            return "empty"
        if len(text) < 40:
            return "text less than 40 chars" 
        if len(subject) < 10:
            return "subject less than 10 chars"

        em['Subject'] = subject
        em.set_content(text)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
    return "success"
        
    
    
    
        

