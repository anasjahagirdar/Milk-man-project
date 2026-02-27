import re

from flask import Blueprint, request, jsonify
from app import db
from app.authz import current_user_id, require_roles
from app.models.customer import Customer
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash


customer_bp = Blueprint("customer", __name__)

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


# CREATE CUSTOMER
@customer_bp.route("/", methods=["POST"])
@require_roles("admin", "staff")
def create_customer():

    data = request.get_json() or {}

    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password")
    phone = (data.get("phone") or "").strip() or None
    address = (data.get("address") or "").strip() or None

    if not name:
        return jsonify({"error": "Name is required"}), 400
    if not email or not _EMAIL_RE.match(email):
        return jsonify({"error": "Valid email is required"}), 400
    if not password or len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400
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

    return jsonify(customer.to_dict()), 201


# GET CUSTOMERS (pagination + search)
@customer_bp.route("/", methods=["GET"])
@require_roles("admin", "staff")
def get_customers():

    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    search = request.args.get("search")

    query = Customer.query

    if search:
        query = query.filter(Customer.name.contains(search))

    customers = query.paginate(
        page=page,
        per_page=limit,
        error_out=False
    )

    return jsonify({
        "total": customers.total,
        "data": [c.to_dict() for c in customers.items]
    })


# GET ONE CUSTOMER
@customer_bp.route("/<int:id>", methods=["GET"])
@require_roles("admin", "staff")
def get_customer(id):

    customer = Customer.query.get_or_404(id)

    return jsonify(customer.to_dict())


# UPDATE CUSTOMER
@customer_bp.route("/<int:id>", methods=["PUT"])
@require_roles("admin", "staff")
def update_customer(id):

    customer = Customer.query.get_or_404(id)

    data = request.get_json() or {}

    customer.name = data.get("name", customer.name)
    if data.get("email"):
        email = (data.get("email") or "").strip().lower()
        if not email or not _EMAIL_RE.match(email):
            return jsonify({"error": "Valid email is required"}), 400
        customer.email = email
    customer.phone = data.get("phone", customer.phone)
    customer.address = data.get("address", customer.address)

    if data.get("password"):
        if len(data["password"]) < 8:
            return jsonify({"error": "Password must be at least 8 characters"}), 400
        customer.password = generate_password_hash(data["password"])

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email already registered"}), 409

    return jsonify(customer.to_dict())


# DELETE CUSTOMER (soft delete)
@customer_bp.route("/<int:id>", methods=["DELETE"])
@require_roles("admin", "staff")
def delete_customer(id):

    customer = Customer.query.get_or_404(id)

    db.session.delete(customer)
    db.session.commit()

    return jsonify({"message": "Customer deleted"})


@customer_bp.route("/me", methods=["GET"])
@require_roles("customer")
def get_me():
    user_id = current_user_id()
    if not user_id:
        return jsonify({"error": "Authentication required"}), 401
    customer = Customer.query.get_or_404(user_id)
    return jsonify(customer.to_dict())


@customer_bp.route("/me", methods=["PUT"])
@require_roles("customer")
def update_me():
    user_id = current_user_id()
    if not user_id:
        return jsonify({"error": "Authentication required"}), 401
    customer = Customer.query.get_or_404(user_id)
    data = request.get_json() or {}

    if data.get("name") is not None:
        name = (data.get("name") or "").strip()
        if not name:
            return jsonify({"error": "Name is required"}), 400
        customer.name = name

    if data.get("phone") is not None:
        customer.phone = (data.get("phone") or "").strip() or None

    if data.get("address") is not None:
        customer.address = (data.get("address") or "").strip() or None

    if data.get("password"):
        if len(data["password"]) < 8:
            return jsonify({"error": "Password must be at least 8 characters"}), 400
        customer.password = generate_password_hash(data["password"])

    db.session.commit()
    return jsonify(customer.to_dict())
