import hashlib
import functools

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import IntegrityError


def autocommit(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):        
        value = func(*args, **kwargs)
        args[0].db.commit()
        return value
    return wrapper_decorator

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

    @autocommit
    def add_user(self, name, login, pwd):
        self.db.execute("""
            INSERT INTO users (user_name, login, pass) 
            VALUES (:name, :login, :pwd)
            """, {"name": name, "login": login, "pwd": get_hash(pwd)})
    
    @autocommit
    def check_user(self, login, pwd):        
        user = self.db.execute("""
            SELECT *
            FROM users 
            WHERE login = :login
            """, {"login": login}).fetchone()
        if user is None:
            raise NoSuchUserError()
        if get_hash(pwd) != user[2]:
            raise WrongPasswordError()               
        return user

    @autocommit
    def get_book(self, book_id):
        book = self.db.execute("""
            SELECT * 
            FROM books 
            WHERE id = :id
            """, {"id": book_id}).fetchone()
        message = ''
        if not book:
            message = "No such book, try another"
        return book, message

    @autocommit
    def get_book_reviews(self, book_id):
        return self.db.execute("""
            SELECT user_name, review_text, score, date
            FROM public.reviews r
            JOIN public.users u
            ON u.id = r.user_id
            WHERE book_id = :book_id
            """, {"book_id": book_id}).fetchall()        

    @autocommit
    def add_review(self, book_id, score, review_text, user):
        try:
            self.db.execute("""
                INSERT INTO public.reviews
                (book_id, user_id, review_text, score)
                VALUES(:book_id, :user, :review_text, :score)
                """, {"book_id": book_id, "user": user.id, 
                    "review_text": review_text, "score": score})  
            message = "Review added successfully."  
        except IntegrityError:
            message = "You've already wrote a review for this book! "
        return message

    @autocommit
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
            return self.db.execute("""
                SELECT * 
                FROM books 
                LIMIT 10
                """).fetchall(), 'First 10 books, because no search parameters provided'            
        res = self.db.execute(f"""
        SELECT * 
        FROM books 
        WHERE {vs}
        """, args).fetchall()        
        if not res:
            message = '0 books found with these criteria'
        return res, message


if __name__ == "__main__":
    import os
    dbh = DBHandler(os.getenv("DATABASE_URL"))
    print(dbh.find_books(None, 'night', None, None))
