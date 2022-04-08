from flask import Flask, render_template, request

# FlASK
#############################################################
app = Flask(__name__)
#############################################################

@app.route('/')
def home():
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("Login.html", error = "email")
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["pswd"]
        return render_template("index.html", error=email)