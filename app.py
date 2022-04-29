from datetime import datetime
from unicodedata import name
from flask import Flask, render_template, request, session, redirect, url_for
import datetime
import pymongo
from decouple import config
from urllib.parse import quote_plus
from twilio.rest import Client

# FlASK
#############################################################
app = Flask(__name__)
app.permanent_session_lifetime = datetime.timedelta(days=365)
app.secret_key = "lfkjsiofjw3Rw3iof89y9)(Y)(iowfsofja"
#############################################################

# MONGODB
#############################################################
mongodb_key = config("mongodb_key")
client = pymongo.MongoClient(mongodb_key, tls=True, tlsAllowInvalidCertificates=True)
db = client.WebProjectDB
usersTable = db.Users
#############################################################

# Twilio
#############################################################
account_sid = config('account_sid')
auth_token = config('auth_token')
TwilioClient = Client(account_sid, auth_token)
#############################################################

@app.route('/')
def home():
    if "email" in session:
        email = session["email"]
        return render_template('index.html', data=email)
    else:
        return render_template('Login.html', data=None) 


@app.route('/signup', methods=["POST"])
def signup():
    try:
        name = request.form["name"]
        email = request.form["email"]
        pswd = request.form["pswd"]
    except:
        print("error recieving the form attributes")
        return redirect(url_for("/login"))
    try:
        if not usersTable.find_one(
            {"email": (email),
            "pswd": (pswd)}
                ):
            try:
                usersTable.insert_one({
                    "name": (name),
                    "email": (email),
                    "pswd": (pswd),
                })
                print("hasta aqui todo ok parte uno")
                comogusten = TwilioClient.messages.create(
                    from_="whatsapp:+14155238886",
                    body="El usuario %s se agregó a tu pagina web" % (name),
                    to="whatsapp:+5215534330756"
                )
                print("hasta aqui todo ok parte dos")
                return render_template('index.html')
            except Exception as e:
                return "<h1>There was an error signing up :( ----Error = %s</h1>" % e
        return render_template('index.html')
    except Exception as e:
        return "<h1>There was an error accesing the database up :( ----Error = %s</h1>" % e
    


@app.route("/login", methods=["GET", "POST"])
def login():
    email = request.form["email"]
    pswd = request.form["pswd"]
    try:
        if usersTable.find_one({"email": (email),
                                "pswd": (pswd)}):
            if "email" not in session:
                if request.method == "GET":
                    return render_template("Login.html", data = "email")
                if request.method == "POST":
                    email = request.form["email"]
                    password = request.form["pswd"]
                    return render_template("index.html", data=email)
            else: 
                return render_template("Login.html", data=session["email"])
        else:
            return "<h1>email o contraseña inválidos</h1>"
    except Exception as e: 
        return "<h1>There was an error accesing the database up :( ----Error = %s</h1>" % e
    
        

@app.route('/logout')
def logout():
    if "email" in session:
        session.clear()
    return redirect(url_for('home'))
    

@app.route('/users')
def users():
    cursor = usersTable.find({})
    users = []
    for doc in cursor:
        users.append(doc)
    return render_template("/users.html", data=users)

@app.route("/find_one/<matricula>")
def find_one(matricula):
    try:
        user = usersTable.find_one({"matricula": (matricula)})
        if user != None:
            return "<p>Encontramos: %s</p>" % (user)
        return "<p>La matrícula %s no existe" %matricula
    except Exception as e:
        return e 

@app.route("/delete_one/<matricula>")
def delete_one(matricula):
    try:
        user = usersTable.delete_one({"matricula": (matricula)})
        if user.deleted_count == None:
            return "<p>La matricula %s nó existe</p>" % (matricula)
        else:
            return redirect(url_for("users"))
    except Exception as e:
        return "%s" % e

@app.route("/update", methods=["POST"])
def update():
    try:
        filter = {"matricula":request.form["matricula"]}
        user={"$set": {
            "nombre": request.form["nombre"]
        }}
        usersTable.update_one(filter, user)
        return redirect(url_for("users"))
    except Exception as e:
        return "error" + e 