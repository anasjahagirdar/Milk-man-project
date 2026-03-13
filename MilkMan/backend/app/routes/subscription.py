from flask import Blueprint, request, jsonify
from app import db
from app.authz import current_role, current_user_id, require_roles
from app.models.subscription import Subscription
from app.models.customer import Customer
from app.models.product import Product
from datetime import date, datetime, timedelta

subscription_bp = Blueprint("subscription", __name__)

ALLOWED_FREQUENCIES = {"daily": 1, "alternate": 2, "weekly": 7}
ALLOWED_STATUSES = {"active", "paused", "cancelled", "canceled"}


def _parse_date(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value).date()
    except Exception:
        return None


def _deliveries_per_month(frequency):
    if frequency == "daily":
        return 30
    if frequency == "alternate":
        return 15
    if frequency == "weekly":
        return 4
    return 0


def _next_delivery(sub, today=None):
    today = today or date.today()
    if sub.status in ("canceled", "cancelled"):
        return None

    start = sub.start_date
    if not start:
        return None

    interval = ALLOWED_FREQUENCIES.get(sub.frequency or "daily", 1)

    base = today
    if sub.status == "paused":
        if sub.paused_until and sub.paused_until >= today:
            base = sub.paused_until + timedelta(days=1)
        else:
            base = today

    if start >= base:
        return start

    delta_days = (base - start).days
    steps = (delta_days + interval - 1) // interval
    return start + timedelta(days=steps * interval)


def _serialize(sub, include_product=False):
    data = sub.to_dict()
    nxt = _next_delivery(sub)
    data["next_delivery_date"] = nxt.isoformat() if nxt else None
    if include_product:
        product = Product.query.get(sub.product_id)
        data["product"] = product.to_dict() if product else None
    return data


# CREATE SUBSCRIPTION
@subscription_bp.route("/", methods=["POST"])
@require_roles("customer", "admin", "staff")
def create_subscription():
    data = request.get_json() or {}

    role = current_role()
    user_id = current_user_id() if role == "customer" else None
    customer_id = data.get("customer_id")
    if user_id:
        customer_id = user_id

    if not customer_id or not Customer.query.get(customer_id):
        return jsonify({"error": "Customer not found"}), 404

    product = Product.query.get(data.get("product_id"))
    if not product:
        return jsonify({"error": "Product not found"}), 404

    # Check for duplicate active subscription
    existing = Subscription.query.filter_by(
        customer_id=customer_id,
        product_id=product.id,
        status="active"
    ).first()
    if existing:
        return jsonify({"error": "You already have an active subscription for this product"}), 409

    start_date = _parse_date(data.get("start_date")) or date.today()
    end_date = _parse_date(data.get("end_date"))
    if end_date and end_date < start_date:
        return jsonify({"error": "end_date cannot be before start_date"}), 400

    try:
        quantity = int(data.get("quantity", 1) or 1)
    except Exception:
        return jsonify({"error": "quantity must be a number"}), 400
    if quantity < 1:
        return jsonify({"error": "quantity must be at least 1"}), 400

    frequency = (data.get("frequency") or "daily").strip().lower()
    if frequency not in ALLOWED_FREQUENCIES:
        return jsonify({"error": "Invalid frequency. Use: daily, alternate, weekly"}), 400

    subscription = Subscription(
        customer_id=customer_id,
        product_id=data["product_id"],
        start_date=start_date,
        end_date=end_date,
        quantity=quantity,
        frequency=frequency,
        status="active",
        unit_price=product.price,
        payment_status=(data.get("payment_status") or "pending").strip().lower(),
        notes=(data.get("notes") or "").strip() or None,
    )

    db.session.add(subscription)
    db.session.commit()

    return jsonify(_serialize(subscription, include_product=True)), 201


# GET ALL SUBSCRIPTIONS — customers see own, admin/staff see all
@subscription_bp.route("/", methods=["GET"])
@require_roles("admin", "staff", "customer")
def get_subscriptions():
    role = current_role()
    if role == "customer":
        user_id = current_user_id()
        if not user_id:
            return jsonify({"error": "Authentication required"}), 401
        subs = Subscription.query.filter_by(customer_id=user_id).all()
    else:
        subs = Subscription.query.all()

    result = []
    for s in subs:
        d = _serialize(s, include_product=True)
        if role in ("admin", "staff") and s.customer:
            d["customer_name"] = s.customer.name
            d["customer_email"] = s.customer.email
        result.append(d)
    return jsonify(result)


# MY SUBSCRIPTIONS (customer shortcut)
@subscription_bp.route("/my", methods=["GET"])
@require_roles("customer")
def get_my_subscriptions():
    user_id = current_user_id()
    if not user_id:
        return jsonify({"error": "Authentication required"}), 401
    subs = Subscription.query.filter_by(customer_id=user_id).all()
    return jsonify([_serialize(s, include_product=True) for s in subs])


# PREVIEW
@subscription_bp.route("/preview", methods=["GET"])
def preview_subscription():
    product_id = request.args.get("product_id", type=int)
    if not product_id:
        return jsonify({"error": "product_id is required"}), 400

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    quantity = request.args.get("quantity", default=1, type=int) or 1
    if quantity < 1:
        return jsonify({"error": "quantity must be at least 1"}), 400

    frequency = (request.args.get("frequency") or "daily").strip().lower()
    if frequency not in ALLOWED_FREQUENCIES:
        return jsonify({"error": "Invalid frequency"}), 400

    deliveries = _deliveries_per_month(frequency)
    unit_price = product.price

    return jsonify({
        "product": product.to_dict(),
        "unit_price": unit_price,
        "quantity": quantity,
        "frequency": frequency,
        "deliveries_per_month": deliveries,
        "estimated_monthly_total": round(unit_price * quantity * deliveries, 2),
    })


# GET ONE SUBSCRIPTION
@subscription_bp.route("/<int:id>", methods=["GET"])
@require_roles("customer", "admin", "staff")
def get_subscription(id):
    sub = Subscription.query.get_or_404(id)
    role = current_role()
    user_id = current_user_id() if role == "customer" else None
    if user_id and sub.customer_id != user_id:
        return jsonify({"error": "Forbidden"}), 403
    return jsonify(_serialize(sub, include_product=True))


# GET SUBSCRIPTIONS BY CUSTOMER (admin/staff)
@subscription_bp.route("/customer/<int:customer_id>", methods=["GET"])
@require_roles("admin", "staff")
def get_by_customer(customer_id):
    subs = Subscription.query.filter_by(customer_id=customer_id).all()
    return jsonify([_serialize(s, include_product=True) for s in subs])


# UPDATE SUBSCRIPTION
@subscription_bp.route("/<int:id>", methods=["PUT"])
@require_roles("customer", "admin", "staff")
def update_subscription(id):
    sub = Subscription.query.get_or_404(id)
    data = request.get_json() or {}

    role = current_role()
    user_id = current_user_id() if role == "customer" else None
    if user_id and sub.customer_id != user_id:
        return jsonify({"error": "Forbidden"}), 403

    if data.get("status") is not None:
        status = data["status"].lower()
        if status in ("cancelled", "canceled"):
            sub.status = "canceled"
            sub.canceled_at = datetime.utcnow()
            sub.end_date = date.today()
        elif status == "paused":
            sub.status = "paused"
        elif status == "active":
            sub.status = "active"
            sub.paused_until = None
        else:
            return jsonify({"error": "Invalid status"}), 400

    if data.get("quantity") is not None:
        try:
            quantity = int(data.get("quantity") or 1)
        except Exception:
            return jsonify({"error": "quantity must be a number"}), 400
        if quantity < 1:
            return jsonify({"error": "quantity must be at least 1"}), 400
        sub.quantity = quantity

    if data.get("frequency") is not None:
        frequency = (data.get("frequency") or "").strip().lower()
        if frequency not in ALLOWED_FREQUENCIES:
            return jsonify({"error": "Invalid frequency"}), 400
        sub.frequency = frequency

    if data.get("payment_status"):
        sub.payment_status = data["payment_status"]
        sub.payment_updated_at = datetime.utcnow()

    db.session.commit()
    return jsonify(_serialize(sub, include_product=True))


# DELETE SUBSCRIPTION
@subscription_bp.route("/<int:id>", methods=["DELETE"])
@require_roles("admin", "staff")
def delete_subscription(id):
    sub = Subscription.query.get_or_404(id)
    db.session.delete(sub)
    db.session.commit()
    return jsonify({"message": "Subscription deleted"})


# PAUSE
@subscription_bp.route("/<int:id>/pause", methods=["POST"])
@require_roles("customer", "admin", "staff")
def pause_subscription(id):
    sub = Subscription.query.get_or_404(id)
    role = current_role()
    user_id = current_user_id() if role == "customer" else None
    if user_id and sub.customer_id != user_id:
        return jsonify({"error": "Forbidden"}), 403

    data = request.get_json() or {}
    paused_until = _parse_date(data.get("paused_until"))

    sub.status = "paused"
    sub.paused_until = paused_until

    db.session.commit()
    return jsonify(_serialize(sub, include_product=True))


# RESUME
@subscription_bp.route("/<int:id>/resume", methods=["POST"])
@require_roles("customer", "admin", "staff")
def resume_subscription(id):
    sub = Subscription.query.get_or_404(id)
    role = current_role()
    user_id = current_user_id() if role == "customer" else None
    if user_id and sub.customer_id != user_id:
        return jsonify({"error": "Forbidden"}), 403

    sub.status = "active"
    sub.paused_until = None

    db.session.commit()
    return jsonify(_serialize(sub, include_product=True))


# CANCEL
@subscription_bp.route("/<int:id>/cancel", methods=["POST"])
@require_roles("customer", "admin", "staff")
def cancel_subscription(id):
    sub = Subscription.query.get_or_404(id)
    role = current_role()
    user_id = current_user_id() if role == "customer" else None
    if user_id and sub.customer_id != user_id:
        return jsonify({"error": "Forbidden"}), 403

    sub.status = "canceled"
    sub.canceled_at = datetime.utcnow()
    sub.end_date = date.today()

    db.session.commit()
    return jsonify(_serialize(sub, include_product=True))
