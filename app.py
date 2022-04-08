from datetime import datetime
from unicodedata import name
from flask import Flask, render_template, request, session, redirect, url_for
import datetime
# FlASK
#############################################################
app = Flask(__name__)
app.permanent_session_lifetime = datetime.timedelta(days=365)
app.secret_key = "lfkjsiofjw3Rw3iof89y9)(Y)(iowfsofja"
#############################################################

@app.route('/')
def home():
    if "email" in session:
        email = session["email"]
        return render_template('index.html', data=email)
    else:
        return render_template('Login.html', data=None) 


@app.route('/signup')
def signup():
    name = request.form["name"]
    email = request.form["email"]
    pswd = request.form["pswd"]
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if "email" not in session:
        if request.method == "GET":
            return render_template("Login.html", data = "email")
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["pswd"]
            return render_template("index.html", data=email)
    else: 
        return render_template("Login.html", data=session["email"])


@app.route('/logout')
def logout():
    if "email" in session:
        session.clear()
    return redirect(url_for('home'))
    
