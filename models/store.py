from db import db

class StoreModel(db.Model):

#This creates the table for  the items model and sets the columns.
    __tablename__='stores'
    id= db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    #Relationship to the items. With the lazy method it will only look for the items when the json method is called. 
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]} #This returns the list of items in the store.

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
