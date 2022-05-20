from werkzeug.security import check_password_hash, generate_password_hash 
from db import db

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, _id: int, _username: str, _password: str) -> None:
        self.id = _id
        self.username = _username
        self.password = self.crate_hash(_password)
    
    @classmethod
    def check_password(cls, hashed_password: str, password: str) -> bool:
        '''
        This method is used to check if the password match with the hashed storage.
        '''
        return check_password_hash(hashed_password, password)

    def crate_hash(self, password: str) -> str:
        '''
        This method is used to create a hash for the password.
        '''
        hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
        return hash

    @classmethod
    def find_by_id(cls, id) -> object:
        '''
        This method is used to find a user by id.
        '''
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_username(cls, name) -> object:
        '''
        This method is used to find a user by name.
        '''
        return cls.query.filter_by(username=name).first()

    @classmethod
    def find_all(cls) -> list:
        '''
        This method is used to find all users.
        '''
        return cls.query.all()


    def save_to_db(self) -> dict:
        '''
        This method is used to insert or update a user into the database.
        '''
        db.session.add(self)
        db.session.commit()
        
    @classmethod
    def delete(cls, name) -> None:
        '''
        This method is used to delete a user.
        '''
        cls.query.filter_by(username=name).delete()
        db.session.commit()
    