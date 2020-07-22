from werkzeug.security import safe_str_cmp
from models.user import UserModel


def authenticate(username, password):
    """
    Function that gets called when a user calls the /auth endpoint
    with their username and password
    :param ussername|: user's username in string format
    :param password; USERS unencrypted password in string format
    return: A usermodel object if authentication was successful and none otherwise
    """
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password,password):
        return user

    
def identity(payload):
    """
    function that gets called when user has already authenticated
    and Flask-JWT verified their authentication header is correct
    ==param: payload: A dictionary with 'identity' key which is th user id
    ==return: a usermodel object
    """
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
