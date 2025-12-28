from flask import Flask, request, jsonify
from config import API_PREFIX
from chats import get_chats_for_user, get_messages, create_chat, leave_chat, send_message, add_member_to_chat
from jwt_utils import verify_token

app = Flask(__name__)

def auth_required(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        user = verify_token(token)
        if not user:
            return jsonify({"error": "Unauthorized"}), 401
        # Log the decoded token
        app.logger.info(f"Decoded token for user: {user}")
        return f(user, *args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@app.route(API_PREFIX + "/", methods=["GET"])
@auth_required
def chats_list(user):
    chats = get_chats_for_user(user["user_id"])
    return jsonify(chats)

@app.route(API_PREFIX + "/<int:chat_id>", methods=["GET"])
@auth_required
def chat_detail(user, chat_id):
    messages = get_messages(chat_id)
    return jsonify(messages)

@app.route(API_PREFIX + "/", methods=["POST"])
@auth_required
def chat_create(user):
    data = request.json
    name = data.get("name")
    user_ids = [user["user_id"]]
    chat_id = create_chat(name, user_ids)
    return jsonify({"chat_id": chat_id})

@app.route(API_PREFIX + "/<int:chat_id>/leave", methods=["POST"])
@auth_required
def chat_leave(user, chat_id):
    leave_chat(chat_id, user["user_id"])
    return jsonify({"status": "ok"})

@app.route(API_PREFIX + "/<int:chat_id>/message", methods=["POST"])
@auth_required
def chat_send_message(user, chat_id):
    data = request.json
    text = data.get("text")
    send_message(chat_id, user["user_id"], text)
    return jsonify({"status": "ok"})

@app.route(API_PREFIX + "/<int:chat_id>/add-user", methods=["POST"])
@auth_required
def add_user_to_chat(user, chat_id):
    data = request.json
    nickname = data.get("nickname")
    if not nickname:
        return jsonify({"status": "error", "message": "Nickname is required"}), 400

    chats = get_chats_for_user(user["user_id"])
    chats_ids = [chat['id'] for chat in chats]
    if (chat_id in chats_ids):
        add_member_to_chat(chat_id, nickname)
        return jsonify({"status": "ok"})
    else:
        return jsonify({"status": "error", "message": "You are not a member of this chat"}), 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)
