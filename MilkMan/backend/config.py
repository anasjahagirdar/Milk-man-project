import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    os.getenv("JWT_SECRET", "milkman-dev-secret-key-change-me-please-2026"),
)
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", os.getenv("JWT_SECRET", SECRET_KEY))

SQLALCHEMY_DATABASE_URI = os.getenv(
    "DATABASE_URL",
    os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///milkman.db"),
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

CORS_ORIGINS = [
    o.strip()
    for o in os.getenv(
        "CORS_ORIGINS",
        "http://127.0.0.1:3000,http://localhost:3000,"
        "http://127.0.0.1:3001,http://localhost:3001,"
        "http://127.0.0.1:8000,http://localhost:8000,"
        "http://127.0.0.1:5173,http://localhost:5173,"
        "null",  # browsers send 'null' origin for file:// pages
    ).split(",")
    if o.strip()
]

JWT_TOKEN_LOCATION = ["headers", "cookies"]
JWT_COOKIE_SECURE = os.getenv("JWT_COOKIE_SECURE", "false").lower() == "true"
JWT_COOKIE_SAMESITE = os.getenv("JWT_COOKIE_SAMESITE", "Lax")
JWT_COOKIE_CSRF_PROTECT = os.getenv("JWT_COOKIE_CSRF_PROTECT", "false").lower() == "true"
JWT_ACCESS_COOKIE_PATH = "/"
JWT_REFRESH_COOKIE_PATH = "/api/auth"
JWT_CSRF_CHECK_FORM = False

# 7 days for development convenience
JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=int(os.getenv("JWT_ACCESS_DAYS", "7")))
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.getenv("JWT_REFRESH_DAYS", "30")))