import base64
import hashlib
import hmac
import calendar
import datetime
import jwt

from flask import current_app, request, abort

from project.exceptions import ItemNotFound


def generate_password_digest(password):
    return base64.b64encode(hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"],
    ))


def auth_check():
    if 'Authorization' not in request.headers:
        return False
    token = request.headers['Authorization'].split("Bearer ")[-1]
    return jwt_decode(token)


def jwt_decode(token):
    try:
        decoded_jwt = jwt.decode(token, current_app.config["SECRET_KEY"], current_app.config["JWT_ALGORITHM"])
    except:
        return False
    else:
        return decoded_jwt


def auth_required(func):
    def wrapper(*args, **kwargs):
        if auth_check():
            return func(*args, **kwargs)
        abort(401, "Authorization error")
    return wrapper


def generate_token(data):
    min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    data["exp"] = calendar.timegm(min30.timetuple())
    access_token = jwt.encode(data, key=current_app.config["SECRET_KEY"], algorithm=current_app.config[
        "JWT_ALGORITHM"])
    days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
    data["exp"] = calendar.timegm(days130.timetuple())
    refresh_token = jwt.encode(data, key=current_app.config["SECRET_KEY"], algorithm=current_app.config[
        "JWT_ALGORITHM"])
    return {'access_token': access_token, 'refresh_token': refresh_token}


def compare_passwords(password_hash, user_pass) -> bool:
    return hmac.compare_digest(
        base64.b64decode(password_hash),
        hashlib.pbkdf2_hmac('sha256', user_pass.encode('utf-8'), current_app.config["PWD_HASH_SALT"],
                            current_app.config["PWD_HASH_ITERATIONS"]))


def login_user(req_json, user):
    user_email = req_json.get("email")
    user_pass = req_json.get("password")
    if user_email and user_pass:
        pass_hashed = user["password"]
        req_json["email"] = user["email"]
        if compare_passwords(pass_hashed, user_pass):
            return generate_token(req_json)
        return ItemNotFound


def refresh_user_token(req_json):
    refresh_token = req_json.get("refresh_token")
    data = jwt_decode(refresh_token)
    if data:
        tokens = generate_token(data)
        return tokens
    return ItemNotFound
