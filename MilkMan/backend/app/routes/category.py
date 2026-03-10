from flask import Blueprint, request, jsonify
from app import db
from app.authz import require_roles
from app.models.category import Category
from sqlalchemy.exc import IntegrityError

category_bp = Blueprint("category", __name__)


# CREATE CATEGORY
@category_bp.route("/", methods=["POST"])
@require_roles("admin")
def create_category():

    data = request.get_json() or {}
    name = (data.get("name") or "").strip()
    description = (data.get("description") or "").strip() or None

    if not name:
        return jsonify({"error": "Name is required"}), 400

    category = Category(
        name=name,
        description=description
    )

    db.session.add(category)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Category already exists"}), 409

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

    if data.get("name") is not None:
        name = (data.get("name") or "").strip()
        if not name:
            return jsonify({"error": "Name is required"}), 400
        category.name = name
    if data.get("description") is not None:
        category.description = (data.get("description") or "").strip() or None

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Category already exists"}), 409

    return jsonify(category.to_dict())


# DELETE CATEGORY
@category_bp.route("/<int:id>", methods=["DELETE"])
@require_roles("admin")
def delete_category(id):

    category = Category.query.get_or_404(id)

    db.session.delete(category)
    db.session.commit()

    return jsonify({"message": "Category deleted"})
