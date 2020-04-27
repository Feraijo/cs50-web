import os

from flask import Flask, session, render_template, request, jsonify
from flask_session import Session
from db_handler import DBHandler
from goodreadapi import get_book_data

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

@app.route("/api/<string:isbn>")
def book_api(isbn):
    """Return details in json format about single book"""

    book, message = dbh.get_book_by_isbn(isbn)
    if message:
        return jsonify({"error": "Invalid isbn"}), 404
    goodreads = get_book_data(isbn)
    return jsonify({
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "isbn": isbn,
        "review_count": goodreads['reviews_count'],
        "average_score": goodreads['average_rating'],
    })
        

@app.route("/")
def index():
    """Return index page"""

    purpose = request.args.get('to')
    if purpose == 'logout' or session.get("user") is None:
        session["user"] = False       
    return render_template("index.html", user=session["user"])

@app.route("/<int:book_id>")
def book(book_id):
    """Return details about single book"""

    book, message = dbh.get_book(book_id)
    reviews = dbh.get_book_reviews(book_id)    
    if not book:
        return render_template("index.html", user=session["user"], message=message)
    goodreads = get_book_data(book.isbn)
    return render_template("book.html", user=session["user"], book=book, reviews=reviews, goodreads=goodreads)

@app.route("/<int:book_id>/review", methods=['GET', 'POST'])
def review(book_id):
    """Process review form"""

    book, message = dbh.get_book(book_id)
    if request.method == 'GET':
        return render_template("review.html", user=session["user"], book=book)
    else:        
        review_text = request.form.get("review_text") or None
        score = request.form.get("score") or None
        message = dbh.add_review(book_id, score, review_text, session["user"])
        reviews = dbh.get_book_reviews(book_id)
        return render_template("book.html", user=session["user"], book=book, reviews=reviews, message=message)    

@app.route("/search", methods=['POST'])
def search():
    """Process search values at index"""

    isbn = request.form.get("isbn") or None
    title = request.form.get("title") or None
    author = request.form.get("author") or None    
    year = request.form.get("year")
    year = int(year) if year else None    
    books, response = dbh.find_books(isbn, title, author, year)    
    return render_template("index.html", user=session["user"], books=books, message=response)

@app.route("/login_url", methods=['GET', 'POST'])
def login_form():
    """Process login and registration pages"""

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
            session["user"], message, good_res = dbh.check_user(login, pwd)
            if good_res:
                return render_template("index.html", user=session["user"], message=message)
            else:
                return render_template("login_form.html", purpose=purpose, message=message)
        else:
            # if it is registration - check if login already exists and register otherwise
            name = request.form.get("name") or login
            message, good_res = dbh.add_user(name, login, pwd)
            if good_res:
                purpose = 'login'
            return render_template("login_form.html", purpose=purpose, message=message)            
