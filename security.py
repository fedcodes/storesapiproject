#this brings the user from the user file
from models.user import UserModel

#this authenticates the users to generate the JWT token, and looks for it in the database
def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user is not None and user.password == password:
        return user

#this takes in a payload, the JWT token, extract the user id and return it in order to retrieve the API info.
def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
