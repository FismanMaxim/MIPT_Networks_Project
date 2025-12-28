import time
import jwt
from config import JWT_SECRET, JWT_ALGO


def create_token(user_id, login, nickname):
    payload = {
        "user_id": user_id,
        "login": login,
        "nickname": nickname,
        "exp": int(time.time()) + 3600
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)


def verify_token(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
