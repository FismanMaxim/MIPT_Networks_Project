from flask import Flask, request, jsonify
from config import API_PREFIX
from auth import register_user, authenticate_user
from jwt_utils import create_token, verify_token

app = Flask(__name__)

@app.route(API_PREFIX + "/register", methods=["POST"])
def register():
    data = request.json or {}
    login = data.get("login")
    password = data.get("password")
    nickname = data.get("nickname")

    user, error = register_user(login, password, nickname)
    if error:
        return jsonify({"error": error}), 400

    token = create_token(user["id"], user["login"], user["nickname"])
    return jsonify({
        "token": token,
        "user": {
            "id": user["id"],
            "login": user["login"],
            "nickname": user["nickname"]
        }
    })


@app.route(API_PREFIX + "/login", methods=["POST"])
def login():
    data = request.json or {}
    login = data.get("login")
    password = data.get("password")

    user, error = authenticate_user(login, password)
    if error:
        return jsonify({"error": error}), 400

    token = create_token(user["id"], user["login"], user["nickname"])
    return jsonify({
        "token": token,
        "user": {
            "id": user["id"],
            "login": user["login"],
            "nickname": user["nickname"]
        }
    })


@app.route(API_PREFIX + "/verify", methods=["POST"])
def verify():
    data = request.json or {}
    token = data.get("token")
    if not token:
        return jsonify({"valid": False}), 400

    payload = verify_token(token)
    if not payload:
        return jsonify({"valid": False}), 401

    return jsonify({"valid": True, "payload": payload})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
