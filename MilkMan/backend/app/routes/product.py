from flask import Blueprint, request, jsonify
from app import db
from app.authz import require_roles
from app.models.product import Product
from app.models.category import Category

product_bp = Blueprint("product", __name__)

ALLOWED_UNITS = {"L", "ml", "kg", "g", "pieces", "custom"}


# CREATE PRODUCT
@product_bp.route("/", methods=["POST"])
@require_roles("admin")
def create_product():

    data = request.get_json() or {}

    # validate category exists
    if not Category.query.get(data["category_id"]):
        return jsonify({"error": "Category not found"}), 404

    # validate size (free-form but required)
    if not data.get("size"):
        return jsonify({"error": "Size is required"}), 400

    # validate unit
    unit = (data.get("unit") or "custom").strip().lower()
    unit_map = {"liters": "L", "liter": "L", "l": "L", "milliliters": "ml"}
    unit = unit_map.get(unit, unit)
    if unit not in ALLOWED_UNITS:
        return jsonify({"error": "Invalid unit"}), 400

    product = Product(
        name=data["name"],
        category_id=data["category_id"],
        size=data["size"],
        unit=unit,
        price=data["price"],
        description=data.get("description"),
        stock=data.get("stock", 0),
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
    if active is not None:
        if active.lower() in ("true", "1"):
            q = q.filter(Product.is_active.is_(True))
        elif active.lower() in ("false", "0"):
            q = q.filter(Product.is_active.is_(False))

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

    products = Product.query.filter_by(category_id=category_id).all()

    return jsonify([p.to_dict() for p in products])


# UPDATE PRODUCT
@product_bp.route("/<int:id>", methods=["PUT"])
@require_roles("admin")
def update_product(id):

    product = Product.query.get_or_404(id)
    data = request.get_json() or {}

    if data.get("size") is not None and not data.get("size"):
        return jsonify({"error": "Size is required"}), 400

    if data.get("unit") is not None:
        unit = (data.get("unit") or "").strip().lower()
        unit_map = {"liters": "L", "liter": "L", "l": "L", "milliliters": "ml"}
        unit = unit_map.get(unit, unit)
        if unit not in ALLOWED_UNITS:
            return jsonify({"error": "Invalid unit"}), 400
        product.unit = unit

    product.name = data.get("name", product.name)
    product.category_id = data.get("category_id", product.category_id)
    product.size = data.get("size", product.size)
    product.price = data.get("price", product.price)
    product.description = data.get("description", product.description)
    product.stock = data.get("stock", product.stock)
    if data.get("is_active") is not None:
        product.is_active = bool(data.get("is_active"))

    db.session.commit()

    return jsonify(product.to_dict())


# DELETE PRODUCT
@product_bp.route("/<int:id>", methods=["DELETE"])
@require_roles("admin")
def delete_product(id):

    product = Product.query.get_or_404(id)

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Product deleted"})
