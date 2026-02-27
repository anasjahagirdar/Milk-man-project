from flask import Blueprint, request, jsonify
from app import db
from app.authz import require_roles
from app.models.category import Category

category_bp = Blueprint("category", __name__)


# CREATE CATEGORY
@category_bp.route("/", methods=["POST"])
@require_roles("admin")
def create_category():

    data = request.get_json() or {}

    category = Category(
        name=data["name"],
        description=data.get("description")
    )

    db.session.add(category)
    db.session.commit()

    return jsonify(category.to_dict()), 201


# GET ALL CATEGORIES
@category_bp.route("/", methods=["GET"])
def get_categories():

    categories = Category.query.all()

    return jsonify([c.to_dict() for c in categories])


# GET ONE CATEGORY
@category_bp.route("/<int:id>", methods=["GET"])
def get_category(id):

    category = Category.query.get_or_404(id)

    return jsonify(category.to_dict())


# UPDATE CATEGORY
@category_bp.route("/<int:id>", methods=["PUT"])
@require_roles("admin")
def update_category(id):

    category = Category.query.get_or_404(id)

    data = request.get_json() or {}

    category.name = data.get("name", category.name)
    category.description = data.get("description", category.description)

    db.session.commit()

    return jsonify(category.to_dict())


# DELETE CATEGORY
@category_bp.route("/<int:id>", methods=["DELETE"])
@require_roles("admin")
def delete_category(id):

    category = Category.query.get_or_404(id)

    db.session.delete(category)
    db.session.commit()

    return jsonify({"message": "Category deleted"})
