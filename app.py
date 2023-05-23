# heslo na server: oKOSTUJ_uD4N4_t0FU
import os
from flask import Flask, render_template, redirect, abort, request, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm, csrf, form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_session import Session
#import sqlite3
import json

# APP CONTEXT -- Nasa Flasa
app = Flask(__name__)

app.config["SECRET_KEY"] = os.urandom(32)
app.config["CSRF_ENABLED"] = True  # Cross Site Request Forgery
app.config["SECURITY_PASSWORD_HASH"] = "bcrypt"
app.config["SECURITY_PASSWORD_HASH"] = "bcrypt"


login_manager = LoginManager()
login_manager.init_app(app)

# MOCK
users = {"andrej@gmail.com": {"password":"halabala"}, "filip@gmail.com": {"password":"netusim"}}

class User(UserMixin):
    pass

# LOGIN MANAGER LOADER
@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return
    user = User()
    user.id = email
    return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get("email")
    if email not in users:
        return
    user = User()
    user.id = email
    return user

@app.route("/login", methods=(["GET", "POST"]))
def login():
    if request.method == "GET":
        return """
        <form action="login" method="POST">
        <input type="text" name="email" id="email" placeholder="email"
        <input type="password" name="password" id="password" placeholder="password"
        <input type="submit" name="submit"
        </form>
        """
    email = request.form["email"]
    if email in users and request.form["password"] == users["email"]["password"]:
        user = User()
        user.id = email
        login_user(user)
        return redirect(url_for("protected"))
    return "<h2>BAD LOGIN</h2>"

@app.route("/protected")
@login_required
def protected():
    return "nalogovany ako uzivatel" + current_user.id
@app.route("/logout")
def logout():
    logout.user()
    return "odhlaseny uzivatel"


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
        if form.validate():
            print(request.form.get("pwd"))
            #info_list.append(request.form.get('info'))
            session["info"] = request.form["info"]  # tu sa nacita z formulara info
            #with open(file="session_info.json", mode="a", encoding="utf8") as f:
                #json.dump(fp=f, obj=session, indent=4)
            #add_record(session["info"])
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