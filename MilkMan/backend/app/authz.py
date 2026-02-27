from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt, get_jwt_identity, verify_jwt_in_request


def require_roles(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt() or {}
            role = claims.get("role")
            if roles and role not in roles:
                return jsonify({"error": "Forbidden"}), 403
            return fn(*args, **kwargs)

        return wrapper

    return decorator


def current_user_id():
    verify_jwt_in_request(optional=True)
    identity = get_jwt_identity()
    if identity is None:
        return None
    try:
        return int(identity)
    except Exception:
        return None


def current_role():
    verify_jwt_in_request(optional=True)
    claims = get_jwt() or {}
    return claims.get("role")
