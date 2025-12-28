import os

API_PREFIX = "/mychat/api"
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DB")
JWT_SECRET = os.getenv("JWT_SECRET")

API_PREFIX = "/mychat/api/chat"