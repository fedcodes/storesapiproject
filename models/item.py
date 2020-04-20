from db import db

class ItemModel(db.Model):

#This creates the table for  the items model and sets the columns.
    __tablename__='items'
    id= db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    #This brings the stores id from the the stores model. The foreign key defines it as the lookup column to the other table.
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

    #This method permits other methods to find items by their name.
    @classmethod
    def find_by_name(cls, name):
        #SQLAlchemy query to filter by name, and returns the first value - SELECT * FROM items WHERE name=name LIMIT 1
        return cls.query.filter_by(name=name).first()

    #Method of SQLAlchemy to add or update files to database.
    def save_to_db(self):
        #adding the self object to the database through SQLAlchemy.
        db.session.add(self)
        db.session.commit()

    #Method to delete items from database
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
