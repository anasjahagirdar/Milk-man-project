import re

from flask import Blueprint, request, jsonify
from app import db
from app.models.admin import Admin
from app.models.staff import Staff
from app.models.customer import Customer
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
)
from app.authz import require_roles

auth_bp = Blueprint("auth", __name__)

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _clean_email(value):
    if not value:
        return ""
    return value.strip().lower()


def _validate_password(password):
    if not password or len(password) < 8:
        return "Password must be at least 8 characters"
    return None


# ------------------
# ADMIN LOGIN
# ------------------
@auth_bp.route("/admin/login", methods=["POST"])
def admin_login():

    data = request.get_json() or {}

    email = _clean_email(data.get("email"))
    password = data.get("password")

    admin = Admin.query.filter_by(email=email).first()

    if not admin or not check_password_hash(admin.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    # IMPORTANT → identity must be STRING
    token = create_access_token(identity=str(admin.id), additional_claims={"role": "admin"})

    return jsonify({
        "token": token,
        "user": admin.to_dict()
    })


# ------------------
# STAFF LOGIN
# ------------------
@auth_bp.route("/staff/login", methods=["POST"])
def staff_login():

    data = request.get_json() or {}

    email = _clean_email(data.get("email"))
    password = data.get("password")

    staff = Staff.query.filter_by(email=email).first()

    if not staff or not check_password_hash(staff.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity=str(staff.id), additional_claims={"role": "staff"})

    return jsonify({
        "token": token,
        "user": staff.to_dict()
    })


# ------------------
# CUSTOMER SIGNUP
# ------------------
@auth_bp.route("/customer/signup", methods=["POST"])
def customer_signup():

    data = request.get_json() or {}

    name = (data.get("name") or "").strip()
    email = _clean_email(data.get("email"))
    password = data.get("password")
    phone = (data.get("phone") or "").strip() or None
    address = (data.get("address") or "").strip() or None

    if not name:
        return jsonify({"error": "Name is required"}), 400

    if not email or not _EMAIL_RE.match(email):
        return jsonify({"error": "Valid email is required"}), 400

    password_error = _validate_password(password)
    if password_error:
        return jsonify({"error": password_error}), 400

    if Customer.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409

    customer = Customer(
        name=name,
        email=email,
        phone=phone,
        address=address,
        password=generate_password_hash(password),
    )

    db.session.add(customer)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email already registered"}), 409

    access_token = create_access_token(
        identity=str(customer.id),
        additional_claims={"role": "customer"},
    )
    refresh_token = create_refresh_token(
        identity=str(customer.id),
        additional_claims={"role": "customer"},
    )

    resp = jsonify({"user": customer.to_dict(), "token": access_token})
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp, 201


# ------------------
# CUSTOMER LOGIN
# ------------------
@auth_bp.route("/customer/login", methods=["POST"])
def customer_login():

    data = request.get_json() or {}

    email = _clean_email(data.get("email"))
    password = data.get("password")

    customer = Customer.query.filter_by(email=email).first()

    if not customer or not check_password_hash(customer.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(
        identity=str(customer.id),
        additional_claims={"role": "customer"},
    )
    refresh_token = create_refresh_token(
        identity=str(customer.id),
        additional_claims={"role": "customer"},
    )

    resp = jsonify({"token": access_token, "user": customer.to_dict()})
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp


@auth_bp.route("/customer/me", methods=["GET"])
@require_roles("customer")
def customer_me():
    user_id = get_jwt_identity()
    customer = Customer.query.get(int(user_id)) if user_id else None
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    return jsonify(customer.to_dict())


@auth_bp.route("/customer/refresh", methods=["POST"])
@jwt_required(refresh=True)
def customer_refresh():
    user_id = get_jwt_identity()
    access_token = create_access_token(
        identity=str(user_id),
        additional_claims={"role": "customer"},
    )
    resp = jsonify({"token": access_token})
    set_access_cookies(resp, access_token)
    return resp


@auth_bp.route("/customer/logout", methods=["POST"])
def customer_logout():
    resp = jsonify({"message": "Logged out"})
    unset_jwt_cookies(resp)
    return resp
