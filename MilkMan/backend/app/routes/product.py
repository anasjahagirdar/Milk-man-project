from flask import Blueprint, request, jsonify
from app import db
from app.models.product import Product
from app.models.category import Category

product_bp = Blueprint("product", __name__)

ALLOWED_SIZES = ["0.5L", "1L", "2L"]


# CREATE PRODUCT
@product_bp.route("/", methods=["POST"])
def create_product():

    data = request.get_json()

    # validate category exists
    if not Category.query.get(data["category_id"]):
        return jsonify({"error": "Category not found"}), 404

    # validate size
    if data["size"] not in ALLOWED_SIZES:
        return jsonify({"error": "Invalid size"}), 400

    product = Product(
        name=data["name"],
        category_id=data["category_id"],
        size=data["size"],
        price=data["price"],
        description=data.get("description"),
        stock=data.get("stock", 0)
    )

    db.session.add(product)
    db.session.commit()

    return jsonify(product.to_dict()), 201


# GET ALL PRODUCTS
@product_bp.route("/", methods=["GET"])
def get_products():

    products = Product.query.all()

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
def update_product(id):

    product = Product.query.get_or_404(id)
    data = request.get_json()

    if data.get("size") and data["size"] not in ALLOWED_SIZES:
        return jsonify({"error": "Invalid size"}), 400

    product.name = data.get("name", product.name)
    product.category_id = data.get("category_id", product.category_id)
    product.size = data.get("size", product.size)
    product.price = data.get("price", product.price)
    product.description = data.get("description", product.description)
    product.stock = data.get("stock", product.stock)

    db.session.commit()

    return jsonify(product.to_dict())


# DELETE PRODUCT
@product_bp.route("/<int:id>", methods=["DELETE"])
def delete_product(id):

    product = Product.query.get_or_404(id)

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Product deleted"})