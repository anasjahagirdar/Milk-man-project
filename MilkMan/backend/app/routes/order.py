from flask import Blueprint, request, jsonify
from app import db
from app.authz import current_role, current_user_id, require_roles
from app.models.order import Order
from app.models.customer import Customer
from app.models.product import Product
from datetime import datetime

order_bp = Blueprint("order", __name__)

ALLOWED_STATUSES = {"pending", "delivered", "failed", "cancelled"}


# CREATE ORDER
@order_bp.route("/", methods=["POST"])
@require_roles("admin", "staff", "customer")
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

    try:
        quantity = int(data.get("quantity", 1) or 1)
        if quantity < 1:
            raise ValueError
    except (TypeError, ValueError):
        return jsonify({"error": "quantity must be a positive number"}), 400

    amount = product.price * quantity

    order = Order(
        customer_id=customer_id,
        product_id=data["product_id"],
        subscription_id=data.get("subscription_id"),
        quantity=quantity,
        amount=amount,
        total_price=amount,
        status=data.get("status", "pending"),
    )

    db.session.add(order)
    db.session.commit()

    return jsonify(order.to_dict()), 201


# GET ALL ORDERS
@order_bp.route("/", methods=["GET"])
@require_roles("admin", "staff")
def get_orders():
    status_filter = request.args.get("status")
    q = Order.query
    if status_filter and status_filter in ALLOWED_STATUSES:
        q = q.filter(Order.status == status_filter)
    orders = q.order_by(Order.order_date.desc()).all()
    result = []
    for o in orders:
        d = o.to_dict()
        if o.customer:
            d["customer_name"] = o.customer.name
            d["customer_email"] = o.customer.email
        result.append(d)
    return jsonify(result)


# ORDERS SUMMARY (admin only)
@order_bp.route("/summary", methods=["GET"])
@require_roles("admin", "staff")
def orders_summary():
    all_orders = Order.query.all()
    summary = {
        "total": len(all_orders),
        "pending": sum(1 for o in all_orders if o.status == "pending"),
        "delivered": sum(1 for o in all_orders if o.status == "delivered"),
        "failed": sum(1 for o in all_orders if o.status == "failed"),
        "total_revenue": sum(o.amount or 0 for o in all_orders if o.status == "delivered"),
    }
    return jsonify(summary)


# MY ORDERS (customer)
@order_bp.route("/my", methods=["GET"])
@require_roles("customer")
def get_my_orders():
    user_id = current_user_id()
    if not user_id:
        return jsonify({"error": "Authentication required"}), 401
    orders = Order.query.filter_by(customer_id=user_id).order_by(Order.order_date.desc()).all()
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


# GET ORDERS BY CUSTOMER (admin/staff)
@order_bp.route("/customer/<int:customer_id>", methods=["GET"])
@require_roles("admin", "staff")
def get_by_customer(customer_id):
    orders = Order.query.filter_by(customer_id=customer_id).order_by(Order.order_date.desc()).all()
    return jsonify([o.to_dict() for o in orders])


# UPDATE ORDER STATUS
@order_bp.route("/<int:id>", methods=["PUT"])
@require_roles("admin", "staff")
def update_order(id):
    order = Order.query.get_or_404(id)
    data = request.get_json() or {}

    if data.get("status"):
        status = data["status"].lower()
        if status not in ALLOWED_STATUSES:
            return jsonify({"error": f"Status must be one of: {', '.join(ALLOWED_STATUSES)}"}), 400
        order.status = status
        if status == "delivered" and not order.delivered_at:
            order.delivered_at = datetime.utcnow()

    if data.get("quantity") is not None:
        try:
            quantity = int(data["quantity"])
            if quantity < 1:
                raise ValueError
        except (TypeError, ValueError):
            return jsonify({"error": "quantity must be a positive number"}), 400
        order.quantity = quantity
        product = Product.query.get(order.product_id)
        if product:
            order.amount = product.price * quantity
            order.total_price = order.amount

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
