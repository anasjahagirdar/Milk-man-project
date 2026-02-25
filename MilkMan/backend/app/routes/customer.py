from flask import Blueprint, request, jsonify
from app import db
from app.models.customer import Customer
from werkzeug.security import generate_password_hash


customer_bp = Blueprint("customer", __name__)


# CREATE CUSTOMER
@customer_bp.route("/", methods=["POST"])

def create_customer():

    data = request.get_json()

    customer = Customer(
        name=data["name"],
        email=data["email"],
        phone=data.get("phone"),
        address=data.get("address"),
        password=generate_password_hash(data["password"])
    )

    db.session.add(customer)
    db.session.commit()

    return jsonify(customer.to_dict()), 201


# GET CUSTOMERS (pagination + search)
@customer_bp.route("/", methods=["GET"])

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

def get_customer(id):

    customer = Customer.query.get_or_404(id)

    return jsonify(customer.to_dict())


# UPDATE CUSTOMER
@customer_bp.route("/<int:id>", methods=["PUT"])

def update_customer(id):

    customer = Customer.query.get_or_404(id)

    data = request.get_json()

    customer.name = data.get("name", customer.name)
    customer.email = data.get("email", customer.email)
    customer.phone = data.get("phone", customer.phone)
    customer.address = data.get("address", customer.address)

    if data.get("password"):
        customer.password = generate_password_hash(data["password"])

    db.session.commit()

    return jsonify(customer.to_dict())


# DELETE CUSTOMER (soft delete)
@customer_bp.route("/<int:id>", methods=["DELETE"])

def delete_customer(id):

    customer = Customer.query.get_or_404(id)

    db.session.delete(customer)
    db.session.commit()

    return jsonify({"message": "Customer deleted"})