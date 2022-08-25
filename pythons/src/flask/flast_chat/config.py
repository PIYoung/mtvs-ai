import os
from dotenv import load_dotenv

load_dotenv(verbose=True)
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PW = os.getenv("MYSQL_PW")

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PW}@localhost:3306/user"
SQLALCHEMY_TRACK_MODIFICATIONS = False

DEBUG = True
FLASK_APP = "app"
