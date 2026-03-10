import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "milkman-dev-secret-key-change-me-please-2026",
)
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", SECRET_KEY)

SQLALCHEMY_DATABASE_URI = "sqlite:///milkman.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False

CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "*").split(",") if o.strip()]

JWT_TOKEN_LOCATION = ["headers", "cookies"]
JWT_COOKIE_SECURE = os.getenv("JWT_COOKIE_SECURE", "false").lower() == "true"
JWT_COOKIE_SAMESITE = os.getenv("JWT_COOKIE_SAMESITE", "Lax")
JWT_COOKIE_CSRF_PROTECT = os.getenv("JWT_COOKIE_CSRF_PROTECT", "true").lower() == "true"
JWT_ACCESS_COOKIE_PATH = "/"
JWT_REFRESH_COOKIE_PATH = "/api/auth"
JWT_CSRF_CHECK_FORM = False

JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.getenv("JWT_ACCESS_MINUTES", "30")))
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.getenv("JWT_REFRESH_DAYS", "30")))
