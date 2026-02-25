from flask import Blueprint, request, jsonify
from app import db
from app.models.subscription import Subscription
from app.models.customer import Customer
from app.models.product import Product
from datetime import datetime

subscription_bp = Blueprint("subscription", __name__)


# CREATE SUBSCRIPTION
@subscription_bp.route("/", methods=["POST"])
def create_subscription():

    data = request.get_json()

    # validate customer
    if not Customer.query.get(data["customer_id"]):
        return jsonify({"error": "Customer not found"}), 404

    # validate product
    if not Product.query.get(data["product_id"]):
        return jsonify({"error": "Product not found"}), 404

    subscription = Subscription(
        customer_id=data["customer_id"],
        product_id=data["product_id"],
        start_date=datetime.fromisoformat(data["start_date"]).date(),
        end_date=datetime.fromisoformat(data["end_date"]).date() if data.get("end_date") else None,
        quantity=data.get("quantity", 1),
        payment_status=data.get("payment_status", "pending"),
        notes=data.get("notes")
    )

    db.session.add(subscription)
    db.session.commit()

    return jsonify(subscription.to_dict()), 201


# GET ALL SUBSCRIPTIONS
@subscription_bp.route("/", methods=["GET"])
def get_subscriptions():

    subs = Subscription.query.all()

    return jsonify([s.to_dict() for s in subs])


# GET ONE SUBSCRIPTION
@subscription_bp.route("/<int:id>", methods=["GET"])
def get_subscription(id):

    sub = Subscription.query.get_or_404(id)

    return jsonify(sub.to_dict())


# GET SUBSCRIPTIONS BY CUSTOMER
@subscription_bp.route("/customer/<int:customer_id>", methods=["GET"])
def get_by_customer(customer_id):

    subs = Subscription.query.filter_by(customer_id=customer_id).all()

    return jsonify([s.to_dict() for s in subs])


# UPDATE SUBSCRIPTION
@subscription_bp.route("/<int:id>", methods=["PUT"])
def update_subscription(id):

    sub = Subscription.query.get_or_404(id)
    data = request.get_json()

    sub.quantity = data.get("quantity", sub.quantity)

    if data.get("payment_status"):
        sub.payment_status = data["payment_status"]
        sub.payment_updated_at = datetime.utcnow()

    db.session.commit()

    return jsonify(sub.to_dict())


# DELETE SUBSCRIPTION
@subscription_bp.route("/<int:id>", methods=["DELETE"])
def delete_subscription(id):

    sub = Subscription.query.get_or_404(id)

    db.session.delete(sub)
    db.session.commit()

    return jsonify({"message": "Subscription deleted"})