from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import IntegrityError
import hashlib

def get_hash(s):
    return hashlib.sha256(s.encode()).hexdigest()

class NoSuchUserError(Exception):
    pass

class WrongPasswordError(Exception):
    pass

class DBHandler():

    def __init__(self, db_url):
        engine = create_engine(db_url)
        self.db = scoped_session(sessionmaker(bind=engine))
    
    def execute(self, *args, **kwargs):
        self.db.execute(*args, **kwargs)
    
    def commit(self):
        self.db.commit

    def add_user(self, name, login, pwd):
        self.db.execute("INSERT INTO users (user_name, login, pass) VALUES (:name, :login, :pwd)",
                {"name": name, "login": login, "pwd": get_hash(pwd)})        
        self.db.commit()            
    
    def check_user(self, login, pwd):        
        user = self.db.execute("SELECT * FROM users WHERE login = :login", {"login": login}).fetchone()
        if user is None:
            raise NoSuchUserError()
        if get_hash(pwd) != user[2]:
            raise WrongPasswordError()
        return

    def get_book(self, book_id):
        book = self.db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).fetchone()
        message = ''
        if not book:
            message = "No such book, try another"
        return book, message

    def get_book_reviews(self, book_id):
        return self.db.execute("SELECT * FROM reviews WHERE book_id = :book_id", {"book_id": book_id}).fetchall()        
        
    def find_books(self, isbn, title, author, year):
        locs = dict(locals())
        message = ''
        lst = []
        args = {}
        for k, v in locs.items():
            if k == 'self' or v is None:
                continue
            if isinstance(v, int) or isinstance(v, float) or isinstance(v, bool):
                lst.append(f'{k} = :{k}')
                args[k] = v            
            else:
                lst.append(f'lower({k}) like :{k.lower()}')
                args[k] = f'%{v}%'            
        vs = ' AND '.join(lst)
        if not args:
            return self.db.execute(f"SELECT * FROM books LIMIT 10").fetchall(), \
                    'First 10 books, because no search parameters provided'
        res = self.db.execute(f"SELECT * FROM books WHERE {vs}", args).fetchall()
        if not res:
            message = '0 books found with these criteria'
        return res, message


if __name__ == "__main__":
    import os
    dbh = DBHandler(os.getenv("DATABASE_URL"))
    print(dbh.find_books(None, 'night', None, None))
