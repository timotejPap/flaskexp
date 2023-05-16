from flask import Flask, render_template, abort, redirect, request
import datetime

app = Flask(__name__)
BUFFER = list()


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html"), 500


# Routes
@app.route("/")
@app.route("/index")
def main():
    return "<h1>Ahoj ja som dzin z Flasku</h1>"

@app.route("/mojastranka")
def moja():
    return "<h2>Test mojej stranky</h2><br><p>Toto je moja skusobna stranka WEB</p>"
@app.route("/vitajte")
def welcome():
    return render_template("vitajte.html")  # po slovensky

@app.route("/welcome")
def vitajte():
    return redirect("/vitajte")

@app.route("/cas")
def cas():
    return render_template("main.html", cas=datetime.datetime.now())

@app.route("/spravy/<int:index>", methods=["GET"])
def spravy(index):
    spravy = ["sprava1 - zlacnelo mydlo", "sprava2 - zajtra bude pekne", "sprava3 - Hotovo"]
    try:
        return render_template("spravy.html", msg=spravy[index])
    except IndexError:
        abort(404)

@app.route("/kurzkk", methods=["GET"])
def kurz():
    kurz = [12, 34, 23, 78, 45, -5, -76, 15, 36, 89]
    return render_template("kurzkk.html", kurzy=kurz)

@app.route("/form", methods=["GET", "POST"])
def form():
    print(request)
    if request.method == "POST":
        user = request.form.get("user")
        pwd = request.form.get("pwd")
        print(user, pwd)
        BUFFER.append((user,pwd))  # pridavame TUPLE
        app.logger.info("USPECH - Vysledok formulara bol ulozeny do BUFFERU")

    return render_template("form.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)

# Development -> DevOps -> Produkcny server <- User
# --> v.3      --> v.2.5         v.1.8