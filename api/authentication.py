from werkzeug.security import check_password_hash
from flask import abort, jsonify, request
from functools import wraps
from manager.users import get_user_by_user_id, get_user_by_username
import base64


def user_verifying():
    request_auth = request.headers.get("Authorization")
    if request_auth is None:
        print("You need to send username and password as header!")
        abort(401)
        exit(0)
    request_auth = request_auth.split(" ")[1]
    encoded_auth_username = str(base64.b64decode(request_auth).decode("UTF-8")).split(":")[0]
    user = get_user_by_username(encoded_auth_username)
    verified_user_id = user.user_id
    return verified_user_id


def is_admin(user_id):
    if user_id is None:
        user = get_user_by_user_id(user_verifying())
        if user.role_id == 2:
            return True
        else:
            return False
    else:
        user = get_user_by_user_id(user_id)
        if user.role_id == 2:
            return True
        else:
            return False


def login_required(f):
    @wraps(f)
    def login(*args, **kwargs):
        request_auth = request.headers.get("Authorization")
        if request_auth is None:
            print("You need to send username and password as header!")
            abort(401)
            exit(0)
        request_auth = request_auth.split(" ")[1]
        encoded_auth_username, encoded_auth_password = str(base64.b64decode(request_auth).decode("UTF-8")).split(":")
        user = get_user_by_username(encoded_auth_username)
        if user:
            if check_password_hash(user.password_hash, encoded_auth_password):
                return f(*args, **kwargs)
            else:
                return jsonify("Wrong username or password")
        else:
            return jsonify("Please login.")

    return login
