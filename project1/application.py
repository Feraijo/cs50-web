import os

from flask import Flask, session, render_template, request, flash
from flask_session import Session
from db_handler import *

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
dbh = DBHandler(os.getenv("DATABASE_URL"))


@app.route("/")
def index():
    purpose = request.args.get('to')
    if purpose == 'logout' or session.get("logged") is None:
        session["logged"] = False       
    return render_template("index.html", logged=session["logged"])

@app.route("/login_url", methods=['GET', 'POST'])
def login_form():
    # check if the purpose (registration or user login)
    purpose = request.args.get('to')

    # redirect to form if GET
    if request.method == 'GET':        
        return render_template("login_form.html", purpose=purpose)
    else:               
        # get the form values if POST
        login = request.form.get("login")
        pwd = request.form.get("pwd")    

        # if it is login - check user and password and log him in    
        if purpose == 'login':
            try:
                dbh.check_user(login, pwd)
                session["logged"] = True
                message = 'You\'ve successfully logged in.'
            except NoSuchUserError:
                message = 'No such user, please register'
            except WrongPasswordError:
                message = 'Wrong password, try again'
                
            return render_template("index.html", logged=session["logged"], message=message)
        else:
            # if it is registration - check if name already exists and register otherwise
            name = request.form.get("name")
            try:
                dbh.add_user(name, login, pwd)
            except IntegrityError:
                message = 'That username is already in use'
                return render_template("login_form.html", purpose=purpose, message=message)
            return render_template("login_form.html", purpose='login')

