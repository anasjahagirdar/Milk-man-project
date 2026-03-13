from flask import Blueprint, request, jsonify
from app import db
from app.authz import require_roles
from app.models.product import Product
from app.models.category import Category

product_bp = Blueprint("product", __name__)


# CREATE PRODUCT
@product_bp.route("/", methods=["POST"])
@require_roles("admin")
def create_product():
    data = request.get_json() or {}
    name = (data.get("name") or "").strip()
    category_id = data.get("category_id")
    price = data.get("price")

    if not name:
        return jsonify({"error": "Name is required"}), 400
    if category_id is None:
        return jsonify({"error": "category_id is required"}), 400
    if price is None:
        return jsonify({"error": "price is required"}), 400
    try:
        price = float(price)
        if price < 0:
            raise ValueError
    except (TypeError, ValueError):
        return jsonify({"error": "price must be a positive number"}), 400

    if not Category.query.get(category_id):
        return jsonify({"error": "Category not found"}), 404

    unit = (data.get("unit") or "500ml").strip()
    stock = data.get("stock", 0)
    try:
        stock = int(stock)
        if stock < 0:
            raise ValueError
    except (TypeError, ValueError):
        return jsonify({"error": "stock must be a non-negative integer"}), 400

    product = Product(
        name=name,
        category_id=category_id,
        unit=unit,
        price=price,
        description=(data.get("description") or "").strip() or None,
        stock=stock,
        image_url=(data.get("image_url") or "").strip() or None,
        is_active=bool(data.get("is_active", True)),
    )

    db.session.add(product)
    db.session.commit()

    return jsonify(product.to_dict()), 201


# GET ALL PRODUCTS
@product_bp.route("/", methods=["GET"])
def get_products():
    q = Product.query
    unit = request.args.get("unit")
    category_id = request.args.get("category_id", type=int)
    search = request.args.get("search")
    active = request.args.get("active")

    if unit:
        q = q.filter(Product.unit == unit)
    if category_id:
        q = q.filter(Product.category_id == category_id)
    if search:
        q = q.filter(Product.name.contains(search))
    # Default: only active products for public endpoint
    if active is not None:
        if active.lower() in ("true", "1"):
            q = q.filter(Product.is_active.is_(True))
        elif active.lower() in ("false", "0"):
            q = q.filter(Product.is_active.is_(False))
    else:
        # When no active filter specified, return only active
        q = q.filter(Product.is_active.is_(True))

    products = q.all()
    return jsonify([p.to_dict() for p in products])


# GET PRODUCT BY ID
@product_bp.route("/<int:id>", methods=["GET"])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify(product.to_dict())


# GET PRODUCTS BY CATEGORY
@product_bp.route("/category/<int:category_id>", methods=["GET"])
def get_by_category(category_id):
    products = Product.query.filter_by(category_id=category_id, is_active=True).all()
    return jsonify([p.to_dict() for p in products])


# UPDATE PRODUCT
@product_bp.route("/<int:id>", methods=["PUT"])
@require_roles("admin")
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json() or {}

    if data.get("category_id") is not None and not Category.query.get(data.get("category_id")):
        return jsonify({"error": "Category not found"}), 404

    if data.get("name") is not None:
        name = (data.get("name") or "").strip()
        if not name:
            return jsonify({"error": "Name is required"}), 400
        product.name = name

    if data.get("category_id") is not None:
        product.category_id = data["category_id"]
    if data.get("price") is not None:
        product.price = data["price"]
    if data.get("unit") is not None:
        product.unit = (data["unit"] or "").strip() or product.unit
    if "description" in data:
        product.description = (data.get("description") or "").strip() or None
    if data.get("stock") is not None:
        product.stock = data["stock"]
    if "image_url" in data:
        product.image_url = (data.get("image_url") or "").strip() or None
    if data.get("is_active") is not None:
        product.is_active = bool(data["is_active"])

    db.session.commit()
    return jsonify(product.to_dict())


# SOFT DELETE PRODUCT (deactivate)
@product_bp.route("/<int:id>", methods=["DELETE"])
@require_roles("admin")
def delete_product(id):
    product = Product.query.get_or_404(id)
    product.is_active = False
    db.session.commit()
    return jsonify({"message": "Product deactivated", "id": id})
