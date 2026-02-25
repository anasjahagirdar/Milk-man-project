
from flask import Blueprint, request, jsonify
from app import db
from app.models.admin import Admin
from werkzeug.security import generate_password_hash


admin_bp = Blueprint("admin", __name__)


# CREATE ADMIN
@admin_bp.route("/", methods=["POST"])

def create_admin():

    data = request.get_json()

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

def get_admins():

    admins = Admin.query.all()

    return jsonify([a.to_dict() for a in admins])


# GET ONE ADMIN
@admin_bp.route("/<int:id>", methods=["GET"])

def get_admin(id):

    admin = Admin.query.get_or_404(id)

    return jsonify(admin.to_dict())


# UPDATE ADMIN
@admin_bp.route("/<int:id>", methods=["PUT"])

def update_admin(id):

    admin = Admin.query.get_or_404(id)

    data = request.get_json()

    admin.name = data.get("name", admin.name)
    admin.email = data.get("email", admin.email)

    if data.get("password"):
        admin.password = generate_password_hash(data["password"])

    db.session.commit()

    return jsonify(admin.to_dict())


# DELETE ADMIN
@admin_bp.route("/<int:id>", methods=["DELETE"])

def delete_admin(id):

    admin = Admin.query.get_or_404(id)

    db.session.delete(admin)
    db.session.commit()

    return jsonify({"message": "Admin deleted"})