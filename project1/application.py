import os

from flask import Flask, session, render_template, request, flash
from flask_session import Session
from db_handler import DBHandler, NoSuchUserError, WrongPasswordError, IntegrityError

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

# index page
@app.route("/")
def index():
    purpose = request.args.get('to')
    if purpose == 'logout' or session.get("user") is None:
        session["user"] = False       
    return render_template("index.html", user=session["user"])

# book page
@app.route("/<int:book_id>")
def book(book_id):
    book, message = dbh.get_book(book_id)
    reviews = dbh.get_book_reviews(book_id)
    if not book:
        return render_template("index.html", user=session["user"], message=message)
    return render_template("book.html", user=session["user"], book=book, reviews=reviews)

# process search values
@app.route("/<int:book_id>/review", methods=['GET', 'POST'])
def review(book_id):
    book, message = dbh.get_book(book_id)
    if request.method == 'GET':
        return render_template("review.html", user=session["user"], book=book)
    else:        
        review_text = request.form.get("review_text") or None
        score = request.form.get("score") or None
        message = dbh.add_review(book_id, score, review_text, session["user"])
        reviews = dbh.get_book_reviews(book_id)
        return render_template("book.html", user=session["user"], book=book, reviews=reviews, message=message)    

# process search values
@app.route("/search", methods=['POST'])
def search():
    isbn = request.form.get("isbn") or None
    title = request.form.get("title") or None
    author = request.form.get("author") or None    
    year = request.form.get("year")
    year = int(year) if year else None    
    books, response = dbh.find_books(isbn, title, author, year)    
    return render_template("index.html", user=session["user"], books=books, message=response)

# login and registration page
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
                session["user"] = dbh.check_user(login, pwd)
                message = 'You\'ve successfully logged in.'
            except NoSuchUserError:
                message = 'No such user, please register'
            except WrongPasswordError:
                message = 'Wrong password, try again'
                
            return render_template("index.html", user=session["user"], message=message)
        else:
            # if it is registration - check if login already exists and register otherwise
            name = request.form.get("name") or login            
            try:
                dbh.add_user(name, login, pwd)
            except IntegrityError:
                message = 'That login is already in use'
                return render_template("login_form.html", purpose=purpose, message=message)
            return render_template("login_form.html", purpose='login')
