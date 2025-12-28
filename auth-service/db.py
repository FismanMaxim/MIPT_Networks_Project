import mysql.connector
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, MYSQL_PORT


def get_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        port=MYSQL_PORT,
    )

def insert_user(login, password_hash, nickname):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (login, password_hash, nickname)
        VALUES (%s, %s, %s)
    """, (login, password_hash, nickname))

    conn.commit()
    cursor.close()
    conn.close()


def find_user_by_login(login):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE login = %s", (login,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()
    return user
