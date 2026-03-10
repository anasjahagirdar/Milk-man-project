import argparse

from werkzeug.security import generate_password_hash

from app import create_app, db
from app.models.admin import Admin
from app.models.customer import Customer


def upsert_admin(name, email, password):
    admin = Admin.query.filter_by(email=email).first()
    if admin is None:
        admin = Admin.query.order_by(Admin.id.asc()).first()

    if admin is None:
        admin = Admin(
            name=name,
            email=email,
            password=generate_password_hash(password),
        )
        db.session.add(admin)
    else:
        admin.name = name
        admin.email = email
        admin.password = generate_password_hash(password)

    return admin


def upsert_customer(name, email, password, phone=None, address=None):
    customer = Customer.query.filter_by(email=email).first()

    if customer is None:
        customer = Customer(
            name=name,
            email=email,
            phone=phone,
            address=address,
            password=generate_password_hash(password),
        )
        db.session.add(customer)
    else:
        customer.name = name
        customer.phone = phone
        customer.address = address
        customer.password = generate_password_hash(password)

    return customer


def main():
    parser = argparse.ArgumentParser(
        description="Reset the admin account and create or update a customer account.",
    )
    parser.add_argument("--admin-name", default="Super Admin")
    parser.add_argument("--admin-email", default="admin@milkman.com")
    parser.add_argument("--admin-password", default="MilkManAdmin@2026")
    parser.add_argument("--customer-name", default="Demo Customer")
    parser.add_argument("--customer-email", default="customer@milkman.com")
    parser.add_argument("--customer-password", default="MilkManUser@2026")
    parser.add_argument("--customer-phone", default="9876543210")
    parser.add_argument("--customer-address", default="Pune")
    args = parser.parse_args()

    app = create_app()

    with app.app_context():
        db.create_all()

        admin = upsert_admin(
            name=args.admin_name.strip(),
            email=args.admin_email.strip().lower(),
            password=args.admin_password,
        )
        customer = upsert_customer(
            name=args.customer_name.strip(),
            email=args.customer_email.strip().lower(),
            password=args.customer_password,
            phone=(args.customer_phone or "").strip() or None,
            address=(args.customer_address or "").strip() or None,
        )

        db.session.commit()

        print("Admin account ready:")
        print(f"  email: {admin.email}")
        print(f"  password: {args.admin_password}")
        print("Customer account ready:")
        print(f"  email: {customer.email}")
        print(f"  password: {args.customer_password}")


if __name__ == "__main__":
    main()
