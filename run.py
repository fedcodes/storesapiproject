from app import app
from db import db

db.init_app(app)

#This creates the table
@app.before_first_request
def create_tables():
    db.create_all()
