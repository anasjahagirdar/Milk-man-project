from flask import Blueprint, request, jsonify
from app import db
from app.authz import require_roles
from app.models.staff import Staff
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

staff_bp = Blueprint("staff", __name__)


def _clean_email(value):
    return (value or "").strip().lower()


# CREATE STAFF
@staff_bp.route("/", methods=["POST"])
@require_roles("admin")
def create_staff():

    data = request.get_json() or {}
    name = (data.get("name") or "").strip()
    email = _clean_email(data.get("email"))
    password = data.get("password")
    role = (data.get("role") or "").strip() or None
    phone = (data.get("phone") or "").strip() or None

    if not name:
        return jsonify({"error": "Name is required"}), 400
    if not email:
        return jsonify({"error": "Email is required"}), 400
    if not password or len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400

    staff = Staff(
        name=name,
        email=email,
        phone=phone,
        role=role,
        password=generate_password_hash(password)
    )

    db.session.add(staff)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email already registered"}), 409

    return jsonify(staff.to_dict()), 201


# GET ALL STAFF
@staff_bp.route("/", methods=["GET"])
@require_roles("admin", "staff")
def get_staff():

    staff = Staff.query.all()

    return jsonify([s.to_dict() for s in staff])


# GET ONE STAFF
@staff_bp.route("/<int:id>", methods=["GET"])
@require_roles("admin", "staff")
def get_one_staff(id):

    staff = Staff.query.get_or_404(id)

    return jsonify(staff.to_dict())


# UPDATE STAFF
@staff_bp.route("/<int:id>", methods=["PUT"])
@require_roles("admin")
def update_staff(id):

    staff = Staff.query.get_or_404(id)
    data = request.get_json() or {}

    if data.get("name") is not None:
        name = (data.get("name") or "").strip()
        if not name:
            return jsonify({"error": "Name is required"}), 400
        staff.name = name

    if data.get("email") is not None:
        email = _clean_email(data.get("email"))
        if not email:
            return jsonify({"error": "Email is required"}), 400
        staff.email = email

    if data.get("phone") is not None:
        staff.phone = (data.get("phone") or "").strip() or None

    if data.get("role") is not None:
        staff.role = (data.get("role") or "").strip() or None

    if data.get("password"):
        if len(data["password"]) < 8:
            return jsonify({"error": "Password must be at least 8 characters"}), 400
        staff.password = generate_password_hash(data["password"])

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email already registered"}), 409

    return jsonify(staff.to_dict())


# DELETE STAFF
@staff_bp.route("/<int:id>", methods=["DELETE"])
@require_roles("admin")
def delete_staff(id):

    staff = Staff.query.get_or_404(id)

    db.session.delete(staff)
    db.session.commit()

    return jsonify({"message": "Staff deleted"})
