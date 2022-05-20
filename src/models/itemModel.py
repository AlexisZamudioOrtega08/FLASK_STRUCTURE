from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), unique=True, nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)

    def __init__(self, _id: int, _name: str, _price: float) -> None:
        self.id = _id
        self.name = _name
        self.price = _price
    
    def json(self) -> dict:
        '''
        This method is used to return a json representation of an item.
        '''
        return {'id': self.id, 'name': self.name, 'price': self.price}

    @classmethod
    def find_by_id(cls, id) -> object:
        '''
        This method is used to find an item by id.
        '''
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name) -> object:
        '''
        This method is used to find an item by its name.
        '''
        return cls.query.filter_by(name=name).first()
    
    @classmethod
    def find_all(cls) -> list:
        '''
        This method is used to find all items.
        '''
        return cls.query.all()

    def save_to_db(self) -> bool:
        '''
        This method is used to insert an item into the database.
        '''
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

    @classmethod
    def delete_from_db(cls, name) -> bool:
        '''
        This method is used to delete a user.
        '''
        try:
            cls.query.filter_by(name=name).delete()
            db.session.commit()
            return True
        except:
            return False