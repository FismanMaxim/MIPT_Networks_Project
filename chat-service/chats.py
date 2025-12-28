from db import get_connection
from mysql.connector import Error

def get_chats_for_user(user_id):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT c.id, c.name, c.date_added
                FROM chat c
                JOIN chat_2_user cu ON c.id = cu.chat_id
                WHERE cu.user_id = %s
                ORDER BY c.date_added DESC
            """
            cursor.execute(query, (user_id,))
            chats = cursor.fetchall()
            return chats
        finally:
            cursor.close()
    finally:
        conn.close()


def get_messages(chat_id):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT m.id, m.chat_id, m.sender_id, u.nickname as sender_nickname, m.text, m.date_sent
                FROM messages m
                JOIN users u ON u.id = m.sender_id
                WHERE m.chat_id = %s
                ORDER BY m.date_sent ASC
            """
            cursor.execute(query, (chat_id,))
            messages = cursor.fetchall()
            return messages
        finally:
            cursor.close()
    finally:
        conn.close()


def create_chat(name, user_ids):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO chat (name, date_added) VALUES (%s, NOW())",
                (name,)
            )
            chat_id = cursor.lastrowid
            for uid in user_ids:
                cursor.execute(
                    "INSERT INTO chat_2_user (chat_id, user_id) VALUES (%s, %s)",
                    (chat_id, uid)
                )
            conn.commit()
            return chat_id
        except Error as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
    finally:
        conn.close()


def leave_chat(chat_id, user_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM chat_2_user WHERE chat_id=%s AND user_id=%s",
                (chat_id, user_id)
            )
            conn.commit()
        except Error as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
    finally:
        conn.close()


def send_message(chat_id, sender_id, text):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO messages (chat_id, sender_id, text, date_sent) VALUES (%s,%s,%s,NOW())",
                (chat_id, sender_id, text)
            )
            conn.commit()
        except Error as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
    finally:
        conn.close()

def add_member_to_chat(chat_id, member_nickname):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO chat_2_user (chat_id, user_id) 
                SELECT %s, u.id 
                FROM users u
                WHERE nickname = %s
                """,
                (chat_id, member_nickname)
            )
            conn.commit()
        except Error as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
    finally:
        conn.close()
