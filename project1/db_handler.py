from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import IntegrityError
from password_handler import get_hash


class NoSuchUserError(Exception):
    pass

class WrongPasswordError(Exception):
    pass

class DBHandler():

    def __init__(self, db_url):
        engine = create_engine(db_url)
        self.db = scoped_session(sessionmaker(bind=engine))
    
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