from flask import Flask, render_template, abort
from blueprints.admin import routes
from flask_wtf import FlaskForm, csrf
from blueprints.admin.routes import admin_bp
from blueprints.auth.auth import auth

app = Flask(__name__)

# registracia blueprintu admin
app.register_blueprint(admin_bp)
app.register_blueprint(auth)

@app.route('/')
@app.route('/index')
def index():
    return render_template('main.html')

if __name__ == "__main__":
    app.run(debug=True)