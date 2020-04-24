import csv
import os
from db_handler import DBHandler

dbh = DBHandler(os.getenv("DATABASE_URL"))

def main():
    with open("books.csv") as f:
        reader = csv.reader(f)
        start = True
        for isbn, title, author, year in reader:
            if start:
                start = False
                continue
            dbh.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                        {"isbn": isbn, "title": title, "author": author, "year":year})
        dbh.commit()

if __name__ == "__main__":
    main()
