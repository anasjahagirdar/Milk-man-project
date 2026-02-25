from flask import Blueprint, request, jsonify
from app import db
from app.models.order import Order
from app.models.customer import Customer
from app.models.product import Product

order_bp = Blueprint("order", __name__)


# CREATE ORDER
@order_bp.route("/", methods=["POST"])
def create_order():

    data = request.get_json()

    customer = Customer.query.get(data["customer_id"])
    product = Product.query.get(data["product_id"])

    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    if not product:
        return jsonify({"error": "Product not found"}), 404

    total_price = product.price * data.get("quantity", 1)

    order = Order(
        customer_id=data["customer_id"],
        product_id=data["product_id"],
        quantity=data.get("quantity", 1),
        size=data["size"],
        total_price=total_price
    )

    db.session.add(order)
    db.session.commit()

    return jsonify(order.to_dict()), 201


# GET ALL ORDERS
@order_bp.route("/", methods=["GET"])
def get_orders():

    orders = Order.query.all()

    return jsonify([o.to_dict() for o in orders])


# GET ONE ORDER
@order_bp.route("/<int:id>", methods=["GET"])
def get_order(id):

    order = Order.query.get_or_404(id)

    return jsonify(order.to_dict())


# GET ORDERS BY CUSTOMER
@order_bp.route("/customer/<int:customer_id>", methods=["GET"])
def get_by_customer(customer_id):

    orders = Order.query.filter_by(customer_id=customer_id).all()

    return jsonify([o.to_dict() for o in orders])


# UPDATE ORDER STATUS
@order_bp.route("/<int:id>", methods=["PUT"])
def update_order(id):

    order = Order.query.get_or_404(id)
    data = request.get_json()

    if data.get("status"):
        order.status = data["status"]

    db.session.commit()

    return jsonify(order.to_dict())


# DELETE ORDER
@order_bp.route("/<int:id>", methods=["DELETE"])
def delete_order(id):

    order = Order.query.get_or_404(id)

    db.session.delete(order)
    db.session.commit()

    return jsonify({"message": "Order deleted"})