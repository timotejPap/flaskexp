import os
from flask import Flask, render_template, redirect, abort, request
from flask_wtf import FlaskForm, csrf
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# APP CONTEXT -- Nasa Flasa
app=Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(32)
app.config["CSFR_ENABLED"] = True  #

# Tu sa budu ukladat nase data
info_list = ["test1", "test20", "test3"]

# Formular
class MojFormular(FlaskForm):
    info = StringField("Info", validators=[DataRequired(message="Required")])
    submit = SubmitField("Submit")

# ROUTES
@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")
"""
@app.route("/info", methods=["GET", "POST"])
def info():
    if request.method == "POST":
        print(request.form.get("info"))
        info_list.append(request.form.get('info'))
        app.logger.info('INFO ULOZENA')
    form = MojFormular()
    app.logger.debug("Formular bol vytvoreny")
    return render_template("info.html", form=form)
"""
"""
# VERZIA 2
@app.route("/info", methods=["GET"])
def info_get():
    form = MojFormular()
    app.logger.debug("Formular bol vytvoreny")
    return render_template("info.html", form=form)

@app.route("/info", methods=["POST"])
def info_post():
    if request.method == "POST":
        print(request.form.get("info"))
        info_list.append("Info ulozena")
        return redirect("/submit")
"""
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
            info_list.append(request.form.get('info'))
            app.logger.debug("Sprava bola ulozena")
        return redirect("/submit")
    else:
        app.logger.info("INFORMACIA NEBOLA ULOZENA")

    return render_template("info.html", form=form)

@app.route("/submit", methods=["GET"])
def submit():
    return render_template("submit.html")

@app.route("/list", methods=["GET"])
def infolist():
    return render_template("list.html", entries=info_list)


if __name__ == "__main__":
    app.run(debug=True)