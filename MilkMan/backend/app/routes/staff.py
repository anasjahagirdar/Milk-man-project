from flask import Blueprint, request, jsonify
from app import db
from app.models.staff import Staff
from werkzeug.security import generate_password_hash

staff_bp = Blueprint("staff", __name__)


# CREATE STAFF
@staff_bp.route("/", methods=["POST"])
def create_staff():

    data = request.get_json()

    staff = Staff(
        name=data["name"],
        email=data["email"],
        phone=data.get("phone"),
        role=data.get("role"),
        password=generate_password_hash(data["password"])
    )

    db.session.add(staff)
    db.session.commit()

    return jsonify(staff.to_dict()), 201


# GET ALL STAFF
@staff_bp.route("/", methods=["GET"])
def get_staff():

    staff = Staff.query.all()

    return jsonify([s.to_dict() for s in staff])


# GET ONE STAFF
@staff_bp.route("/<int:id>", methods=["GET"])
def get_one_staff(id):

    staff = Staff.query.get_or_404(id)

    return jsonify(staff.to_dict())


# UPDATE STAFF
@staff_bp.route("/<int:id>", methods=["PUT"])
def update_staff(id):

    staff = Staff.query.get_or_404(id)
    data = request.get_json()

    staff.name = data.get("name", staff.name)
    staff.email = data.get("email", staff.email)
    staff.phone = data.get("phone", staff.phone)
    staff.role = data.get("role", staff.role)

    if data.get("password"):
        staff.password = generate_password_hash(data["password"])

    db.session.commit()

    return jsonify(staff.to_dict())


# DELETE STAFF
@staff_bp.route("/<int:id>", methods=["DELETE"])
def delete_staff(id):

    staff = Staff.query.get_or_404(id)

    db.session.delete(staff)
    db.session.commit()

    return jsonify({"message": "Staff deleted"})