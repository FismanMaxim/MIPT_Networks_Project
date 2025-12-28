from passlib.hash import bcrypt
from db import insert_user, find_user_by_login


def register_user(login, password, nickname):
    if not login or not password or not nickname:
        return None, "All fields are required"

    if find_user_by_login(login):
        return None, "User already exists"

    password_hash = bcrypt.hash(password)
    insert_user(login, password_hash, nickname)

    user = find_user_by_login(login)
    return user, None


def authenticate_user(login, password):
    user = find_user_by_login(login)
    if not user:
        return None, "Invalid login or password"

    if not bcrypt.verify(password, user["password_hash"]):
        return None, "Invalid login or password"

    return user, None
