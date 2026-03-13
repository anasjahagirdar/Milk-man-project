"""
MilkMan Database Seed Script
Run from the backend/ directory: python seed.py

Credentials:
  Admin:    admin@milkman.com     / admin123
  Staff:    staff1@milkman.com    / staff123
            staff2@milkman.com    / staff123
  Customer: customer@milkman.com  / customer123
            (plus 4 more demo customers)

Product images must be in:
  customer-site/assets/images/products/
Current images: milk.avif, butter.avif, curd.avif, ghee.avif, paneer.jpg
"""
import sys
import os

# Make sure we can import app from the backend dir
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.admin import Admin
from app.models.customer import Customer
from app.models.staff import Staff
from app.models.category import Category
from app.models.product import Product
from app.models.subscription import Subscription
from app.models.order import Order
from werkzeug.security import generate_password_hash
from datetime import date, datetime, timedelta


# Delete stale DB BEFORE create_app() runs, so migration code starts with a clean slate
# Flask stores SQLite DBs in the instance/ directory by default
_backend_dir = os.path.dirname(os.path.abspath(__file__))
_db_path = os.path.join(_backend_dir, "instance", "milkman.db")
if not os.path.exists(_db_path):
    # Also check root directory (in case of custom config)
    _db_path_alt = os.path.join(_backend_dir, "milkman.db")
    if os.path.exists(_db_path_alt):
        _db_path = _db_path_alt
if os.path.exists(_db_path):
    os.remove(_db_path)
    print(f"  Removed old DB: {_db_path}")

app = create_app()

with app.app_context():

    print("Creating database tables...")
    db.create_all()

    # -------------------------
    # CATEGORIES
    # -------------------------
    _categories_data = [
        ("Cow Milk",       "Fresh cow milk products"),
        ("Buffalo Milk",   "Rich buffalo milk products"),
        ("Dairy Products", "Ghee, butter, paneer and more"),
    ]
    category_map = {}
    for name, desc in _categories_data:
        cat = Category.query.filter_by(name=name).first()
        if not cat:
            cat = Category(name=name, description=desc)
            db.session.add(cat)
            db.session.flush()
            print(f"  + Category: {name}")
        category_map[name] = cat

    db.session.commit()
    # Refresh map with IDs
    for name, _ in _categories_data:
        category_map[name] = Category.query.filter_by(name=name).first()

    # -------------------------
    # ADMIN
    # -------------------------
    if not Admin.query.filter_by(email="admin@milkman.com").first():
        db.session.add(Admin(
            name="Super Admin",
            email="admin@milkman.com",
            password=generate_password_hash("admin123"),
            is_active=True,
        ))
        print("  + Admin: admin@milkman.com")

    # -------------------------
    # STAFF
    # -------------------------
    staff_data = [
        ("Ravi Kumar",   "staff1@milkman.com", "Delivery Manager"),
        ("Priti Deshpande", "staff2@milkman.com", "Customer Support"),
    ]
    for name, email, role in staff_data:
        if not Staff.query.filter_by(email=email).first():
            db.session.add(Staff(
                name=name,
                email=email,
                password=generate_password_hash("staff123"),
                role=role,
                is_active=True,
            ))
            print(f"  + Staff: {email}")

    db.session.commit()

    # -------------------------
    # CUSTOMERS
    # -------------------------
    customers_data = [
        ("Ananya Joshi",    "customer@milkman.com",  "+91-9876543210", "12, Kothrud Main Road, Pune 411038"),
        ("Rajesh Patil",    "rajesh@milkman.com",    "+91-9876543211", "45, Aundh Rd, Pune 411007"),
        ("Meera Kulkarni",  "meera@milkman.com",     "+91-9876543212", "7, Baner Road, Pune 411045"),
        ("Suresh Nair",     "suresh@milkman.com",    "+91-9876543213", "88, FC Road, Pune 411004"),
        ("Kavita Sharma",   "kavita@milkman.com",    "+91-9876543214", "23, Viman Nagar, Pune 411014"),
    ]
    customer_objs = []
    for i, (name, email, phone, address) in enumerate(customers_data):
        cust = Customer.query.filter_by(email=email).first()
        if not cust:
            cust = Customer(
                name=name,
                email=email,
                phone=phone,
                address=address,
                password=generate_password_hash("customer123"),
                is_active=True,
            )
            db.session.add(cust)
            db.session.flush()
            print(f"  + Customer: {email}")
        customer_objs.append(cust)

    db.session.commit()
    # Refresh
    customer_objs = [Customer.query.filter_by(email=e).first() for _, e, _, _ in customers_data]

    # -------------------------
    # PRODUCTS (matched to image files)
    # -------------------------
    products_data = [
        {
            "name": "Full Cream Cow Milk",
            "description": "Farm-fresh full cream cow milk, rich in calcium and vitamins. Delivered before 7 AM every morning.",
            "price": 72.0,
            "unit": "500ml",
            "stock": 200,
            "image_url": "/assets/images/products/milk.avif",
            "category": "Cow Milk",
        },
        {
            "name": "Buffalo Milk",
            "description": "Thick and creamy buffalo milk from local farms. Perfect for making chai, paneer and sweets.",
            "price": 85.0,
            "unit": "500ml",
            "stock": 150,
            "image_url": "/assets/images/products/milk.avif",
            "category": "Buffalo Milk",
        },
        {
            "name": "Pure Cow Ghee",
            "description": "Traditional hand-churned cow ghee made using the bilona process. No additives, pure gold.",
            "price": 650.0,
            "unit": "500g",
            "stock": 80,
            "image_url": "/assets/images/products/ghee.avif",
            "category": "Dairy Products",
        },
        {
            "name": "White Butter",
            "description": "Unsalted fresh white butter, made daily from cream. Spread it on your morning toast.",
            "price": 120.0,
            "unit": "200g",
            "stock": 100,
            "image_url": "/assets/images/products/butter.avif",
            "category": "Dairy Products",
        },
        {
            "name": "Fresh Paneer",
            "description": "Soft, crumbly paneer made fresh daily from whole milk. Perfect for curries and snacks.",
            "price": 180.0,
            "unit": "250g",
            "stock": 90,
            "image_url": "/assets/images/products/paneer.jpg",
            "category": "Dairy Products",
        },
        {
            "name": "Natural Curd",
            "description": "Thick, probiotic-rich curd set overnight. The ideal companion for your meals.",
            "price": 55.0,
            "unit": "400g",
            "stock": 120,
            "image_url": "/assets/images/products/curd.avif",
            "category": "Cow Milk",
        },
    ]

    product_objs = []
    for pdata in products_data:
        prod = Product.query.filter_by(name=pdata["name"]).first()
        if not prod:
            cat = category_map[pdata["category"]]
            prod = Product(
                name=pdata["name"],
                description=pdata["description"],
                price=pdata["price"],
                unit=pdata["unit"],
                stock=pdata["stock"],
                image_url=pdata["image_url"],
                category_id=cat.id,
                is_active=True,
            )
            db.session.add(prod)
            db.session.flush()
            print(f"  + Product: {pdata['name']}")
        product_objs.append(prod)

    db.session.commit()
    product_objs = [Product.query.filter_by(name=p["name"]).first() for p in products_data]

    # -------------------------
    # SUBSCRIPTIONS (for first demo customer)
    # -------------------------
    demo_customer = customer_objs[0]
    subs_data = [
        (product_objs[0], "daily",     1),  # Full Cream Cow Milk
        (product_objs[2], "weekly",    1),  # Pure Cow Ghee
        (product_objs[5], "alternate", 2),  # Natural Curd
    ]
    sub_objs = []
    for product, frequency, quantity in subs_data:
        existing = Subscription.query.filter_by(
            customer_id=demo_customer.id,
            product_id=product.id,
        ).first()
        if not existing:
            sub = Subscription(
                customer_id=demo_customer.id,
                product_id=product.id,
                start_date=date.today() - timedelta(days=30),
                quantity=quantity,
                frequency=frequency,
                status="active",
                unit_price=product.price,
                payment_status="paid",
            )
            db.session.add(sub)
            db.session.flush()
            print(f"  + Subscription: {demo_customer.name} -> {product.name} ({frequency})")
            sub_objs.append(sub)
        else:
            sub_objs.append(existing)

    db.session.commit()
    sub_objs = [Subscription.query.filter_by(
        customer_id=demo_customer.id,
        product_id=product.id
    ).first() for product, _, _ in subs_data]

    # -------------------------
    # ORDERS (10 orders across multiple customers)
    # -------------------------
    orders_seed = [
        # (customer_idx, product_idx, qty, days_ago, status)
        (0, 0, 1, 1,  "delivered"),
        (0, 0, 1, 2,  "delivered"),
        (0, 0, 1, 3,  "delivered"),
        (0, 5, 2, 5,  "delivered"),
        (0, 2, 1, 7,  "delivered"),
        (0, 0, 1, 0,  "pending"),
        (1, 1, 2, 1,  "delivered"),
        (1, 3, 1, 3,  "delivered"),
        (2, 4, 1, 2,  "pending"),
        (3, 0, 1, 1,  "failed"),
    ]

    for cust_idx, prod_idx, qty, days_ago, status in orders_seed:
        cust = customer_objs[cust_idx]
        prod = product_objs[prod_idx]
        if not cust or not prod:
            continue
        order_date = datetime.utcnow() - timedelta(days=days_ago)
        # Avoid duplicate orders on same day for same customer+product
        existing_order = Order.query.filter_by(
            customer_id=cust.id,
            product_id=prod.id,
            status=status,
        ).filter(Order.order_date >= order_date.date()).first()
        if not existing_order:
            amount = prod.price * qty
            order = Order(
                customer_id=cust.id,
                product_id=prod.id,
                quantity=qty,
                amount=amount,
                total_price=amount,
                status=status,
                order_date=order_date,
                delivered_at=order_date if status == "delivered" else None,
            )
            db.session.add(order)

    db.session.commit()
    print(f"  + Seeded orders")

    print("\nDatabase seeded successfully!")
    print("\nLogin credentials:")
    print("  Admin:    admin@milkman.com    / admin123")
    print("  Staff:    staff1@milkman.com   / staff123")
    print("  Customer: customer@milkman.com / customer123")
