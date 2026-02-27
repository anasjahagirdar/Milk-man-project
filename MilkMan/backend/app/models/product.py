from app import db
from datetime import datetime

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("category.id"),
        nullable=False
    )

    size = db.Column(db.String(50), nullable=False)
    unit = db.Column(db.String(20), default="custom")
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))
    stock = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category_id": self.category_id,
            "size": self.size,
            "unit": self.unit,
            "price": self.price,
            "description": self.description,
            "stock": self.stock,
            "is_active": self.is_active
        }
