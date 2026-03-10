from flask import Blueprint, request, jsonify
from app import db
from app.authz import require_roles
from app.models.admin import Admin
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash


admin_bp = Blueprint("admin", __name__)


def _clean_email(value):
    return (value or "").strip().lower()


# CREATE ADMIN
@admin_bp.route("/", methods=["POST"])
def create_admin():
    if Admin.query.count() > 0:
        verify_jwt_in_request()
        claims = get_jwt() or {}
        if claims.get("role") != "admin":
            return jsonify({"error": "Forbidden"}), 403

    data = request.get_json() or {}
    name = (data.get("name") or "").strip()
    email = _clean_email(data.get("email"))
    password = data.get("password")

    if not name:
        return jsonify({"error": "Name is required"}), 400
    if not email:
        return jsonify({"error": "Email is required"}), 400
    if not password or len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400

    admin = Admin(
        name=name,
        email=email,
        password=generate_password_hash(password)
    )

    db.session.add(admin)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email already registered"}), 409

    return jsonify(admin.to_dict()), 201


# GET ALL ADMINS
@admin_bp.route("/", methods=["GET"])
@require_roles("admin")
def get_admins():

    admins = Admin.query.all()

    return jsonify([a.to_dict() for a in admins])


# GET ONE ADMIN
@admin_bp.route("/<int:id>", methods=["GET"])
@require_roles("admin")
def get_admin(id):

    admin = Admin.query.get_or_404(id)

    return jsonify(admin.to_dict())


# UPDATE ADMIN
@admin_bp.route("/<int:id>", methods=["PUT"])
@require_roles("admin")
def update_admin(id):
    admin = Admin.query.get_or_404(id)
    data = request.get_json() or {}

    if data.get("name") is not None:
        name = (data.get("name") or "").strip()
        if not name:
            return jsonify({"error": "Name is required"}), 400
        admin.name = name

    if data.get("email") is not None:
        email = _clean_email(data.get("email"))
        if not email:
            return jsonify({"error": "Email is required"}), 400
        admin.email = email

    if data.get("password"):
        if len(data["password"]) < 8:
            return jsonify({"error": "Password must be at least 8 characters"}), 400
        admin.password = generate_password_hash(data["password"])

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email already registered"}), 409

    return jsonify(admin.to_dict())


# DELETE ADMIN
@admin_bp.route("/<int:id>", methods=["DELETE"])
@require_roles("admin")
def delete_admin(id):

    admin = Admin.query.get_or_404(id)

    db.session.delete(admin)
    db.session.commit()

    return jsonify({"message": "Admin deleted"})
