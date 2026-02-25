import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

SQLALCHEMY_DATABASE_URI = "sqlite:///milkman.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False