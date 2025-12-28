import os

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DB")
MYSQL_PORT = os.getenv("MYSQL_PORT")

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGO = "HS256"

API_PREFIX = "/mychat/api/auth"
