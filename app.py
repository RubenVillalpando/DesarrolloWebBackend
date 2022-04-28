from ast import AsyncFunctionDef
from datetime import datetime
from tkinter import E
from unicodedata import name
from flask import Flask, render_template, request, session, redirect, url_for
import datetime
import pymongo
import urllib

# FlASK
#############################################################
app = Flask(__name__)
app.permanent_session_lifetime = datetime.timedelta(days=365)
app.secret_key = "lfkjsiofjw3Rw3iof89y9)(Y)(iowfsofja"
#############################################################

# FlASK
#############################################################
mongodb_key = "mongodb+srv://a01376331:" + urllib.parse.quote_plus("K8up3VaSi9NBJ@5") + "@cluster0.sgyqc.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
# mongodb_key = "mongodb+srv://desarrollowebuser:desarrollowebpassword@cluster0.dfh7g.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = pymongo.MongoClient(mongodb_key, tls=True, tlsAllowInvalidCertificates=True)
db = client.WebProjectDB
usersTable = db.Users
#############################################################


@app.route('/')
def home():
    if "email" in session:
        email = session["email"]
        return render_template('index.html', data=email)
    else:
        return render_template('Login.html', data=None) 


@app.route('/signup', methods=["GET", "POST"])
def signup():
    try:
        name = request.form["name"]
        email = request.form["email"]
        pswd = request.form["pswd"]
    except:
        print("error recieving the form attributes")
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


@app.route("/insert", methods=["POST"])
def insertUsers():
    user={
        "matricula":"A01376331",
        "nombre":"Rubén Villalpando Bremont",
        "correo":"rubenV@tex.mx",
        "contrasenia":"asfdjoijr283r9j"
    }
    try:
        usersTable.insert_one(user)
        return redirect(url_for("users"))
    except Exception as e:
        return "<p>El servicio no está disponible %s %s" % type(e),e

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
        return redirect(url_for("usuarios"))
    except Exception as e:
        return "error" + e 


@app.route('/create')
def create():
    return render_template('Create.html')
