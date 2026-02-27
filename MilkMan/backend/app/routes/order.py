from flask import Blueprint, request, jsonify
from app import db
from app.authz import current_role, current_user_id, require_roles
from app.models.order import Order
from app.models.customer import Customer
from app.models.product import Product

order_bp = Blueprint("order", __name__)


# CREATE ORDER
@order_bp.route("/", methods=["POST"])
@require_roles("customer", "admin", "staff")
def create_order():

    data = request.get_json() or {}

    role = current_role()
    user_id = current_user_id() if role == "customer" else None
    customer_id = data.get("customer_id")

    if user_id:
        customer_id = user_id

    if not customer_id:
        return jsonify({"error": "customer_id is required"}), 400

    customer = Customer.query.get(customer_id)
    product = Product.query.get(data.get("product_id"))

    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    if not product:
        return jsonify({"error": "Product not found"}), 404

    quantity = int(data.get("quantity", 1) or 1)
    if quantity < 1:
        return jsonify({"error": "quantity must be at least 1"}), 400

    if not data.get("size"):
        return jsonify({"error": "size is required"}), 400

    total_price = product.price * quantity

    order = Order(
        customer_id=customer_id,
        product_id=data["product_id"],
        quantity=quantity,
        size=data["size"],
        total_price=total_price
    )

    db.session.add(order)
    db.session.commit()

    return jsonify(order.to_dict()), 201


# GET ALL ORDERS
@order_bp.route("/", methods=["GET"])
@require_roles("admin", "staff")
def get_orders():

    orders = Order.query.all()

    return jsonify([o.to_dict() for o in orders])


# GET ONE ORDER
@order_bp.route("/<int:id>", methods=["GET"])
@require_roles("customer", "admin", "staff")
def get_order(id):

    order = Order.query.get_or_404(id)

    role = current_role()
    user_id = current_user_id() if role == "customer" else None
    if user_id and order.customer_id != user_id:
        return jsonify({"error": "Forbidden"}), 403

    return jsonify(order.to_dict())


# GET ORDERS BY CUSTOMER
@order_bp.route("/customer/<int:customer_id>", methods=["GET"])
@require_roles("admin", "staff")
def get_by_customer(customer_id):

    orders = Order.query.filter_by(customer_id=customer_id).all()

    return jsonify([o.to_dict() for o in orders])


# UPDATE ORDER STATUS
@order_bp.route("/<int:id>", methods=["PUT"])
@require_roles("admin", "staff")
def update_order(id):

    order = Order.query.get_or_404(id)
    data = request.get_json() or {}

    if data.get("status"):
        order.status = data["status"]

    db.session.commit()

    return jsonify(order.to_dict())


# DELETE ORDER
@order_bp.route("/<int:id>", methods=["DELETE"])
@require_roles("admin")
def delete_order(id):

    order = Order.query.get_or_404(id)

    db.session.delete(order)
    db.session.commit()

    return jsonify({"message": "Order deleted"})


@order_bp.route("/my", methods=["GET"])
@require_roles("customer")
def get_my_orders():
    user_id = current_user_id()
    if not user_id:
        return jsonify({"error": "Authentication required"}), 401
    orders = Order.query.filter_by(customer_id=user_id).all()
    return jsonify([o.to_dict() for o in orders])
