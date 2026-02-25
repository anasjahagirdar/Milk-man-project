from app import create_app, db

# import ALL models so SQLAlchemy registers tables
from app.models.admin import Admin
from app.models.customer import Customer
from app.models.staff import Staff
from app.models.category import Category
from app.models.product import Product
from app.models.subscription import Subscription
from app.models.order import Order

from werkzeug.security import generate_password_hash


app = create_app()

with app.app_context():

    print("Creating database tables...")

    db.create_all()

    # -------------------
    # SEED CATEGORIES
    # -------------------

    categories = ["Cow Milk", "Buffalo Milk", "Ghee"]

    for name in categories:
        exists = Category.query.filter_by(name=name).first()
        if not exists:
            db.session.add(
                Category(
                    name=name,
                    description=f"{name} products"
                )
            )

    # -------------------
    # SEED DEFAULT ADMIN
    # -------------------

    if not Admin.query.filter_by(email="admin@milkman.com").first():
        db.session.add(
            Admin(
                name="Super Admin",
                email="admin@milkman.com",
                password=generate_password_hash("admin123")
            )
        )

    db.session.commit()

    print("Database created + seeded successfully!")