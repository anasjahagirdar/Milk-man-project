
from flask import Blueprint, request, jsonify
from app import db
from app.authz import require_roles
from app.models.admin import Admin
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from werkzeug.security import generate_password_hash


admin_bp = Blueprint("admin", __name__)


# CREATE ADMIN
@admin_bp.route("/", methods=["POST"])

def create_admin():

    if Admin.query.count() > 0:
        verify_jwt_in_request()
        claims = get_jwt() or {}
        if claims.get("role") != "admin":
            return jsonify({"error": "Forbidden"}), 403

    data = request.get_json() or {}

    admin = Admin(
        name=data["name"],
        email=data["email"],
        password=generate_password_hash(data["password"])
    )

    db.session.add(admin)
    db.session.commit()

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

    admin.name = data.get("name", admin.name)
    admin.email = data.get("email", admin.email)

    if data.get("password"):
        admin.password = generate_password_hash(data["password"])

    db.session.commit()

    return jsonify(admin.to_dict())


# DELETE ADMIN
@admin_bp.route("/<int:id>", methods=["DELETE"])
@require_roles("admin")
def delete_admin(id):

    admin = Admin.query.get_or_404(id)

    db.session.delete(admin)
    db.session.commit()

    return jsonify({"message": "Admin deleted"})
