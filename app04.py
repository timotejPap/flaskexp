# heslo na server: oKOSTUJ_uD4N4_t0FU
import json
import os
from flask import Flask, render_template, redirect, abort, request, session, flash
from flask_wtf import FlaskForm, csrf
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_session import Session
import sqlite3
import json

# SQLAlchemy - tabulky, sqlite, mariadb -

# redis -

# mongodb - dokumenty

# APP CONTEXT -- Nasa Flasa
app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(32)
app.config["CSRF_ENABLED"] = True  #

app.config["SESSION TYPE"] = "filesystem"  # tu sa dava adresa serveru
app.config["SESSION_PERMANENT"] = False
Session(app)


# Tu sa budu ukladat nase data
info_list = ["test1", "test20", "test3"]

# FORMULAR
class MojFormular(FlaskForm):
    info = StringField("Info", validators=[DataRequired(message="Required")])
    submit = SubmitField("Submit")

DATABASE = "appdb.db"

def add_record(info):
    with sqlite3.connect(DATABASE) as db:
        cur = db.cursor()
        sql_cmd = "INSERT INTO info VALUES(?,?)"
        data = (1, info)
        cur.execute(sql_cmd, data)
        db.commit()
        return True

# ROUTES
@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/setsession")
def setsession():
    session["USERNAME"] = "Anonymous"
    flash("USERNAME JE NASTAVENE")
    app.logger.debug("USERNAME JE NASTAVENE")
    return redirect("index")

@app.route("/getsession")
def getsession():
    if "USERNAME" in session:
        username = session["USERNAME"]
        msg = f"SESSION FOR USER : {username} WAS ACCESSED"
        flash(msg)
        app.logger.info(msg)
        return redirect("/index")
    else:
        return "<h1>WELCOME GUEST</h1>"

@app.route("/delsession")
def delsession():
    session.pop("USERNAME", None)
    flash("SESSION BOLA VYMAZANA")
    app.logger.debug("SESSION BOLA VYMAZANA")
    return redirect("/index")

@app.route("/info", methods=["GET", "POST"])
def info():
    form = MojFormular()
    app.logger.debug("Formular bol vytvoreny")
    if request.method == "POST":
        csrf.generate_csrf()
        app.logger.debug("Sprava prisla")
        #if request.form.get("info") != "":
        if form.validate():
            print(request.form.get("info"))
            #info_list.append(request.form.get('info'))
            session["info"] = request.form["info"]  # tu sa nacita z formulara info
            with open(file="session_info.json", mode="a", encoding="utf8") as f:
                json.dump(fp=f, obj=session, indent=4)
            add_record(session["info"])
            app.logger.debug("Sprava bola ulozena")
        return redirect("/submit")
    else:
        app.logger.info("INFORMACIA NEBOLA ULOZENA")
    return render_template("info.html", form=form)

@app.route("/submit", methods=["GET"])
def submit():
    return render_template("submit.html")

@app.route("/view", methods=["GET"])
def infolist():
    try:
        entry = str(session["info"])
        app.logger("SPRAVA")
        flash("Info je v poriadku")
    except KeyError:
        entry = None
        flash("NEMAM INFO")
    finally:
        return render_template("view.html", entry=entry)


if __name__ == "__main__":
    app.run(debug=True)