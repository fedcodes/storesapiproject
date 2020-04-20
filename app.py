from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from db import db

#Header for every app
app = Flask(__name__)
#SQLAlchemy config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' #this tells it what kind of database it is.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#this creates the key to your app for a secure token.
app.secret_key = 'jose'
api = Api(app)


#this creates the JWT to authenticate. This endpoint is '/auth'
jwt = JWT(app, authenticate, identity)

#This means that the api can be accessed through the /item endpoint through the item resource
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(StoreList, '/stores')

#This prevents this to run only when you start the app, and not on import.
if __name__ == '__main__':
    db.init_app(app)
#This sets up the  port and sets up the debug code to troubleshoot problems.
    app.run(port=5000, debug=True)
