from flask import Blueprint, request, jsonify
from app.models.admin import Admin
from app.models.staff import Staff
from app.models.customer import Customer
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)


# ------------------
# ADMIN LOGIN
# ------------------
@auth_bp.route("/admin/login", methods=["POST"])
def admin_login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    admin = Admin.query.filter_by(email=email).first()

    if not admin or not check_password_hash(admin.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    # IMPORTANT → identity must be STRING
    token = create_access_token(identity=str(admin.id))

    return jsonify({
        "token": token,
        "user": admin.to_dict()
    })


# ------------------
# STAFF LOGIN
# ------------------
@auth_bp.route("/staff/login", methods=["POST"])
def staff_login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    staff = Staff.query.filter_by(email=email).first()

    if not staff or not check_password_hash(staff.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity=str(staff.id))

    return jsonify({
        "token": token,
        "user": staff.to_dict()
    })


# ------------------
# CUSTOMER LOGIN
# ------------------
@auth_bp.route("/customer/login", methods=["POST"])
def customer_login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    customer = Customer.query.filter_by(email=email).first()

    if not customer or not check_password_hash(customer.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity=str(customer.id))

    return jsonify({
        "token": token,
        "user": customer.to_dict()
    })